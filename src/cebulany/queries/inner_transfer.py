from sqlalchemy import or_
from sqlalchemy.orm import aliased, Bundle

from cebulany.models import Budget, InnerBudget, InnerTransfer, db


class InnerTransferQuery:

    @classmethod
    def get_agg_query(cls, start_date, end_date, inner_budget_id=None, budget_id=None, from_id=None, to_id=None):
        budget = Bundle("budget", Budget.id, Budget.name, Budget.color)
        to_alias = aliased(InnerBudget, name="to_inner_budget")
        from_alias = aliased(InnerBudget, name="from_inner_budget")
        to_inner_budget = Bundle("to_inner_budget", to_alias.id, to_alias.name, to_alias.color)
        from_inner_budget = Bundle("from_inner_budget", from_alias.id, from_alias.name, from_alias.color)
        query = (
            db.select(
                InnerTransfer.budget_id,
                InnerTransfer.from_id,
                InnerTransfer.to_id,
                budget,
                to_inner_budget,
                from_inner_budget,
                db.func.sum(InnerTransfer.cost).label('cost'),
            )
            .group_by(
                InnerTransfer.budget_id,
                InnerTransfer.from_id,
                InnerTransfer.to_id,
                budget,
                to_inner_budget,
                from_inner_budget,
            )
            .join(InnerTransfer.budget)
            .join(to_alias, InnerTransfer.to_inner_budget)
            .join(from_alias, InnerTransfer.from_inner_budget)
            .filter(
                InnerTransfer.date >= start_date,
                InnerTransfer.date <= end_date,
            )
            .order_by(
                InnerTransfer.budget_id,
                InnerTransfer.to_id,
                InnerTransfer.from_id,
            )
        )
        if inner_budget_id is not None:
            query = query.filter(
                or_(
                    InnerTransfer.from_id == inner_budget_id,
                    InnerTransfer.to_id == inner_budget_id,
                )
            )
        if budget_id is not None:
            query = query.filter(InnerTransfer.budget_id == budget_id)
        if from_id is not None:
            query = query.filter(InnerTransfer.from_id == from_id)
        if to_id is not None:
            query = query.filter(InnerTransfer.to_id == to_id)

        return query
