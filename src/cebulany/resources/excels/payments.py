from functools import partial
from typing import Iterable

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from cebulany.auth import token_required
from cebulany.models import db, Payment, Transaction
from cebulany.resources.payment import query_parser
from cebulany.resources.excels.utils import send_excel, setup_styles, add_cell
from cebulany.resources.excels.blueprint import excel_page, URL_PREFIX
from cebulany.queries.payment import PaymentQuery


@excel_page.route(URL_PREFIX + "/payment/")
@token_required
def excel_payment():
    args = query_parser.parse_args()
    args.pop("page", None)
    query = PaymentQuery.get_query_list(**args)
    sum_query = PaymentQuery.get_query_agg(**args)
    groups = {
        "payment_type": PaymentQuery.get_query_group_by_type(**args),
        "budget": PaymentQuery.get_query_group_by_budget(**args),
        "inner_budget": PaymentQuery.get_query_group_by_inner_budget(**args),
    }
    inner_transfers = PaymentQuery.get_inner_transfers(**args)
    download_name = f"wtf.xlsx"

    workbook = Workbook()
    setup_styles(workbook, font_size=8)

    fill_payment_worksheet(workbook.active, db.session.execute(query).scalars(), args)

    return send_excel(workbook, download_name)


def fill_payment_worksheet(sheet, payments: Iterable[Payment], args):
    sheet.title = f"WTF"
    add = partial(add_cell, sheet)
    sheet.append(["", add(sheet.title, "header")])

    header = [
        add("Lp.", "header"),
        add("Data", "header"),
        add("Nazwa", "header"),
    ]
    if not args["payment_type_id"]:
        header.append(add("Typ", "header"))
    if not args["budget_id"]:
        header.append(add("Budżet", "header"))
    if not args["inner_budget_id"]:
        header.append(add("Budżet wew", "header"))

    header += [
        add("Tytuł", "header"),
        add("Kwota", "header"),
    ]
    sheet.append(header)

    sheet.merge_cells(
        start_row=1,
        end_row=1,
        start_column=2,
        end_column=len(header),
    )

    column_count = 1
    def resize_next_column(w):
        nonlocal column_count
        letter = get_column_letter(column_count)
        sheet.column_dimensions[letter].width = w
        column_count += 1

    resize_next_column(5)
    resize_next_column(10)
    resize_next_column(30)
    if not args["payment_type_id"]:
        resize_next_column(15)
    if not args["budget_id"]:
        resize_next_column(15)
    if not args["inner_budget_id"]:
        resize_next_column(15)
    resize_next_column(60)
    resize_next_column(15)

    sheet.freeze_panes = "B1"

    def add_type_cell(type):
        if type is None:
            return add("-", "wrap_text_center")
        cell = add(type.name or "-", "wrap_text_center")
        cell.font = Font(name="Calibri", bold=True, size=8, color=type.color)
        return cell

    for index, payment in enumerate(payments, start=1):
        # payment_type = _to_rich_text(_format_payment_type(p) for p in ps)
        # budget = _to_rich_text(_format_budget(p) for p in ps)
        # info = f"{transaction.additional_info} {transaction.name}".strip()
        transaction: Transaction = payment.transaction
        name = payment.member.name if payment.member else payment.name
        row = [
            add(f"{index:03d}", "left_header"),
            add(transaction.date.strftime("%Y-%m-%d"), "left_header"),
            add(name),
        ]

        if not args["payment_type_id"]:
            row.append(add_type_cell(payment.payment_type))
        if not args["budget_id"]:
            row.append(add_type_cell(payment.budget))
        if not args["inner_budget_id"]:
            row.append(add_type_cell(payment.inner_budget))

        row += [
            add(transaction.title, "wrap_text"),
            add(transaction.cost, "bad" if transaction.cost < 0 else "nice"),
        ]

        sheet.append(row)

    for index in range(2, sheet.max_row + 1):
        sheet.row_dimensions[index].height = 20.0
