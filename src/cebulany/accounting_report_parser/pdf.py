#!/usr/bin/env python3
from decimal import Decimal
from datetime import datetime
import re
from typing import IO

from py_pdf_parser.loaders import load
from py_pdf_parser.exceptions import NoElementFoundError


RE_MONEY = re.compile(r"(?P<unit>-?[\s\d]+)[,.](?P<fract>\d\d)\s*(?P<currency>[A-Z]+)")
RE_CODE = re.compile(r"(CEN|PSD)\d{8,}|5620-4VMTF1-001", re.IGNORECASE)
LA_PARAMS = dict(
    line_margin=1.5,
)


def parse(filename: IO):
    document = load(filename, la_params=LA_PARAMS)
    for page in document.pages:
        yield from _parse_page(page)


def _parse_page(page):
    try:
        lp_el = page.elements.filter_by_text_equal("Lp.").extract_single_element()
    except NoElementFoundError:
        return
    for row_index_el in page.elements.below(lp_el):
        try:
            index = int(row_index_el.text())
        except ValueError:
            continue

        els = list(page.elements.to_the_right_of(row_index_el, tolerance=1.0))
        els.sort(key=lambda el: el.bounding_box.x0)

        if len(els) == 4:
            date, addr_iban, desc, amount_saldo = (el.text() for el in els)
            *addr, iban = addr_iban.split('\n')
            addr = ' '.join(addr).strip()
        elif len(els) == 3:
            addr = ""
            iban = ""
            date, desc, amount_saldo = (el.text() for el in els)
        else:
            raise RuntimeError([repr(el.text()) for el in els])

        date = _parse_date(date)

        code_match = RE_CODE.search(desc)
        assert code_match is not None, desc

        yield {
            "line_num": index,
            "date": date,
            "iban": iban.strip(),
            "name": addr.replace('\n', ' ').strip(),
            "title": desc.replace('\n', ' ').strip(),
            "cost": _parse_cost(amount_saldo),
            "ref_id": f"{date:%Y%m%d}::{code_match[0]}",
        }


def _parse_date(raw):
    return datetime.strptime(raw, "%d.%m.%Y").date()


def _parse_cost(raw):
    raw_amount = raw.split("\n")[0]
    match_amount = RE_MONEY.match(raw_amount)
    if not match_amount:
        raise ValueError(f"unknown money format: {raw_amount}")
    assert match_amount, raw_amount
    assert match_amount.group("currency").upper() == "PLN"
    unit = re.sub(r"\s+", "", match_amount.group("unit"))
    fract = match_amount.group("fract")
    return Decimal(f"{unit}.{fract}")
