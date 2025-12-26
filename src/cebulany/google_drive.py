from datetime import date
from decimal import Decimal
from functools import partial
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
ALL_FIELDS = [
    "id",
    "name",
    "mimeType",
    "modifiedTime",
    "description",
    "properties",
    "parents",
]
DIR_MIMETYPE = "application/vnd.google-apps.folder"


def filter_year_directory(year: int, dirname: str) -> bool:
    return dirname.lower() == f"rok {year}"


def filter_month_directory(month: int, dirname: str) -> bool:
    return dirname.startswith(f"{month:02d}-")


def find_files_by_date(year: int, month: int):

    def first_el(items, filter):
        return next(item for item in items if filter(item["name"]))

    service = build("drive", "v3", credentials=_login())
    find = partial(_find, service)
    year_items = find(f"'{INVOICES_ID}' in parents and mimeType = '{DIR_MIMETYPE}'")
    year_item = first_el(year_items, partial(filter_year_directory, year))
    year_item_id = year_item["id"]
    month_items = find(f"'{year_item_id}' in parents and mimeType = '{DIR_MIMETYPE}'")
    month_item = first_el(month_items, partial(filter_month_directory, month))

    yield from find(
        query=f"'{month_item['id']}' in parents and mimeType != '{DIR_MIMETYPE}' and not trashed",
        fields=ALL_FIELDS,
    )


def update_file(
    id,
    filename: str,
    accounting_record: str | None,
    accounting_date: date | None,
    company_name: str | None,
    price: Decimal | None,
    description: str,
    fields=ALL_FIELDS,
):
    service = build("drive", "v3", credentials=_login())

    properties = {}
    if accounting_record:
        properties["accounting_record"] = accounting_record
    if accounting_date:
        properties["accounting_date"] = accounting_date.isoformat()
    if company_name:
        properties["company_name"] = company_name
    if price:
        properties["price"] = str(price)

    body = {
        "name": filename,
        "description": description,
        "properties": properties,
    }

    return (
        service.files()
        .update(
            fileId=id,
            body=body,
            supportsAllDrives=True,
            fields=", ".join(fields),
        )
        .execute()
    )


def _find(service, query=None, fields=ALL_FIELDS):
    # Call the Drive v3 API
    page_token = None
    while True:
        results = (
            service.files()
            .list(
                pageSize=50,
                fields=f"nextPageToken, files({', '.join(fields)})",
                corpora="allDrives",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=page_token,
                q=query,
            )
            .execute()
        )
        items = results.get("files", [])
        yield from items

        page_token = results.get("nextPageToken")
        if page_token is None:
            break


def get_file_by_id(service, id, fields=["id", "name"]):
    return (
        service.files()
        .get(
            fileId=id,
            supportsAllDrives=True,
            fields=", ".join(fields),
        )
        .execute()
    )


def _login():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    FILENAME = "/data/token.json"
    if os.path.exists(FILENAME):
        creds = Credentials.from_authorized_user_file(FILENAME, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("/data/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(FILENAME, "w") as token:
            token.write(creds.to_json())
    return creds
