from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func, extract as sql_extract
from datetime import datetime
from itertools import groupby

from cebulany.models import db, Member, PaidMonth, Transaction
from cebulany.resources.model import ModelListResource, ModelResource
from cebulany.resources.types import month_type

parser = RequestParser()
parser.add_argument('member_id', required=True, type=int)
parser.add_argument('transaction_id', required=True, type=int)
parser.add_argument('cost', required=True)
parser.add_argument('date', type=month_type)

paid_month_fields = {
    'date': fields.DateTime(dt_format='iso8601'),
    'transaction_id': fields.Integer,
    'cost': fields.Price,
}

paid_month_sum_fields = {
    'member_id': fields.Integer,
    'months': fields.List(fields.Nested({
        'month': fields.String,
        'sum': fields.Price,
    }))
}


class PaidMonthListResource(ModelListResource):
    cls = PaidMonth
    parser = parser
    resource_fields = paid_month_fields

    @marshal_with(paid_month_sum_fields)
    def get(self):
        dt_col = sql_func.strftime('%Y-%m', PaidMonth.date)
        query = db.session.query(
            Member.id,
            sql_func.sum(PaidMonth.cost),
            dt_col,
        ).join(Member.months, isouter=True).order_by(
            Member.is_active.desc(),
            Member.join_date,
            Member.name,
            dt_col,
        ).group_by(
            Member.id, dt_col
        )

        return [
            {
                'member_id': member_id,
                'months': [
                    dict(sum=sum, month=month)
                    for member_id, sum, month in data
                ]
            }
            for member_id, data in groupby(query.all(), lambda o: o[0])
        ]

    def post(self):
        data, status = super(PaidMonthListResource, self).post()
        args = self.parser.parse_args()
        # update proposed_member_id in every transaction who has this same name
        transaction_name = db.session.query(Transaction.name).filter_by(
            id=data['transaction_id'],
        ).scalar()
        query_trans = db.session.query(Transaction).filter_by(name=transaction_name)
        query_trans.update(dict(
            proposed_member_id=args['member_id'],
            proposed_type='paid_month',
        ))
        db.session.commit()
        return data, status


class PaidMonthResource(ModelResource):
    cls = PaidMonth
    resource_fields = paid_month_fields
    parser = parser

