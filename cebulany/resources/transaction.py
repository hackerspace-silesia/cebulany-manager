from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func
from datetime import datetime
from decimal import Decimal

from cebulany import models
from cebulany.models import db

dt_type = lambda val: datetime.strptime(val, '%Y-%m-%d')

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

simple_fields = fields.Nested({
    'name': fields.String(),
    'cost': fields.Price(decimals=2),
})

paid_month_fields = fields.Nested({
    'member': fields.String(),
    'date': fields.DateTime(dt_format='iso8601'),
    'cost': fields.Price(decimals=2),
})

resource_fields = {
    'transactions': fields.List(fields.Nested({
        'id': fields.Integer(),
        'send_date': fields.DateTime(dt_format='iso8601'),
        'date': fields.DateTime(dt_format='iso8601'),
        'title': fields.String(),
        'name': fields.String(),
        'address': fields.String(),
        'cost': fields.Price(decimals=2),
        'iban': fields.String(),
        'donations': fields.List(simple_fields),
        'bills': fields.List(simple_fields),
        'others': fields.List(simple_fields),
        'paidmonths': fields.List(paid_month_fields),
    })),
    'sum': fields.Price(decimals=2),
}


class TransactionResource(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = transaction_parser.parse_args()
        model = models.Transaction
        query = model.query
        query_sum = db.session.query(sql_func.sum(model.cost))
        return {
            'transactions': self.filtering_query(query, args).all(),
            'sum': self.filtering_query(query_sum, args).scalar(),
        }

    @staticmethod
    def filtering_query(query, args):
        model = models.Transaction
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
        return query
