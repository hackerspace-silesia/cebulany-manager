from sqlalchemy import or_, union_all
from sqlalchemy.orm import aliased

from cebulany.models import Transaction, Payment, InnerTransfer, InnerBudget, db
from cebulany.sql_utils import get_year_month_col, get_year_col


class PaymentQuery:

    @classmethod
    def get_query_agg(cls, **kw):
        payment_query = cls._get_query_list(
            db.func.count().label('count'),
            db.func.sum(Payment.cost).label('cost'),
            **kw,
        )

        borrowed_transfer_query = cls._subsub(InnerTransfer.from_id, db.select(
            db.func.count().label('count'),
            db.func.sum(-InnerTransfer.cost).label('cost'),
        ), kw)

        lent_transfer_query = cls._subsub(InnerTransfer.to_id, db.select(
            db.func.count().label('count'),
            db.func.sum(InnerTransfer.cost).label('cost'),
        ), kw)

        union_query = union_all(
            payment_query, 
            borrowed_transfer_query, 
            lent_transfer_query
        ).subquery("total")

        return (
            db.select(
                db.func.sum(union_query.c.count).label('count'), 
                db.func.sum(union_query.c.cost).label('cost'),
            )
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
        payment_query = cls._get_query_list(
            Payment.budget_id.label('id'),
            (Payment.cost).label('cost'),
            **kw,
        )

        borrowed_transfer_query = cls._subsub(InnerTransfer.from_id, db.select(
            InnerTransfer.budget_id.label('id'),
            (-InnerTransfer.cost).label('cost'),
        ), kw)

        lent_transfer_query = cls._subsub(InnerTransfer.to_id, db.select(
            InnerTransfer.budget_id.label('id'),
            (InnerTransfer.cost).label('cost'),
        ), kw)

        union_query = union_all(
            payment_query, 
            borrowed_transfer_query, 
            lent_transfer_query
        ).subquery("total")

        query = (
            db.select(
                union_query.c.id.label('id'), 
                db.func.sum(union_query.c.cost).label('cost'),
            )
            .group_by(union_query.c.id)
        )
        
        return query

    @classmethod
    def get_query_group_by_inner_budget(cls, **kw):
        payment_query = cls._get_query_list(
            Payment.inner_budget_id.label('id'),
            (Payment.cost).label('cost'),
            **kw,
        )

        borrowed_transfer_query = cls._subsub(InnerTransfer.from_id, db.select(
            InnerTransfer.from_id.label('id'),
            (-InnerTransfer.cost).label('cost'),
        ), kw)

        lent_transfer_query = cls._subsub(InnerTransfer.to_id, db.select(
            InnerTransfer.to_id.label('id'),
            (InnerTransfer.cost).label('cost'),
        ), kw)

        union_query = union_all(
            payment_query, 
            borrowed_transfer_query, 
            lent_transfer_query
        ).subquery("total")

        query = (
            db.select(
                union_query.c.id.label('id'), 
                db.func.sum(union_query.c.cost).label('cost'),
            )
            .group_by(union_query.c.id)
        )
        
        return query

    @staticmethod
    def _subsub(inner_budget_col, query, kw):
        budget_id = kw.get("budget_id")
        if budget_id == -1:
            query = query.filter(InnerTransfer.budget_id == None)
        elif budget_id is not None:
            query = query.filter(InnerTransfer.budget_id == budget_id)

        inner_budget_id = kw.get("inner_budget_id")
        if inner_budget_id == -1:
            query = query.filter(inner_budget_col == None)
        elif inner_budget_id is not None:
            query = query.filter(inner_budget_col == inner_budget_id)

        if start := kw.get("start_date"):
            query = query.filter(InnerTransfer.date >= start)
        if end := kw.get("end_date"):
            query = query.filter(InnerTransfer.date <= end)
        return query

    @classmethod
    def get_query_list(cls, **kw):
        return cls._get_query_list(Payment, **kw).order_by(Transaction.date.desc())

    @classmethod
    def get_inner_transfers(cls, **kw):
        query = (
            db.select(InnerTransfer)
            .join(InnerTransfer.budget)
            .join(aliased(InnerBudget), InnerTransfer.to_inner_budget, isouter=True)
            .join(aliased(InnerBudget), InnerTransfer.from_inner_budget, isouter=True)
        )
        budget_id = kw.get("budget_id")
        if budget_id == -1:
            query = query.filter(InnerTransfer.budget_id == None)
        elif budget_id is not None:
            query = query.filter(InnerTransfer.budget_id == budget_id)

        inner_budget_id = kw.get("inner_budget_id")
        if inner_budget_id == -1:
            query = query.filter(or_(
                InnerTransfer.from_id == None,
                InnerTransfer.to_id == None,
            ))
        elif inner_budget_id is not None:
            query = query.filter(or_(
                InnerTransfer.from_id == inner_budget_id,
                InnerTransfer.to_id == inner_budget_id,
            ))

        if start := kw.get("start_date"):
            query = query.filter(InnerTransfer.date >= start)
        if end := kw.get("end_date"):
            query = query.filter(InnerTransfer.date <= end)
        
        return query


    @classmethod
    def _get_query_list(cls, *fields, name=None, payment_type_id=None, budget_id=None, inner_budget_id=None, start_date=None, end_date=None, member_id=None):
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
        query = cls._filter_by_date(query, start_date, end_date)
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
        if budget_id == -1:
            return query.filter(Payment.inner_budget_id == None)
        return query.filter(Payment.inner_budget_id == budget_id)

    @staticmethod
    def _filter_by_date(query, start, end):
        if start:
            query = query.filter(Transaction.date >= start)
        if end:
            query = query.filter(Transaction.date <= end)
        return query

    @staticmethod
    def _filter_by_member_id(query, member_id):
        if member_id is None:
            return query
        return query.filter(Payment.member_id == member_id)