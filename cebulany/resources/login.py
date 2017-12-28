from flask import abort, current_app as app
from flask_restful.reqparse import RequestParser
from flask_restful.fields import String
from flask_restful import marshal_with, Resource

parser = RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('password', required=True)

fields = {
    'token': String,
}


class LoginResource(Resource):

    @marshal_with(fields)
    def post(self):
        data = parser.parse_args()
        if (
                data['login'] == app.config['CEBULANY_LOGIN'] and
                data['password'] == app.config['CEBULANY_PASSWD']):
            return {'token': app.config['CEBULANY_TOKEN']}
        else:
            abort(400, 'Wrong password or/and login')
