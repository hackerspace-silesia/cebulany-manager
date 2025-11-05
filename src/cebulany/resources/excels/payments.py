from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from functools import partial
from typing import Iterable, Protocol
import re

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.cell.rich_text import CellRichText

from cebulany.auth import token_required
from cebulany.models import InnerTransfer, db, Payment, PaymentType, Budget, InnerBudget, Transaction
from cebulany.queries import transaction
from cebulany.resources.payment import query_parser
from cebulany.resources.excels.utils import color_text, send_excel, setup_styles, add_cell
from cebulany.resources.excels.blueprint import excel_page, URL_PREFIX
from cebulany.queries.payment import PaymentQuery


@dataclass
class ArgsObj:
    start_date: date
    end_date: date
    payment_type: PaymentType | None
    budget: Budget | None
    inner_budget: InnerBudget | None


class TypeLike(Protocol):
    name: str
    color: str
    cost: Decimal


@excel_page.route(URL_PREFIX + "/payment/")
@token_required
def excel_payment():
    args = query_parser.parse_args()
    args.pop("page", None)

    obj_args = _get_args_obj(args)
    workbook = Workbook()
    setup_styles(workbook, font_size=8)

    payments = list(db.session.execute(PaymentQuery.get_query_list(**args)).scalars())
    payments += list(
        db.session.execute(PaymentQuery.get_inner_transfers(**args)).scalars()
    )
    payments.sort(key=_sort_key)
    sum_query = PaymentQuery.get_query_agg(**args)
    _, total = db.session.execute(sum_query).one()
    _fill_payment_worksheet(workbook.active, payments, obj_args, total)

    if not obj_args.payment_type:
        _fill_type_worksheet(
            workbook.create_sheet("Rodzaj płatności"),
            _enhance_query(PaymentQuery.get_query_group_by_type(**args), PaymentType),
        )
    if not obj_args.budget:
        _fill_type_worksheet(
            workbook.create_sheet("Budżet"),
            _enhance_query(
                PaymentQuery.get_query_group_by_budget(**args).join(Budget), Budget
            ),
        )
    if not obj_args.inner_budget:
        _fill_type_worksheet(
            workbook.create_sheet("Budżet Wewnętrzny"),
            _enhance_query(
                PaymentQuery.get_query_group_by_inner_budget(**args).join(
                    InnerBudget,
                    isouter=True,
                ),
                InnerBudget,
            ),
        )

    return send_excel(workbook, _get_download_name(obj_args))


def _sort_key(o):
    if isinstance(o, InnerTransfer):
        return (o.date, 0) 
    else:
        return (o.transaction.date, o.transaction.line_num)


def _enhance_query(query, model) -> Iterable[TypeLike]:
    name = model.name.label("name")
    color = model.color.label("color")
    query = query.add_columns(name, color).group_by(name, color)
    print(query)
    return db.session.execute(query)


def _get_args_obj(args):
    return ArgsObj(
        start_date=args["start_date"].date(),
        end_date=args["end_date"].date(),
        payment_type=db.session.execute(
            db.select(PaymentType).filter_by(id=args.payment_type_id)
        ).scalar_one_or_none(),
        budget=db.session.execute(
            db.select(Budget).filter_by(id=args.budget_id)
        ).scalar_one_or_none(),
        inner_budget=db.session.execute(
            db.select(InnerBudget).filter_by(id=args.inner_budget_id)
        ).scalar_one_or_none(),
    )


def _get_download_name(args: ArgsObj):
    start = args.start_date.strftime("%Y-%m-%d")
    end = args.end_date.strftime("%Y-%m-%d")
    name = "payments"

    if args.payment_type:
        name += f"_{args.payment_type.name}"
    if args.budget:
        name += f"_{args.budget.name}"
    if args.inner_budget:
        name += f"_{args.inner_budget.name}"

    return re.sub(r"\s+", "_", f"{name}_{start}_{end}.xlsx".replace(" ", "_"))


def add_type_cell(sheet, type: TypeLike | None):
    if type is None:
        return add_cell(sheet, "-", "wrap_text_center")
    cell = add_cell(sheet, type.name or "-", "wrap_text_center")
    cell.font = Font(name="Calibri", bold=True, size=8, color=type.color)
    return cell


def add_type_text_block(type: TypeLike | None, default: str="-"):
    if type is None:
        return color_text(default, bold=True)
    return color_text(type.name, type.color, bold=True)


def _fill_payment_worksheet(sheet, payments: Iterable[Payment | InnerTransfer], args: ArgsObj, total: Decimal):
    add = partial(add_cell, sheet)
    sheet.title = "Zestawienie"
    sheet.append(["", add(f"Zestawienie {_get_title(args)}", "header")])

    header = [
        (add("Lp.", "header"), 5),
        (add("Data", "header"), 10),
        (add("Nazwa", "header"), 30),
    ]
    if not args.payment_type:
        header.append((add("Rodzaj", "header"), 15))
    if not args.budget:
        header.append((add("Budżet", "header"), 15))
    if not args.inner_budget:
        header.append((add("Budżet wew", "header"), 15))

    header += [
        (add("Tytuł", "header"), 60),
        (add("Kwota", "header"), 15),
    ]
    sheet.append([cell for cell, _ in header])

    sheet.merge_cells(
        start_row=1,
        end_row=1,
        start_column=2,
        end_column=len(header),
    )

    for column_count, (_, width) in enumerate(header, start=1):
        letter = get_column_letter(column_count)
        sheet.column_dimensions[letter].width = width

    sheet.freeze_panes = "B1"

    for index, payment in enumerate(payments, start=1):
        row = [
            add(f"{index:03d}", "left_header"),
        ]
        if isinstance(payment, Payment):
            transaction: Transaction = payment.transaction
            name = payment.member.name if payment.member else payment.name
            row += [
                add(transaction.date.strftime("%Y-%m-%d"), "left_header"),
                add(name),
            ]

            if not args.payment_type:
                row.append(add_type_cell(sheet, payment.payment_type))
            if not args.budget:
                row.append(add_type_cell(sheet, payment.budget))
            if not args.inner_budget:
                row.append(add_type_cell(sheet, payment.inner_budget))

            row += [
                add(transaction.title, "wrap_text"),
                add(transaction.cost, "bad" if transaction.cost < 0 else "nice"),
            ]
        elif isinstance(payment, InnerTransfer):
            row += [
                add(payment.date.strftime("%Y-%m-%d"), "left_header"),
                add("Transfer", "wrap_text"),
            ]

            if not args.payment_type:
                row.append(add_type_cell(sheet, None))
            if not args.budget:
                row.append(add_type_cell(sheet, payment.budget))
            if not args.inner_budget:
                row.append(add_type_cell(sheet, None))

            title_cell = CellRichText()
            if payment.from_inner_budget != args.inner_budget:
                title_cell += [
                    color_text(" z "), 
                    add_type_text_block(payment.from_inner_budget),
                ]
            if payment.to_inner_budget != args.inner_budget:
                title_cell += [
                    color_text(" do "), 
                    add_type_text_block(payment.to_inner_budget),
                ]
            row += [
                title_cell,
                add(payment.cost, "bad" if payment.cost < 0 else "nice"),
            ]
        else:
            row.append(add("???", "wrap_text"))

        sheet.append(row)

    sum_row = [
        add("", "wrap_text"),
        add("", "wrap_text"),
        add("RAZEM", "header"),
    ]
    if not args.payment_type:
        sum_row.append(add("", "wrap_text"))
    if not args.budget:
        sum_row.append(add("", "wrap_text"))
    if not args.inner_budget:
        sum_row.append(add("", "wrap_text"))
    sum_row += [
        add("", "wrap_text"),
        add(total, "bad" if total < 0 else "nice"),
    ]
    sheet.append(sum_row)

    for index in range(2, sheet.max_row + 1):
        sheet.row_dimensions[index].height = 20.0


def _get_title(args):
    start = args.start_date.strftime("%Y-%m-%d")
    end = args.end_date.strftime("%Y-%m-%d")
    name = ""

    if args.payment_type:
        name += f" {args.payment_type.name}"
    if args.budget:
        name += f" {args.budget.name}"
    if args.inner_budget:
        name += f" {args.inner_budget.name}"

    return f"{name} {start} - {end}"


def _fill_type_worksheet(sheet, objs: Iterable[TypeLike]):
    add = partial(add_cell, sheet)

    sheet.append([add(sheet.title, "header")])
    sheet.merge_cells(
        start_row=1,
        end_row=1,
        start_column=1,
        end_column=2,
    )

    sheet.append(
        [
            add("Nazwa", "header"),
            add("Kwota", "header"),
        ]
    )

    sheet.column_dimensions["A"].width = 30
    sheet.column_dimensions["B"].width = 10

    for obj in objs:
        print(obj)
        sheet.append(
            [
                add_type_cell(sheet, obj),
                add(obj.cost, "bad" if obj.cost < 0 else "nice"),
            ]
        )

    sheet.freeze_panes = "A2"
