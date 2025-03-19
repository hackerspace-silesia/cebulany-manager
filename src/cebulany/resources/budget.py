from flask_restful import fields
from flask_restful.reqparse import RequestParser

from cebulany.models import Budget
from cebulany.resources.model import ModelListResource, ModelResource

resource_fields = {
    'id': fields.Integer(),
    'name': fields.String(),
    'color': fields.String(),
    'show_details_in_report': fields.Boolean(),
    'show_count_in_report': fields.Boolean(),
    'description_on_negative': fields.String(),
    'description_on_positive': fields.String(),
}

parser = RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('color', required=True, type=str)
parser.add_argument('show_details_in_report', required=False, type=bool)
parser.add_argument('show_count_in_report', required=False, type=bool)
parser.add_argument('description_on_negative', required=False, type=str)
parser.add_argument('description_on_positive', required=False, type=str)


class BudgetListResource(ModelListResource):
    cls = Budget
    parser = parser
    resource_fields = resource_fields


class BudgetResource(ModelResource):
    cls = Budget
    parser = parser
    resource_fields = resource_fields
