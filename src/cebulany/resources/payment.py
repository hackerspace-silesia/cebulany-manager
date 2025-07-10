from flask_restful import fields, marshal
from flask_restful.reqparse import RequestParser

from cebulany.auth import token_required
from cebulany.models import db, Transaction, Payment, Suggestion
from cebulany.queries.payment import PaymentQuery
from cebulany.resources.model import ModelListResource, ModelResource
from cebulany.resources.types import dt_type

resource_fields = {
    "id": fields.Integer(),
    "transaction_id": fields.Integer(),
    "name": fields.String(),
    "cost": fields.Price(decimals=2),
    "date": fields.DateTime(dt_format="iso8601"),
    "member_id": fields.Integer(),
    "member": fields.Nested(
        {
            "name": fields.String,
        },
        allow_null=True,
    ),
    "payment_type_id": fields.Integer(),
    "payment_type": fields.Nested(
        {
            "color": fields.String(default="999999"),
            "name": fields.String(default="-"),
        }
    ),
    "budget_id": fields.Integer(),
    "budget": fields.Nested(
        {
            "color": fields.String(default="999999"),
            "name": fields.String(default="-"),
        }
    ),
    "inner_budget_id": fields.Integer(),
    "inner_budget": fields.Nested(
        {
            "color": fields.String(default="999999"),
            "name": fields.String(default="-"),
        },
    ),
    "transaction": fields.Nested(
        {
            "date": fields.DateTime(dt_format="iso8601"),
            "name": fields.String,
            "title": fields.String,
        }
    ),
}

group_resource_fields = {
    "id": fields.Integer(),
    "cost": fields.Price(decimals=2),
}

parser = RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("cost", required=True, type=str)
parser.add_argument("transaction_id", required=True, type=int)
parser.add_argument("payment_type_id", required=True, type=int)
parser.add_argument("budget_id", required=True, type=int)
parser.add_argument("inner_budget_id", required=False, type=int)
parser.add_argument("member_id", required=False, type=int)
parser.add_argument("date", required=False, type=dt_type)


query_parser = RequestParser()
query_parser.add_argument("name", location="args")
query_parser.add_argument("payment_type_id", type=int, location="args")
query_parser.add_argument("budget_id", type=int, location="args")
query_parser.add_argument("inner_budget_id", type=int, location="args")
query_parser.add_argument("member_id", type=int, location="args")
query_parser.add_argument("month", location="args")
query_parser.add_argument("page", type=int, default=1, location="args")


class PaymentListResource(ModelListResource):
    cls = Payment
    parser = parser
    resource_fields = resource_fields
    ITEMS_PER_PAGE = 50

    def get_list_query(self):
        args = query_parser.parse_args()
        page = args.pop("page")
        query = (
            PaymentQuery.get_query_list(**args)
            .limit(self.ITEMS_PER_PAGE)
            .offset(self.ITEMS_PER_PAGE * (page - 1))
        )
        sum_query = PaymentQuery.get_query_agg(**args)
        groups = {
            "payment_type": PaymentQuery.get_query_group_by_type(**args),
            "budget": PaymentQuery.get_query_group_by_budget(**args),
            "inner_budget": PaymentQuery.get_query_group_by_inner_budget(**args),
        }

        return query, sum_query, groups

    @token_required
    def get(self):
        query, sum_query, groups = self.get_list_query()
        count, total = db.session.execute(sum_query).one()
        return {
            "data": [
                marshal(obj, self.resource_fields)
                for obj in db.session.execute(query).scalars()
            ],
            "groups": {
                name: [marshal(obj, group_resource_fields) for obj in db.session.execute(query)]
                for name, query in groups.items()
            },
            "items_per_page": self.ITEMS_PER_PAGE,
            "count": count or 0,
            "total": str(total if total is not None else "-"),
        }

    @token_required
    def post(self):
        data, status = super().post()
        iban = (
            db.session.query(Transaction.iban)
            .filter_by(id=data["transaction_id"])
            .scalar()
        )

        suggestion = db.session.query(Suggestion).get(iban)
        if suggestion is None:
            suggestion = Suggestion(iban=iban)

        suggestion.type_name = data["name"] or ""
        suggestion.type_id = data["payment_type_id"] or None
        suggestion.budget_id = data["budget_id"] or None
        suggestion.inner_budget_id = data["inner_budget_id"] or None
        suggestion.member_id = data["member_id"] or None

        db.session.add(suggestion)
        db.session.commit()

        return data, status


class PaymentResource(ModelResource):
    cls = Payment
    parser = parser
    resource_fields = resource_fields
