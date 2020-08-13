from flask_restful import fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import func as sql_func
from itertools import groupby

from cebulany.auth import token_required
from cebulany.models import db, Member, Payment
from cebulany.resources.model import ModelListResource
from cebulany.resources.types import month_type
from cebulany import fields as cebulany_fields
from cebulany.sql_utils import get_year_month_col

parser = RequestParser()
parser.add_argument('member_id', required=True, type=int)
parser.add_argument('transaction_id', required=True, type=int)
parser.add_argument('cost', required=True)
parser.add_argument('date', type=month_type)

query_parser = RequestParser()
query_parser.add_argument('payment_type_id', required=True, type=int)
query_parser.add_argument('month', type=month_type)


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
        dt_col = get_year_month_col(Payment.date)
        args = query_parser.parse_args()
        query = db.session.query(
            Member.id,
            sql_func.sum(Payment.cost),
            sql_func.count(Payment.cost),
            dt_col,
        ).join(Payment, isouter=True).order_by(
            Member.is_active.desc(),
            Member.join_date,
            Member.name,
            dt_col,
        ).filter(
            Payment.payment_type_id == args['payment_type_id'],
        ).group_by(
            Member.id, dt_col
        )

        return [
            {
                'member_id': member_id,
                'months': {
                    month: dict(sum=sum, count=count)
                    for _, sum, count, month in data
                }
            }
            for member_id, data in groupby(query.all(), lambda o: o[0])
        ]
