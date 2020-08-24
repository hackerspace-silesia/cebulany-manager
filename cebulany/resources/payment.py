from flask_restful import fields, marshal
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_

from cebulany.auth import token_required
from cebulany.models import db, Transaction, Payment
from cebulany.resources.model import ModelListResource, ModelResource
from cebulany.resources.types import dt_type
from cebulany.sql_utils import get_year_month_col, get_year_col

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
        cls = self.cls
        query = (
            cls.query
            .join(cls.transaction)
            .join(cls.member, isouter=True)
            .join(cls.payment_type)
            .join(cls.budget)
            .order_by(Transaction.date.desc())
        )

        args = query_parser.parse_args()
        if args['name']:
            arg = args['name'].replace('%', r'\%')
            query = query.filter(or_(
                Transaction.name.ilike('%%%s%%' % arg),
                cls.name.ilike('%%%s%%' % arg),
            ))
        if args['payment_type_id'] is not None:
            query = query.filter(cls.payment_type_id == args['payment_type_id'])
        if args['budget_id'] is not None:
            query = query.filter(cls.budget_id == args['budget_id'])
        if args['month'] is not None:
            if '-' in args['month']:
                query = query.filter(
                    get_year_month_col(cls.date) == args['month']
                )
            else:
                query = query.filter(
                    get_year_col(cls.date) == args['month']
                )

        if args['member_id'] is not None:
            query = query.filter(cls.member_id == args['member_id'])

        return query, args['page']

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
