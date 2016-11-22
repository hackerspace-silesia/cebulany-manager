from flask_restful import Resource, fields, marshal, abort
from flask_restful.reqparse import RequestParser

from cebulany.models import db, Transaction

resource_fields = {
    'id': fields.Integer(),
    'transaction_id': fields.Integer(),
    'name': fields.String(),
    'cost': fields.Price(decimals=2),
    'transaction': fields.Nested({
        'date': fields.DateTime(dt_format='iso8601'),
    })
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
    type_name = ''

    def get_list_query(self):
        cls = self.cls
        return cls.query.join(
            cls.transaction
        ).order_by(
            Transaction.date.desc()
        ).all()

    def post(self):
        data, status = super(TransactionTypeListResource, self).post()
        name = data.pop('name')
        transaction_name = db.session.query(Transaction.name).filter_by(
            id=data['transaction_id']
        ).scalar()
        db.session.query(Transaction).filter_by(
            name=transaction_name,
        ).update(dict(
            proposed_type_name=name,
            proposed_type=self.type_name,
        )) 
        db.session.commit()

        return data, status



class ModelResource(Resource):
    cls = None
    parser = parser
    resource_fields = resource_fields

    def get(self, id):
        obj = self.cls.query.get(id)
        if obj is None:
            abort(404)
        return marshal(obj, self.resource_fields)

    def put(self, id):
        obj = self.cls.query.get(id)
        if obj is None:
            abort(404)

        data = self.parser.parse_args()
        obj.__dict__.update(**data)
        db.session.add(obj)
        db.session.commit()
        return marshal(obj, self.resource_fields)

    def delete(self, id):
        query = self.cls.query.filter_by(id=id)
        is_exists = db.session.query(query.exists()).scalar()
        if not is_exists:
            abort(404)
        query.delete()
        db.session.commit()
        return '', 204
