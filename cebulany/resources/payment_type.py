from flask_restful import Resource, fields, marshal, abort
from flask_restful.reqparse import RequestParser
from sqlalchemy.sql.elements import or_

from cebulany.auth import token_required
from cebulany.models import db, Transaction, Payment
from cebulany.resources.model import ModelListResource

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
    'transaction': fields.Nested({
        'date': fields.DateTime(dt_format='iso8601'),
        'name': fields.String,
        'title': fields.String,
    })
}

parser = RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('cost', required=True, type=str)
parser.add_argument('date', required=True, type=str)
parser.add_argument('transaction_id', required=True, type=int)


class PaymentListResource(ModelListResource):
    parser = parser
    resource_fields = resource_fields
    cls = Payment
    type_name = ''

    def get_list_query(self):
        cls = self.cls
        query = cls.query.join(
            cls.transaction
        ).order_by(
            Transaction.date.desc()
        )

        args = query_parser.parse_args()
        if args['name']:
            arg = args['name'].replace('%',r'\%')
            query = query.filter(or_(
                Transaction.name.ilike('%%%s%%' % arg),
                cls.name.ilike('%%%s%%' % arg),
            ))

        return query

    def post(self):
        data, status = super(TransactionTypeListResource, self).post()
        name = data.pop('name')
        iban = db.session.query(Transaction.iban).filter_by(
            id=data['transaction_id']
        ).scalar()
        db.session.query(Transaction).filter_by(
           iban=iban,
        ).update(dict(
            proposed_type_name=name,
            proposed_type_id=
            proposed_type=self.type_name,
        ))
        db.session.commit()

        return data, status
