from flask_restful import fields
from flask_restful.reqparse import RequestParser

from cebulany.models import InnerTransfer
from cebulany.resources.model import ModelListResource, ModelResource
from cebulany.resources.types import dt_type

resource_fields = {
    "id": fields.Integer(),
    "date": fields.DateTime(dt_format="iso8601"),
    "cost": fields.Price(decimals=2),
    "budget_id": fields.Integer(),
    "from_id": fields.Integer(default=None),
    "to_id": fields.Integer(default=None),
}

parser = RequestParser()
parser.add_argument("date", required=True, type=dt_type)
parser.add_argument("cost", required=True, type=str)
parser.add_argument("budget_id", required=True, type=int)
parser.add_argument("from_id", required=True, type=int)
parser.add_argument("to_id", required=True, type=int)

query_parser = RequestParser()
query_parser.add_argument("start_date", required=True, type=dt_type, location="args")
query_parser.add_argument("end_date", required=True, type=dt_type, location="args")


class InnerTransferListResource(ModelListResource):
    cls = InnerTransfer
    parser = parser
    resource_fields = resource_fields

    def get_list_query(self):
        args = query_parser.parse_args()
        return (
            self.cls.query
            .filter(InnerTransfer.date >= args.start_date)
            .filter(InnerTransfer.date <= args.end_date)
            .order_by("id", "date")
        )


class InnerTransferResource(ModelResource):
    cls = InnerTransfer
    parser = parser
    resource_fields = resource_fields
