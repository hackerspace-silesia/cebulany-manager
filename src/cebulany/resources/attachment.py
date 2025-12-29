from flask import abort
from flask_restful import fields
from flask_restful.reqparse import RequestParser

from cebulany.models import Attachment
from cebulany.resources.document import resource_fields_base as document_fields
from cebulany.resources.model import ModelListResource, ModelResource


resource_fields = {
    "id": fields.Integer(),
    "transaction_id": fields.Integer(),
    "document_id": fields.Integer(),
    "transaction": fields.Nested(
        {
            "date": fields.DateTime(dt_format="iso8601"),
            "name": fields.String,
            "title": fields.String,
        }
    ),
    "document": fields.Nested(document_fields),
}

parser = RequestParser()
parser.add_argument("transaction_id", required=True, type=int)
parser.add_argument("document_id", required=True, type=int)


class AttachmentListResource(ModelListResource):
    cls = Attachment
    parser = parser
    resource_fields = resource_fields

    def get(self):
        abort(404)


class AttachmentResource(ModelResource):
    cls = Attachment
    parser = parser
    resource_fields = resource_fields

    def put(self, id):
        abort(404)