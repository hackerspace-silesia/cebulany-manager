from flask_restful import fields, marshal_with
from flask_restful.reqparse import RequestParser

from cebulany.auth import token_required
from cebulany.models import Payment
from cebulany.queries.paid_month import PaidMonthQuery
from cebulany.resources.model import ModelListResource
from cebulany.resources.types import month_type
from cebulany import fields as cebulany_fields

parser = RequestParser()
parser.add_argument('member_id', required=True, type=int)
parser.add_argument('transaction_id', required=True, type=int)
parser.add_argument('cost', required=True)
parser.add_argument('date', type=month_type)

query_parser = RequestParser()
query_parser.add_argument('payment_type_id', required=True, type=int)
query_parser.add_argument('start_year', required=True, type=int)
query_parser.add_argument('end_year', required=True, type=int)

transaction_fields = {
    'date': fields.DateTime(dt_format='iso8601'),
    'name': fields.String,
    'title': fields.String,
}

member_fields = fields.Nested({
    'name': fields.String,
    'id': fields.Integer,
})

month_fields = {
    'sum': fields.Price(2),
    'count': fields.Integer,
}

payment_sum_fields = {
    'member_id': fields.Integer,
    'months': cebulany_fields.Dict(fields.Nested(month_fields)),
}


class PaymentTableResource(ModelListResource):
    cls = Payment
    parser = parser
    resource_fields = payment_sum_fields

    @marshal_with(payment_sum_fields)
    @token_required
    def get(self):
        args = query_parser.parse_args()
        return PaidMonthQuery.get_aggregated_payments(**args)