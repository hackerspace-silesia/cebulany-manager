from flask_restful import fields, Resource, marshal_with
from flask_restful.reqparse import RequestParser

from cebulany.auth import token_required
from cebulany.models import User, db
from cebulany.resources.model import ModelListResource, ModelResource

resource_fields = {
    'id': fields.Integer(),
    'username': fields.String(),
    'totp_uri': fields.String(),
    # 'is_active': fields.Boolean(),
}

parser = RequestParser()
parser.add_argument('username', required=True)
# parser.add_argument('is_active', required=False, type=bool)

create_parser = RequestParser()
create_parser.add_argument('username', required=True)
create_parser.add_argument('password', required=True)

password_parser = RequestParser()
password_parser.add_argument('password', required=True)


class UserListResource(ModelListResource):
    cls = User
    parser = parser
    resource_fields = resource_fields


class UserResource(ModelResource):
    cls = User
    parser = create_parser
    resource_fields = resource_fields


class ChangePasswordResource(Resource):

    @token_required
    @marshal_with({})
    def post(self, id):
        data = password_parser.parse_args()
        user = User.query.get(id)
        user.password = data['password']
        user.generate_token()  # generate new token - previous session should be cancelled
        user.update_token_time()

        db.session.add(user)
        db.session.commit()

        return {}
