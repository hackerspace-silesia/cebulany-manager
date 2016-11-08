from flask_security import http_auth_required
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func
from datetime import datetime

from cebulany.models import db, Member

member_parser = RequestParser()
member_parser.add_argument('name', required=True)
member_parser.add_argument('join_date', required=True)
member_parser.add_argument('is_active', type=bool)

query_parser = RequestParser()
query_parser.add_argument('q')
query_parser.add_argument('limit', type=int)


member_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'join_date': fields.DateTime(dt_format='iso8601'),
    'is_active': fields.Boolean,
}


class MemberListResource(Resource):
    method_decorators = [http_auth_required]

    @marshal_with(member_fields)
    def get(self):
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
        return query.all()

    @marshal_with(member_fields)
    def post(self):
        args = member_parse.parse_args()
        member = Member(**parse.args())
        db.session.add(member)
        db.session.commit()
        return member, 201


class MemberResource(Resource):
    method_decorators = [http_auth_required]

    @marshal_with(member_fields)
    def get(self, id):
        return Member.query.get(id)

    def delete(self, id):
        db.session.delete(Member.query.get(id))
        return 204

