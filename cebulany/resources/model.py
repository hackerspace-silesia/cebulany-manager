from flask_restful import Resource, fields, marshal, abort
from flask_restful.reqparse import RequestParser

from cebulany.models import db, Transaction

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


class ModelListResource(Resource):
    cls = None
    parser = parser
    resource_fields = resource_fields

    def get_list_query(self):
        return self.cls.query.all()

    def get(self):
        return marshal(self.get_list_query(), self.resource_fields)

    def post(self):
        data = self.parser.parse_args()
        obj = self.cls(**data)
        db.session.add(obj)
        db.session.commit()
        return marshal(obj, self.resource_fields), 201


class TransactionTypeListResource(ModelListResource):

    def get_list_query():
        return cls.query.join(cls.transaction).order_by(Transaction.date.desc)

    def post(self):
        data, status = super(TransactionTypeListResource, self).post()
        name = data.pop('name')
        transaction_name = db.session.query(Transaction.name).filter_by(
            id=data['transaction_id']
        ).scalar()
        db.session.query(Transaction).filter_by(
            name=transaction_name,
        ).update(dict(proposed_type_name=name)) 
        db.session.commit()

        return data, status



class ModelResource(Resource):
    cls = None
    parser = parser
    resource_fields = resource_fields

    def get(self, pk):
        obj = self.cls.query.get(pk)
        if obj is None:
            abort(404)
        return marshal(obj, self.resource_fields)

    def put(self, pk):
        query = self.cls.query.filter_by(id=pk)
        is_exists = query.exists()
        if not is_exists:
            abort(404)
        return marshal(obj, self.resource_fields)

    def delete(self, pk):
        query = self.cls.query.filter_by(id=pk)
        is_exists = query.exists()
        if not is_exists:
            abort(404)
        query.delete()
        return 204
