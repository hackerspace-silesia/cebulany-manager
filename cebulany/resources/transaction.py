from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func
from datetime import datetime

from cebulany import models

dt_type = lambda val: datetime.strptime(val, '%Y-%m-%d')


transaction_parser = RequestParser()
transaction_parser.add_argument('date_start', type=dt_type)
transaction_parser.add_argument('date_end', type=dt_type)
transaction_parser.add_argument('month')
transaction_parser.add_argument('text')
transaction_parser.add_argument('negative')
transaction_parser.add_argument('positive')
transaction_parser.add_argument('cost_le', type=int)
transaction_parser.add_argument('cost_ge', type=int)
transaction_parser.add_argument('ordering')


resource_fields = {
    'send_date': fields.DateTime(dt_format='iso8601'),
    'date': fields.DateTime(dt_format='iso8601'),
    'title': fields.String(),
    'name': fields.String(),
    'address': fields.String(),
    'cost': fields.Price(decimals=2),
    'iban': fields.String(),
}


class TransactionResource(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = transaction_parser.parse_args()
        model = models.Transaction
        query =  model.query
        if args['date_start'] and arg['date_end']:
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

        return query.limit(120).all()

