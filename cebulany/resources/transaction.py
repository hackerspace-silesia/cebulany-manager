from datetime import datetime
from decimal import Decimal

from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func
from sqlalchemy.orm import contains_eager

from cebulany.auth import token_required
from cebulany.models import Transaction, Payment
from cebulany.resources.types import dt_type
from cebulany.sql_utils import get_year_month_col

transaction_parser = RequestParser()
transaction_parser.add_argument('date_start', type=dt_type, location='args')
transaction_parser.add_argument('date_end', type=dt_type, location='args')
transaction_parser.add_argument('month', location='args')
transaction_parser.add_argument('text', location='args')
transaction_parser.add_argument('negative', location='args')
transaction_parser.add_argument('positive', location='args')
transaction_parser.add_argument('cost_le', type=Decimal, location='args')
transaction_parser.add_argument('cost_ge', type=Decimal, location='args')
transaction_parser.add_argument('ordering', location='args')
transaction_parser.add_argument('member_id', type=int, location='args')


member_fields = fields.Nested({
    'id': fields.Integer,
    'name': fields.String,
})

payment_type_fields = fields.Nested({
    'id': fields.Integer,
    'color': fields.String,
    'name': fields.String,
})

budget_fields = fields.Nested({
    'id': fields.Integer,
    'color': fields.String,
    'name': fields.String,
})

payment_fields = fields.Nested({
    'name': fields.String,
    'id': fields.Integer,
    'member': member_fields,
    'payment_type': payment_type_fields,
    'budget': budget_fields,
    'date': fields.DateTime(dt_format='iso8601'),
    'cost': fields.Price(decimals=2),
})


resource_fields = {
    'transactions': fields.List(fields.Nested({
        'id': fields.Integer(),
        'date': fields.DateTime(dt_format='iso8601'),
        'title': fields.String(),
        'name': fields.String(),
        'cost': fields.Price(decimals=2),
        'iban': fields.String(),
        'payments': fields.List(payment_fields),
        'proposed_member_id': fields.String,
        'proposed_type_name': fields.String,
        'proposed_type_id': fields.Integer,
        'proposed_budget_id': fields.Integer,
        'proposed_member': member_fields,
    })),
    'sum': fields.Price(decimals=2),
}


class TransactionResource(Resource):

    @marshal_with(resource_fields)
    @token_required
    def get(self):
        args = transaction_parser.parse_args()
        transactions = self.get_transactions(args)
        return {
            'transactions': transactions,
            'sum': sum(transaction.cost for transaction in transactions),
        }

    @staticmethod
    def get_transactions(args):
        model = Transaction
        query = (
            Transaction.query
            .outerjoin(model.payments)
            .options(contains_eager(model.payments))
        )
        if args['date_start'] and args['date_end']:
            query = query.filter(model.date >= args['date_start'])
            query = query.filter(model.date <= args['date_end'])
        elif args['month']:
            query = query.filter(
                get_year_month_col(model.date) == args['month']
            )
        elif not args['member_id']:
            month = datetime.today().strftime('%Y-%m')
            query = query.filter(
                get_year_month_col(model.date) == month
            )
        if args['member_id']:
            query = query.filter(Payment.member_id == args['member_id'])
        if args['negative'] == 't':
            query = query.filter(model.cost < 0)
        if args['positive'] == 't':
            query = query.filter(model.cost > 0)
        if args['cost_le']:
            query = query.filter(model.cost <= args['cost_le'])
        if args['cost_ge']:
            query = query.filter(model.cost >= args['cost_ge'])
        if args['text']:
            query = query.filter(or_(
                model.main_line.like('%%%s%%' % word.replace('%', r'\%'))
                for word in args['text'].upper().split()
            ))
        if args['ordering']:
            query = query.order_by(*args['ordering'].split(','))
        else:
            query = query.order_by(model.date)

        return query.all()
