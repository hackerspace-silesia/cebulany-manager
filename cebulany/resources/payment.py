from flask_restful import fields
from flask_restful.reqparse import RequestParser
from sqlalchemy.sql.elements import or_

from cebulany.models import db, Transaction, Payment
from cebulany.resources.model import ModelListResource, ModelResource
from cebulany.resources.types import dt_type

resource_fields = {
    'id': fields.Integer(),
    'transaction_id': fields.Integer(),
    'name': fields.String(),
    'cost': fields.Price(decimals=2),
    'date': fields.DateTime(dt_format='iso8601'),
    'member_id': fields.Integer(),
    'member': fields.Nested({
        'name': fields.String,
    }),
    'payment_type_id': fields.Integer(),
    'payment_type': fields.Nested({
        'name': fields.String,
        'color': fields.String,
    }),
    'budget_id': fields.Integer(),
    'budget': fields.Nested({
        'name': fields.String,
        'color': fields.String,
    }),
    'transaction': fields.Nested({
        'date': fields.DateTime(dt_format='iso8601'),
        'name': fields.String,
        'title': fields.String,
    })
}

parser = RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('cost', required=True, type=str)
parser.add_argument('transaction_id', required=True, type=int)
parser.add_argument('payment_type_id', required=True, type=int)
parser.add_argument('budget_id', required=True, type=int)
parser.add_argument('member_id', required=False, type=int)
parser.add_argument('date', required=False, type=dt_type)


query_parser = RequestParser()
query_parser.add_argument('name')
query_parser.add_argument('payment_type_id', type=int)


class PaymentListResource(ModelListResource):
    cls = Payment
    parser = parser
    resource_fields = resource_fields

    def get_list_query(self):
        cls = self.cls
        query = (
            cls.query
            .join(cls.transaction)
            .join(cls.member)
            .order_by(Transaction.date.desc())
            .limit(10)
        )

        args = query_parser.parse_args()
        if args['name']:
            arg = args['name'].replace('%',r'\%')
            query = query.filter(or_(
                Transaction.name.ilike('%%%s%%' % arg),
                cls.name.ilike('%%%s%%' % arg),
            ))
        if args['payment_type_id']:
            query = query.filter(cls.payment_type_id == args['payment_type_id'])

        return query

    def post(self):
        data, status = super(PaymentListResource, self).post()
        name = data['name']
        iban = (
            db.session
            .query(Transaction.iban)
            .filter_by(id=data['transaction_id'])
            .scalar()
        )
        data_to_update = dict(
            proposed_type_name=name,
            proposed_type_id=data['payment_type_id'],
            proposed_budget_id=data['budget_id'],
            proposed_member_id=data['member_id'],
        )
        if data['member_id'] is not None:
            data_to_update['proposed_member_id'] = data['member_id']

        (
            db.session
            .query(Transaction)
            .filter_by(iban=iban)
            .update(data_to_update)
        )
        db.session.commit()

        return data, status


class PaymentResource(ModelResource):
    cls = Payment
    parser = parser
    resource_fields = resource_fields
