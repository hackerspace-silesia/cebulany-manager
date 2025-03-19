from flask_restful import fields
from flask_restful.reqparse import RequestParser

from cebulany.models import AccountancyType
from cebulany.resources.model import ModelListResource, ModelResource

resource_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'color': fields.String(),
}

parser = RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('color', required=True, type=str)


class AccountancyTypeListResource(ModelListResource):
    cls = AccountancyType
    parser = parser
    resource_fields = resource_fields


class AccountancyTypeResource(ModelResource):
    cls = AccountancyType
    parser = parser
    resource_fields = resource_fields

