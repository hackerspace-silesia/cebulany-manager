from functools import partial

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
        one_payment = len(ps) == 1
        payment_type = CellRichText([format_payment_type(p, not one_payment) for p in ps])
        payment_type.style = "wrap_text"
        budget = CellRichText([format_budget(p, not one_payment) for p in ps])
        budget.style = "wrap_text"

        sheet.append(
            [
                add(f"{index:03d}", "left_header"),
                add(transaction.date.strftime("%Y-%m-%d"), "left_header"),
                add(f"{transaction.additional_info} {transaction.name}", "wrap_text"),
                add(transaction.title, "wrap_text"),
                add(transaction.cost, "bad" if transaction.cost < 0 else "nice"),
                add(payment_type, "wrap_text"),
                add(budget, "wrap_text"),
            ]
        )

    for index in range(2, sheet.max_row + 1):
        sheet.row_dimensions[index].height = 40.0


def format_payment_type(payment: Payment, with_cost=False):
    pt = payment.payment_type
    at = pt.accountancy_type
    if at:
        desc = at.name
        color = at.color
    else:
        desc = pt.name
        color = pt.color

    if with_cost:
        desc = f"{desc}({payment.cost} zł)"

    return _color_text(desc + "; ", color)


def format_budget(payment: Payment, with_cost=False):
    if payment.cost >= 0:
        desc = payment.budget.description_on_positive
    else:
        desc = payment.budget.description_on_negative

    if not desc:
        return desc

    if with_cost:
        desc = f"{desc}({payment.cost} zł)"

    return _color_text(desc + "; ", payment.budget.color)


def _color_text(s, color):
    font = InlineFont(sz=8, b=True, rFont='Calibri', color=color)
    return TextBlock(font, s)
