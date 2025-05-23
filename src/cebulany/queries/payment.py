from sqlalchemy import or_

from cebulany.models import Transaction, Payment, db
from cebulany.sql_utils import get_year_month_col, get_year_col


class PaymentQuery:

    @classmethod
    def get_query_agg(cls, **kw):
        return cls._get_query_list(
            db.func.count(),
            db.func.sum(Payment.cost),
            **kw,
        )

    @classmethod
    def get_query_group_by_type(cls, **kw):
        return cls._get_query_list(
            Payment.payment_type_id.label('id'),
            db.func.sum(Payment.cost).label('cost'),
            **kw,
        ).group_by(Payment.payment_type_id)

    @classmethod
    def get_query_group_by_budget(cls, **kw):
        return cls._get_query_list(
            Payment.budget_id.label('id'),
            db.func.sum(Payment.cost).label('cost'),
            **kw,
        ).group_by(Payment.budget_id)

    @classmethod
    def get_query_group_by_inner_budget(cls, **kw):
        return cls._get_query_list(
            Payment.inner_budget_id.label('id'),
            db.func.sum(Payment.cost).label('cost'),
            **kw,
        ).group_by(Payment.inner_budget_id)

    @classmethod
    def get_query_list(cls, **kw):
        return cls._get_query_list(Payment, **kw).order_by(Transaction.date.desc())

    @classmethod
    def _get_query_list(cls, *fields, name=None, payment_type_id=None, budget_id=None, inner_budget_id=None, month=None, member_id=None):
        query = (
            db.select(*fields)
            .join(Payment.transaction)
            .join(Payment.member, isouter=True)
            .join(Payment.payment_type)
            .join(Payment.budget)
            .join(Payment.inner_budget, isouter=True)
        )

        query = cls._filter_by_name(query, name)
        query = cls._filter_by_payment_type(query, payment_type_id)
        query = cls._filter_by_budget_id(query, budget_id)
        query = cls._filter_by_inner_budget_id(query, inner_budget_id)
        query = cls._filter_by_month(query, month)
        query = cls._filter_by_member_id(query, member_id)

        return query

    @staticmethod
    def _filter_by_name(query, name):
        if not name:
            return query
        arg = name.replace('%', r'\%')
        return query.filter(or_(
            Transaction.name.ilike(f'%%{arg}%%'),
            Payment.name.ilike(f'%%{arg}%%'),
        ))

    @staticmethod
    def _filter_by_payment_type(query, payment_type_id):
        if payment_type_id is None:
            return query
        return query.filter(Payment.payment_type_id == payment_type_id)

    @staticmethod
    def _filter_by_budget_id(query, budget_id):
        if budget_id is None:
            return query

        return query.filter(Payment.budget_id == budget_id)

    @staticmethod
    def _filter_by_inner_budget_id(query, budget_id):
        if budget_id is None:
            return query
        return query.filter(Payment.inner_budget_id == budget_id)

    @staticmethod
    def _filter_by_month(query, month):
        if month is None:
            return query
        if '-' in month:
            return query.filter(
                get_year_month_col(Transaction.date) == month
            )
        return query.filter(
            get_year_col(Transaction.date) == month
        )

    @staticmethod
    def _filter_by_member_id(query, member_id):
        if member_id is None:
            return query
        return query.filter(Payment.member_id == member_id)