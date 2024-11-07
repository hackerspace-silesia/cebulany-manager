from itertools import groupby

from sqlalchemy import func as sql_func

from cebulany.models import db, Member, Payment
from cebulany.sql_utils import get_year_month_col, get_year_col


class PaidMonthQuery:

    @classmethod
    def get_aggregated_payments(cls, payment_type_id, start_year, end_year):
        query = cls._get_query(payment_type_id, start_year, end_year)
        return cls._aggregate(query)

    @staticmethod
    def _get_query(payment_type_id, start_year, end_year):
        dt_col = get_year_month_col(Payment.date)
        year_col = get_year_col(Payment.date)
        print(start_year, end_year, year_col)
        return db.session.query(
            Member.id,
            sql_func.sum(Payment.cost),
            sql_func.count(Payment.cost),
            dt_col,
        ).join(
            Payment, isouter=True
        ).order_by(
            Member.is_active.desc(),
            Member.join_date,
            Member.name,
            dt_col,
        ).filter(
            Payment.payment_type_id == payment_type_id,
            #year_col >= start_year,
            #year_col <= end_year,
        ).group_by(
            Member.id,
            dt_col,
        )

    @staticmethod
    def _aggregate(query):
        return [
            {
                'member_id': member_id,
                'months': {
                    month: dict(sum=total, count=count)
                    for _, total, count, month in data
                }
            }
            for member_id, data in groupby(query.all(), lambda o: o[0])
        ]
