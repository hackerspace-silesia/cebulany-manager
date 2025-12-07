from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol

from openpyxl.styles import Font
from openpyxl.cell.rich_text import CellRichText

from cebulany.models import (
    InnerTransfer,
    PaymentType,
    Budget,
    InnerBudget,
)
from cebulany.resources.excels.utils import (
    color_text,
    add_cell,
)

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


def make_inner_transfer_cell(transfer: InnerTransfer, budget, inner_budget, prefix=""):
    title_cell = CellRichText(prefix) if prefix else CellRichText()
    factor = 1
    inner_budget_id = inner_budget.id if inner_budget else None
    if transfer.from_id != inner_budget_id:
        if title_cell:
            title_cell.append(" ")
        title_cell += [
            "z ",
            add_type_text_block(transfer.from_inner_budget),
        ]
    if transfer.to_id != inner_budget_id:
        factor = -1
        if title_cell:
            title_cell.append(" ")
        title_cell += [
            "do ",
            add_type_text_block(transfer.to_inner_budget),
        ]
    budget_id = budget.id if budget else None
    if transfer.budget_id != budget_id:
        if title_cell:
            title_cell.append(" ")
        title_cell += [
            "(",
            add_type_text_block(transfer.budget),
            ")",
        ]

    return title_cell, transfer.cost * factor


def add_type_cell(sheet, type: TypeLike | str | None):
    if isinstance(type, str):
        return add_cell(sheet, type, "wrap_text_center")
    if type is None:
        return add_cell(sheet, "", "wrap_text_center")
    cell = add_cell(sheet, type.name or "-", "wrap_text_center")
    cell.font = Font(name="Calibri", bold=True, size=8, color=type.color)
    return cell


def add_type_text_block(type: TypeLike | None, default: str = "-"):
    if type is None:
        return color_text(default, bold=True)
    return color_text(type.name, type.color, bold=True)