
from flask_restful import fields, marshal_with
from flask_restful.reqparse import RequestParser

from cebulany.auth import token_required
from cebulany.queries.payment_summary import PaymentSummaryQuery
from cebulany.resources.model import ModelListResource

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
query_summary_parser.add_argument('year', type=int, location='args')


class PaymentSummaryResource(ModelListResource):

    @token_required
    @marshal_with(resource_fields)
    def get(self):
        args = query_summary_parser.parse_args()
        year = args['year']

        return {
            'payments': PaymentSummaryQuery.get_payment_data(year),
            'balances': PaymentSummaryQuery.get_balances(year),
            'outstanding_cost': PaymentSummaryQuery.get_outstanding_cost(year),
        }

