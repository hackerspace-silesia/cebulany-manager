from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser

from cebulany.models import db

resource_fields = {
    'id': fields.Integer(),
    'transaction_id': fields.Integer(),
    'name': fields.String(),
    'cost': fields.Price(decimals=2),
}

parser = RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('cost', required=True, type=str)
parser.add_argument('transaction_id', required=True, type=int)


class ModelResource(Resource):
    cls = None
    parser = parser
    resource_fields = resource_fields

    def get(self):
        return marshal(self.cls.query.all(), self.resource_fields)

    def post(self):
        bill = self.cls(**self.parser.parse_args())
        db.session.add(bill)
        db.session.commit()
        return marshal(bill, self.resource_fields), 201

