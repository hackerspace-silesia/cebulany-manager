from datetime import date
from decimal import Decimal

from flask_restful import fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import func as sql_func

from cebulany.auth import token_required
from cebulany.models import db, Transaction, Payment
from cebulany.resources.model import ModelListResource
from cebulany.sql_utils import get_year_col

resource_fields = {
    'payments': fields.List(fields.Nested({
        'cost': fields.Price(decimals=2),
        'is_positive': fields.Boolean(),
        'payment_type_id': fields.Integer(),
        'budget_id': fields.Integer(),
    })),
    'balances': fields.Nested({
        'curr_start_year': fields.Price(decimals=2),
        'curr_end_year': fields.Price(decimals=2),
        'prev_start_year': fields.Price(decimals=2),
        'prev_end_year': fields.Price(decimals=2),
        'diff_start_year': fields.Price(decimals=2),
        'diff_end_year': fields.Price(decimals=2),
        'diff_prev_start_year': fields.Price(decimals=2),
        'diff_prev_end_year': fields.Price(decimals=2),
    }),
    'outstanding_cost': fields.Price(decimals=2),
}

query_summary_parser = RequestParser()
query_summary_parser.add_argument('year', type=int)


def year_col(col, year: int):
    return get_year_col(col) == str(year)


def get_start_year_day(year: int) -> date:
    return date(year, 1, 1)


def get_end_year_day(year: int) -> date:
    return date(year, 12, 31)


class PaymentSummaryResource(ModelListResource):

    @token_required
    @marshal_with(resource_fields)
    def get(self):
        args = query_summary_parser.parse_args()
        year = args['year']

        return {
            'payments': self._get_payment_data(year),
            'balances': self._get_balances(year),
            'outstanding_cost': self._get_outstanding_cost(year),
        }

    @staticmethod
    def _get_payment_data(year: int):
        cls = Payment
        is_positive_col = Payment.cost > 0
        query = (
            db.session
            .query(
                sql_func.sum(cls.cost),
                cls.payment_type_id,
                cls.budget_id,
                is_positive_col,
            )
            .join(cls.transaction)
            .filter(year_col(Transaction.date, year))
            .group_by(
                cls.payment_type_id,
                cls.budget_id,
                is_positive_col,
            )
        )

        return [
            {
                'budget_id': budget_id,
                'payment_type_id': payment_type_id,
                'is_positive': is_positive,
                'cost': cost,
            }
            for cost, payment_type_id, budget_id, is_positive in query
        ]

    @staticmethod
    def _get_outstanding_cost(year: int):
        payments_cost = (
            db.session
            .query(sql_func.sum(Payment.cost))
            .join(Payment.transaction)
            .filter(year_col(Transaction.date, year))
            .scalar()
        ) or Decimal('0.00')
        transaction_cost = (
            db.session
            .query(sql_func.sum(Transaction.cost))
            .filter(year_col(Transaction.date, year))
            .scalar()
        ) or Decimal('0.00')

        return abs(transaction_cost - payments_cost)

    @staticmethod
    def _get_balance(day: date):
        return (
            db.session
            .query(sql_func.sum(Payment.cost))
            .join(Payment.transaction)
            .filter(Transaction.date <= day)
            .scalar()
        ) or Decimal('0.00')

    @classmethod
    def _get_balances(cls, year: int):
        last_year = year - 1
        last_last_year = year - 2

        curr_start_year = cls._get_balance(get_start_year_day(year))
        curr_end_year = cls._get_balance(get_end_year_day(year))
        prev_start_year = cls._get_balance(get_start_year_day(last_year))
        prev_end_year = cls._get_balance(get_end_year_day(last_year))
        prev_prev_start_year = cls._get_balance(get_start_year_day(last_last_year))
        prev_prev_end_year = cls._get_balance(get_end_year_day(last_last_year))

        return {
            'curr_start_year': curr_start_year,
            'curr_end_year': curr_end_year,
            'prev_start_year': prev_start_year,
            'prev_end_year': prev_end_year,
            'diff_start_year': curr_start_year - prev_start_year,
            'diff_end_year': curr_end_year - prev_end_year,
            'diff_prev_start_year': prev_start_year - prev_prev_start_year,
            'diff_prev_end_year': prev_end_year - prev_prev_end_year,
        }
