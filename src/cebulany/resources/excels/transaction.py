from collections import defaultdict
from decimal import Decimal
from functools import partial
from itertools import chain
from typing import Iterable, NamedTuple

from openpyxl import Workbook
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText

from cebulany.auth import token_required
from cebulany.models import Payment, Transaction
from cebulany.resources.excels.utils import send_excel, setup_styles, add_cell
from cebulany.resources.excels.blueprint import excel_page, URL_PREFIX
from cebulany.queries.transaction import TransactionQuery


@excel_page.route(URL_PREFIX + "/transactions/<int:year>-<int:month>")
@token_required
def excel_transaction(year: int, month: int):
    dt = f"{year}-{month:02d}"
    transactions = TransactionQuery.get_transactions(month=dt)
    workbook = gen_workbook(dt, transactions)
    download_name = f"transaction-{dt}.xlsx"
    return send_excel(workbook, download_name)


def gen_workbook(dt: str, transactions: list[Transaction]):
    workbook = Workbook()
    setup_styles(workbook, font_size=8)
    fill_worksheet(workbook.active, dt, transactions)

    return workbook


def fill_worksheet(sheet, dt: str, transactions: list[Transaction]):
    sheet.title = f"Zestawienie {dt}"
    add = partial(add_cell, sheet)
    sheet.append(["", add(sheet.title, "header")])
    sheet.append(
        [
            add("L.p", "header"),
            add("data", "header"),
            add("Kontrahent / Numer rachunku", "header"),
            add("Opis / Typ transakcji", "header"),
            add("Kwota", "header"),
            add("Rodzaj", "header"),
            add("Źródło finansowania wydatku", "header"),
        ]
    )

    sheet.merge_cells(
        start_row=1,
        end_row=1,
        start_column=2,
        end_column=7,
    )

    sheet.column_dimensions["A"].width = 5.0
    sheet.column_dimensions["B"].width = 10.0
    sheet.column_dimensions["C"].width = 40.0
    sheet.column_dimensions["D"].width = 40.0
    sheet.column_dimensions["E"].width = 15.0
    sheet.column_dimensions["F"].width = 30.0
    sheet.column_dimensions["G"].width = 40.0
    sheet.freeze_panes = "B1"

    for index, transaction in enumerate(transactions, start=1):
        ps = transaction.payments
        payment_type = _to_rich_text(_format_payment_type(p) for p in ps)
        budget = _to_rich_text(_format_budget(p) for p in ps)
        info = f"{transaction.additional_info} {transaction.name}".strip()

        sheet.append(
            [
                add(f"{index:03d}", "left_header"),
                add(transaction.date.strftime("%Y-%m-%d"), "left_header"),
                add(info, "wrap_text"),
                add(transaction.title, "wrap_text"),
                add(transaction.cost, "bad" if transaction.cost < 0 else "nice"),
                add(payment_type, "wrap_text_center"),
                add(budget, "wrap_text_center"),
            ]
        )

    for index in range(2, sheet.max_row + 1):
        sheet.row_dimensions[index].height = 40.0


class RichCostLabel(NamedTuple):
    desc: str
    color: str
    cost: Decimal


def _format_payment_type(payment: Payment):
    pt = payment.payment_type
    at = pt.accountancy_type
    if at:
        desc = at.name
        color = at.color
    else:
        desc = pt.name
        color = pt.color

    return RichCostLabel(desc, color, abs(payment.cost))


def _format_budget(payment: Payment):
    if payment.cost >= 0:
        desc_attr = "description_on_positive"
    else:
        desc_attr = "description_on_negative"

    desc = getattr(payment.budget, desc_attr)
    color = payment.budget.color
    
    if payment.inner_budget:
        if additional_desc := getattr(payment.inner_budget, desc_attr):
            desc += f" {additional_desc}"
            color = payment.inner_budget.color

    return RichCostLabel(desc, color, abs(payment.cost))


def _to_rich_text(labels: Iterable[RichCostLabel]) -> CellRichText:
    accumulator: defaultdict[str, Decimal] = defaultdict(Decimal)
    colors: dict[str, str] = {}
    for label, color, cost in labels:
        accumulator[label] += cost
        colors[label] = color

    match len(accumulator):
        case 0:
            return CellRichText(["-"])
        case 1:
            label = next(iter(accumulator))
            color = colors[label]
            return CellRichText([_color_text(label, color)])
        case _:
            elements = list(chain.from_iterable(
                [
                    _color_text(label, colors[label]),
                    _color_text(f" ({str(cost).replace('.', ',')} zł)", colors[label], bold=True),
                    "\n"
                ]
                for label, cost in accumulator.items()
            ))
            elements.pop()  # Remove last '\n'
            return CellRichText(elements)


def _color_text(s: str, color: str, bold: bool=False):
    font = InlineFont(sz=8, b=bold, rFont='Calibri', color=color)
    return TextBlock(font, s)
