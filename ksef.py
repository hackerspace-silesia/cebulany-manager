import argparse
from base64 import b64decode, b64encode
from dataclasses import dataclass
from pathlib import Path
import calendar
import shutil
import subprocess
from tempfile import TemporaryDirectory
from time import sleep
from zipfile import ZipFile

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

import requests

TOKEN = Path("ksef_token").read_text().strip()
URL = "https://api.ksef.mf.gov.pl/v2"
NIP = "6312679080"

parser = argparse.ArgumentParser()
parser.add_argument("date")


def main():
    args = parser.parse_args()
    raw_year, raw_month = args.date.split("-")
    year = int(raw_year)
    month = int(raw_month)

    public_keys = _public_key()
    challenge = _challenge()
    auth = _auth(public_keys["KsefTokenEncryption"], challenge)

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {auth.access_token}"

    try:
        symkey = SymKey.make(public_keys["SymmetricKeyEncryption"])
        parts = _get_invoices_file(session, symkey, 2, year, month)

        with TemporaryDirectory() as tmpdirname:
            dir = Path(tmpdirname)
            for part in parts:
                path = Path(part["partName"])
                filename = Path(path.stem).with_suffix(".zip")
                filepath = dir / filename
                _save_file(filepath, part["url"], symkey)
                _seek_in_zip(filepath)
                shutil.copyfile(filepath, filename)

    finally:
        resp = session.delete(URL + "/auth/sessions/current")
        resp.raise_for_status()


def _seek_in_zip(filepath: Path):
    with ZipFile(filepath, mode="a") as zip:
        for filename in zip.namelist():
            if not filename.endswith("xml"):
                continue
            content = zip.read(filename)
            stem, _, _ = filename.partition(".")
            output = subprocess.run(
                ["nodejs", "generate-invoice.js"],
                input=content,
                # check=True,
                capture_output=True,
                text=False,
            )
            if output.returncode != 0:
                print(filename, output.returncode, output.stderr)
            else:
                zip.writestr(stem + ".pdf", output.stdout)


@dataclass
class ChallengeResp:
    challenge: str
    timestamp: int


@dataclass
class PublicKey:
    key_id: str
    certifiate_base64: str
    certifiate_id: str

    def make_cipher(self):
        key = RSA.importKey(b64decode(self.certifiate_base64))
        return PKCS1_OAEP.new(key, hashAlgo=SHA256)


@dataclass
class AuthToken:
    access_token: str
    refresh_token: str
    reference: str


@dataclass
class SymKey:
    public_key: PublicKey
    init_vec: bytes
    symmetric_key: bytes

    @classmethod
    def make(cls, public_key: PublicKey):
        return cls(
            public_key=public_key,
            init_vec=get_random_bytes(16),
            symmetric_key=get_random_bytes(32),
        )

    def make_crypted_key(self):
        return self.public_key.make_cipher().encrypt(self.symmetric_key)


def _save_file(path: Path, url: str, symkey: SymKey):
    cipher = AES.new(symkey.symmetric_key, mode=AES.MODE_CBC, iv=symkey.init_vec)

    with requests.get(url, stream=True) as resp:
        resp.raise_for_status()
        data = b""
        for chunk in resp.iter_content(chunk_size=1024**2):
            data += chunk

    with open(path, "wb") as file:
        decrypted = cipher.decrypt(data)
        unpadded = unpad(decrypted, block_size=AES.block_size)
        file.write(unpadded)


def _get_invoices_file(
    session: requests.Session,
    key: SymKey,
    subject: int,
    year: int,
    month: int,
):
    _, days = calendar.monthrange(year, month)
    from_dt = f"{year}-{month:02d}-01T00:00:00"
    to_dt = f"{year}-{month:02d}-{days:02d}T23:59:59"

    resp = session.post(
        url=URL + "/invoices/exports",
        json={
            "encryption": {
                "publicKeyId": key.public_key.key_id,
                "encryptedSymmetricKey": b64encode(key.make_crypted_key()).decode(),
                "initializationVector": b64encode(key.init_vec).decode(),
            },
            "filters": {
                "subjectType": f"Subject{subject}",
                "dateRange": {
                    "dateType": "PermanentStorage",
                    "from": from_dt,
                    "to": to_dt,
                },
            },
        },
    )

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as exp:
        data = resp.json()
        exp.add_note(str(data["exception"].get("exceptionDetailList")))
        raise

    reference = resp.json()["referenceNumber"]

    for i in range(10):
        resp = session.get(URL + f"/invoices/exports/{reference}")
        resp.raise_for_status()
        data = resp.json()
        match data["status"]["code"]:
            case 100:
                sleep(1)
                continue
            case 200:
                return [o for o in data["package"]["parts"]]
            case code:
                reason = data["status"]["description"]
                raise RuntimeError(f"error code after ksef-token: {code} ({reason})")
    else:
        raise RuntimeError("Too many retries.")


def _get_invoices(session: requests.Session, subject: int, year: int, month: int):
    _, days = calendar.monthrange(year, month)
    from_dt = f"{year}-{month:02d}-01T00:00:00"
    to_dt = f"{year}-{month:02d}-{days:02d}T23:59:59"
    page_offset = 0
    while True:
        resp = session.post(
            url=URL + "/invoices/query/metadata",
            params={
                "sortOrder": "Asc",
                "pageOffset": page_offset,
                "pageSize": 250,
            },
            json={
                "subjectType": f"Subject{subject}",
                "dateRange": {
                    "dateType": "PermanentStorage",
                    "from": from_dt,
                    "to": to_dt,
                },
            },
        )
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exp:
            data = resp.json()
            exp.add_note(str(data["status"].get("details")))
            raise

        data = resp.json()
        invoices = data["invoices"]
        yield from invoices

        if not invoices:
            break

        if not data["hasMore"]:
            break

        if data["isTruncated"]:
            page_offset = 0
            from_dt = invoices[-1]["permanentStorageDate"]
        else:
            page_offset += 1


def _challenge() -> ChallengeResp:
    resp = requests.post(url=URL + "/auth/challenge")
    resp.raise_for_status()
    data = resp.json()
    return ChallengeResp(data["challenge"], data["timestampMs"])


def _public_key() -> dict[str, PublicKey]:
    resp = requests.get(url=URL + "/security/public-key-certificates")
    resp.raise_for_status()

    def make_key(data):
        assert len(data["usage"]) == 1
        return PublicKey(
            key_id=data["publicKeyId"],
            certifiate_base64=data["certificate"],
            certifiate_id=data["certificateId"],
        )

    return {data["usage"][0]: make_key(data) for data in resp.json()}


def _auth(public_key: PublicKey, challenge: ChallengeResp) -> AuthToken:
    token = f"{TOKEN}|{challenge.timestamp}"
    crypted_token = public_key.make_cipher().encrypt(token.encode())

    resp = requests.post(
        url=URL + "/auth/ksef-token",
        json={
            "challenge": challenge.challenge,
            "contextIdentifier": {"type": "Nip", "value": NIP},
            "publicKeyId": public_key.key_id,
            "encryptedToken": b64encode(crypted_token).decode(),
        },
    )
    resp.raise_for_status()
    data = resp.json()
    reference = data["referenceNumber"]
    auth_token = data["authenticationToken"]["token"]

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {auth_token}"

    for i in range(10):
        resp = session.get(url=URL + f"/auth/{reference}")
        resp.raise_for_status()
        data = resp.json()
        match data["status"]["code"]:
            case 100:
                sleep(1)
                continue
            case 200:
                break
            case code:
                reason = data["status"]["description"]
                raise RuntimeError(f"error code after ksef-token: {code} ({reason})")
    else:
        raise RuntimeError("Something is wrong in authentication token")

    resp = session.post(url=URL + "/auth/token/redeem")
    resp.raise_for_status()
    data = resp.json()
    access_token = data["accessToken"]["token"]
    refresh_token = data["refreshToken"]["token"]

    return AuthToken(
        reference=reference,
        access_token=access_token,
        refresh_token=refresh_token,
    )


if __name__ == "__main__":
    main()
