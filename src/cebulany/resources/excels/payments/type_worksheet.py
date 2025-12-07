from functools import partial
from typing import Iterable

from cebulany.models import (
    db,
    InnerTransfer,
    Budget,
    InnerBudget,
)
from cebulany.resources.excels.utils import add_cell

from .common import TypeLike, add_type_cell, make_inner_transfer_cell


def enhance_query(query, model) -> Iterable[TypeLike]:
    name = model.name.label("name")
    color = model.color.label("color")
    query = query.add_columns(name, color).group_by(name, color)
    return db.session.execute(query)


def types_to_rows(sheet, query: Iterable[TypeLike]):
    for obj in query:
        yield [
            add_type_cell(sheet, obj),
            add_cell(sheet, obj.cost, "bad" if obj.cost < 0 else "nice"),
        ]


def inner_transfers_to_rows(
    sheet,
    budget: Budget | None,
    inner_budget: InnerBudget | None,
    transfers: Iterable[InnerTransfer],
):
    for obj in transfers:
        title_cell, cost = make_inner_transfer_cell(
            obj, budget, inner_budget, "Transfer"
        )
        yield [
            add_cell(sheet, title_cell, "wrap_text_center"),
            add_cell(sheet, cost, "bad" if cost < 0 else "nice"),
        ]


def fill_type_worksheet(sheet, *objs: Iterable):
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

    for rows in objs:
        for row in rows:
            sheet.append(row)

    sheet.freeze_panes = "A2"