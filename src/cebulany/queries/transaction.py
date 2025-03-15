from datetime import datetime

from sqlalchemy import or_, and_
from sqlalchemy.orm import contains_eager

from cebulany.models import Transaction
from cebulany.sql_utils import get_year_month_col


class TransactionQuery:

    @classmethod
    def get_transactions(
        cls,
        date_range: tuple[datetime, datetime] | None = None,
        month: str | None = None,
        text_like: str | None = None,
        ordering: str | None = None,
    ):
        model = Transaction
        query = (
            model.query.outerjoin(model.payments)
            .options(contains_eager(model.payments))
            .order_by(model.date)
        )
        if date_range:
            date_start, date_end = date_range
            query = query.filter(model.date >= date_start)
            query = query.filter(model.date <= date_end)
        elif month:
            query = query.filter(get_year_month_col(model.date) == month)
        else:
            raise Exception("!! :(")

        if text_like:
            query = query.filter(
                and_(
                    or_(
                        model.name.ilike("%%%s%%" % word.replace("%", r"\%")),
                        model.title.ilike("%%%s%%" % word.replace("%", r"\%")),
                    )
                    for word in text_like.split()
                )
            )
        if ordering:
            query = query.order_by(ordering)
        else:
            query = query.order_by(model.date)

        return query.all()
