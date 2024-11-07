from flask import abort, current_app as app
from flask_restful.reqparse import RequestParser
from flask_restful.fields import String, Integer
from flask_restful import marshal_with, Resource
from werkzeug.security import check_password_hash

from cebulany.models import db, User

parser = RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('password', required=True)
parser.add_argument('token', required=True)

fields = {
    'token': String,
    'token_time': Integer,
}


class LoginResource(Resource):

    @marshal_with(fields)
    def post(self):
        data = parser.parse_args()
        user = User.query.filter_by(username=data['login']).first()
        if user is None:
            abort(400, 'Wrong password or/and login')

        if not check_password_hash(user.password_hash, data['password']):
            abort(400, 'Wrong password or/and login')

        if app.config['TOTP_SUPPORT']:
            if not user.verify_totp(data.token):
                abort(400, 'Wrong token from 2FA')

        user.generate_token()
        user.update_token_time()
        db.session.add(user)
        db.session.commit()

        return {
            'token': f'{user.id}:{user.token}',
            'token_time': app.config['TOKEN_TIME'],
        }
