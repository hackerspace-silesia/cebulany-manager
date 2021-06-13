from flask_restful import fields, marshal
from flask_restful.reqparse import RequestParser

from cebulany.auth import token_required
from cebulany.models import db, Transaction, Payment
from cebulany.queries.payment import PaymentQuery
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
    }, allow_null=True),
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
query_parser.add_argument('budget_id', type=int)
query_parser.add_argument('member_id', type=int)
query_parser.add_argument('month')
query_parser.add_argument('page', type=int, default=1)


class PaymentListResource(ModelListResource):
    cls = Payment
    parser = parser
    resource_fields = resource_fields
    ITEMS_PER_PAGE = 50

    def get_list_query(self):
        args = query_parser.parse_args()
        page = args.pop('page')
        query = PaymentQuery.get_query_list(**args)

        return query, page

    @token_required
    def get(self):
        query, page = self.get_list_query()
        return {
            'data': marshal(
                query
                .limit(self.ITEMS_PER_PAGE)
                .offset(self.ITEMS_PER_PAGE * (page - 1))
                .all(),
                self.resource_fields,
            ),
            'items_per_page': self.ITEMS_PER_PAGE,
            'count': query.count(),
        }

    @token_required
    def post(self):
        data, status = super().post()
        name = data['name']
        iban = (
            db.session
            .query(Transaction.iban)
            .filter_by(id=data['transaction_id'])
            .scalar()
        )
        data_to_update = dict(
            proposed_type_name=name,
            proposed_type_id=data['payment_type_id'] or None,
            proposed_budget_id=data['budget_id'] or None,
            proposed_member_id=data['member_id'] or None,
        )

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
