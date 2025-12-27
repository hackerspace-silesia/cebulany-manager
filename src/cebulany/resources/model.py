from flask_restful import Resource, marshal, abort
from flask_restful.fields import Raw
from flask_restful.reqparse import RequestParser

from cebulany.auth import token_required
from cebulany.models import db, Base

resource_fields = {}
parser = RequestParser()


class ModelListResource(Resource):
    cls: Base
    parser: RequestParser
    resource_fields: dict[str, Raw]
    method_decorators = [token_required]

    def get_list_query(self):
        return self.cls.query

    def get(self):
        query = self.get_list_query()
        return marshal(query.all(), self.resource_fields)

    def post(self):
        data = self.parser.parse_args()
        obj = self.cls(**data)
        db.session.add(obj)
        db.session.commit()
        return marshal(obj, self.resource_fields), 201


class ModelResourceWithoutDelete(Resource):
    cls: type[Base]
    parser: RequestParser
    resource_fields: dict[str, Raw]
    method_decorators = [token_required]

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
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()

        return marshal(obj, self.resource_fields)


class ModelResource(ModelResourceWithoutDelete):

    def delete(self, id):
        query = self.cls.query.filter_by(id=id)
        is_exists = db.session.query(query.exists()).scalar()
        if not is_exists:
            abort(404)
        query.delete()
        db.session.commit()
        return '', 204
