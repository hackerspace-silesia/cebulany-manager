from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func
from datetime import datetime
from decimal import Decimal

from cebulany.auth import token_required
from cebulany.models import db, Transaction
from cebulany.resources.types import dt_type

transaction_parser = RequestParser()
transaction_parser.add_argument('date_start', type=dt_type)
transaction_parser.add_argument('date_end', type=dt_type)
transaction_parser.add_argument('month')
transaction_parser.add_argument('text')
transaction_parser.add_argument('negative')
transaction_parser.add_argument('positive')
transaction_parser.add_argument('cost_le', type=Decimal)
transaction_parser.add_argument('cost_ge', type=Decimal)
transaction_parser.add_argument('ordering')

member_fields = fields.Nested({
    'id': fields.Integer,
    'name': fields.String,
})

payment_type_fields = fields.Nested({
    'id': fields.Integer,
    'color': fields.String,
    'name': fields.String,
})

payment_fields = fields.Nested({
    'name': fields.String,
    'id': fields.Integer,
    'member': member_fields,
    'payment_type': payment_type_fields,
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
        'proposed_type': fields.String,
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
        model = Transaction
        query = model.query
        query_sum = db.session.query(sql_func.sum(model.cost))
        return {
            'transactions': self.filtering_query(query, args).all(),
            'sum': self.filtering_query(query_sum, args).scalar(),
        }

    @staticmethod
    def filtering_query(query, args):
        model = Transaction
        if args['date_start'] and args['date_end']:
            query = query.filter(model.date >= args['date_start'])
            query = query.filter(model.date <= args['date_end'])
        else:
            month = args['month'] or datetime.today().strftime('%Y-%m')
            query = query.filter(
                sql_func.strftime('%Y-%m', model.date) == month
            )
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
                model.main_line.like('%%%s%%' % word.replace('%',r'\%'))
                for word in args['text'].upper().split()
            ))
        if args['ordering']:
            query = query.order_by(*args['ordering'].split(','))
        else:
            query = query.order_by(model.date)
        return query
