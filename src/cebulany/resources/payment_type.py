from flask_restful import fields
from flask_restful.reqparse import RequestParser

from cebulany.models import PaymentType
from cebulany.resources.model import ModelListResource, ModelResource
from cebulany.resources.types import boolean

resource_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'color': fields.String(),
    'has_members': fields.Boolean(),
    'show_details_in_report': fields.Boolean(),
    'show_count_in_report': fields.Boolean(),
}

parser = RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('color', required=True, type=str)
parser.add_argument('has_members', required=False, type=bool)
parser.add_argument('show_details_in_report', required=False, type=bool)
parser.add_argument('show_count_in_report', required=False, type=bool)


query_parser = RequestParser()
query_parser.add_argument('has_members', type=boolean, location='args')


class PaymentTypeListResource(ModelListResource):
    cls = PaymentType
    parser = parser
    resource_fields = resource_fields

    def get_list_query(self):
        cls = self.cls
        query = super(PaymentTypeListResource, self).get_list_query()

        args = query_parser.parse_args()
        has_members = args['has_members']
        if has_members is not None:
            query = query.filter(cls.has_members == has_members)

        return query


class PaymentTypeResource(ModelResource):
    cls = PaymentType
    parser = parser
    resource_fields = resource_fields

