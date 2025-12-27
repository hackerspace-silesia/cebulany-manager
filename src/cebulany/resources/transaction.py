from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser

from cebulany.queries.transaction import TransactionQuery
from cebulany.auth import token_required
from cebulany.models import Transaction
from cebulany.resources.model import ModelResourceWithoutDelete
from cebulany.resources.types import dt_type

query_parser = RequestParser()
query_parser.add_argument("date_start", type=dt_type, location="args", required=True)
query_parser.add_argument("date_end", type=dt_type, location="args", required=True)
query_parser.add_argument("text", location="args")
query_parser.add_argument("ordering", location="args")
query_parser.add_argument("member_id", type=int, location="args")

transaction_parser = RequestParser()
transaction_parser.add_argument("additional_info", required=False, type=str)


member_fields = fields.Nested(
    {
        "id": fields.Integer,
        "name": fields.String,
    }
)

member_fields_optional = fields.Nested(
    {
        "id": fields.Integer,
        "name": fields.String,
    },
    allow_null=True,
)

payment_type_fields = fields.Nested(
    {
        "id": fields.Integer,
        "color": fields.String(default="999999"),
        "name": fields.String(default="-"),
    }
)

budget_fields = fields.Nested(
    {
        "id": fields.Integer,
        "color": fields.String(default="999999"),
        "name": fields.String(default="-"),
    }
)

inner_budget_fields = fields.Nested(
    {
        "id": fields.Integer,
        "color": fields.String(default="999999"),
        "name": fields.String(default="-"),
    }
)

payment_fields = fields.Nested(
    {
        "name": fields.String,
        "id": fields.Integer,
        "member_id": fields.Integer(),
        "payment_type_id": fields.Integer(),
        "inner_budget_id": fields.Integer(),
        "budget_id": fields.Integer(),
        "member": member_fields,
        "payment_type": payment_type_fields,
        "budget": budget_fields,
        "inner_budget": inner_budget_fields,
        "date": fields.DateTime(dt_format="iso8601"),
        "cost": fields.Price(decimals=2),
    }
)

suggestion_fields = fields.Nested(
    {
        "name": fields.String(attribute="type_name"),
        "member": member_fields_optional,
        "budget_id": fields.Integer,
        "inner_budget_id": fields.Integer(default=None),
        "payment_type_id": fields.Integer(attribute="type_id"),
        "member_id": fields.String,
    },
    allow_null=True,
)

resource_fields = {
    "id": fields.Integer(),
    "date": fields.DateTime(dt_format="iso8601"),
    "title": fields.String(),
    "name": fields.String(),
    "cost": fields.Price(decimals=2),
    "iban": fields.String(),
    "payments": fields.List(payment_fields),
    "additional_info": fields.String(),
    "suggestion": suggestion_fields,
}

resource_list_fields = {
    "transactions": fields.List(fields.Nested(resource_fields)),
    "sum": fields.Price(decimals=2),
}


class TransactionsResource(Resource):

    @marshal_with(resource_list_fields)
    @token_required
    def get(self):
        args = query_parser.parse_args()
        transactions = TransactionQuery.get_transactions(
            date_range=(args["date_start"], args["date_end"]),
            text_like=args["text"],
            ordering=args["ordering"],
            member_id=args["member_id"],
        )
        return {
            "transactions": transactions,
            "sum": sum(transaction.cost for transaction in transactions),
        }


class TransactionResource(ModelResourceWithoutDelete):
    cls = Transaction
    parser = transaction_parser
    resource_fields = resource_fields