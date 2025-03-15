from datetime import datetime
from functools import partial

from openpyxl import Workbook

from cebulany.auth import token_required
from cebulany.models import Transaction
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
    setup_styles(workbook)
    fill_worksheet(workbook.active, dt, transactions)

    return workbook


def fill_worksheet(sheet, dt: str, transactions: list[Transaction]):
    sheet.title = f"Zestawienie {dt}"
    add = partial(add_cell, sheet)
    sheet.append([add(sheet.title, "header")])
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
        start_column=1,
        end_column=7,
    )

    sheet.column_dimensions['A'].width = 5.0
    sheet.column_dimensions['B'].width = 10.0
    sheet.column_dimensions['C'].width = 60.0
    sheet.column_dimensions['D'].width = 60.0
    sheet.column_dimensions['E'].width = 15.0
    sheet.column_dimensions['F'].width = 40.0
    sheet.column_dimensions['G'].width = 40.0
    sheet.freeze_panes = 'B1'

    for index, transaction in enumerate(transactions, start=1):
        payments = transaction.payments
        payment_type = "; ".join(payment.payment_type.name for payment in payments)
        if len(payments) == 1:
            budget = "; ".join(payment.budget.name for payment in payments)
        else:
            budget = "; ".join(
                f"{payment.budget.name}({payment.cost})" for payment in payments
            )
        sheet.append(
            [
                add(f"{index:03d}", "left_header"),
                add(transaction.date.strftime("%Y-%m-%d"), "left_header"),
                add(transaction.name),
                add(transaction.title),
                add(transaction.cost, "bad" if transaction.cost < 0 else "nice"),
                add(payment_type),
                add(budget),
            ]
        )
