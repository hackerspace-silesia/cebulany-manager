from flask_restful import fields
from flask_restful.reqparse import RequestParser
from cebulany.resources.model import ModelResource, ModelListResource

from cebulany.models import Member
from cebulany.resources.types import dt_type

member_parser = RequestParser()
member_parser.add_argument('name', required=True)
member_parser.add_argument('join_date', required=True, type=dt_type)
member_parser.add_argument('is_active', required=True, type=bool)

query_parser = RequestParser()
query_parser.add_argument('q')
query_parser.add_argument('limit', type=int)


member_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'join_date': fields.DateTime(dt_format='iso8601'),
    'is_active': fields.Boolean,
}


class MemberListResource(ModelListResource):
    cls = Member
    resource_fields = member_fields
    parser = member_parser

    def get_list_query(self):
        parse_args = query_parser.parse_args()
        query = Member.query.order_by(Member.name)
        query_arg = parse_args['q']
        limit_arg = parse_args['limit']
        if query_arg:
            args = query_arg.split()
            query = query.filter(*[
                Member.name.ilike('%%%s%%' % arg.replace('%',r'\%'))
                for arg in args
            ])
        if limit_arg is not None:
            query = query.limit(limit_arg)
        return query


class MemberResource(ModelResource):
    cls = Member
    parser = member_parser
    resource_fields = member_fields

