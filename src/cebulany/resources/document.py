from datetime import date, datetime
from decimal import Decimal
from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from flask import abort

from cebulany.auth import token_required
from cebulany.google_drive import find_files_by_date, update_file
from cebulany.models import Document, db
from cebulany.queries.document import DocumentQuery
from cebulany.resources.types import dt_type, month_type

resource_fields_base = {
    "id": fields.Integer(),
    "filename": fields.String(),
    "accounting_record": fields.String(),
    "accounting_date": fields.DateTime(dt_format="iso8601"),
    "company_name": fields.String(),
    "description": fields.String(),
    "price": fields.Fixed(decimals=2),
}

resource_fields = {
    **resource_fields_base,
    "link": fields.String(),
    "date": fields.DateTime(dt_format="iso8601"),
}

resource_fields_score = {
    **resource_fields_base,
    "score": fields.Float(),
}

parser = RequestParser()
parser.add_argument("filename", required=True)
parser.add_argument("accounting_record", required=False, type=str)
parser.add_argument("accounting_date", required=False, type=dt_type)
parser.add_argument("description", required=False, type=str)
parser.add_argument("company_name", required=False, type=str)
parser.add_argument("price", required=False, type=Decimal)

query_parser = RequestParser()
query_parser.add_argument("parent", required=False, type=str, location="args")
query_parser.add_argument("name", required=False, type=str, location="args")

query_score_parser = RequestParser()
query_score_parser.add_argument("parent", required=True, type=str, location="args")
query_score_parser.add_argument("date", required=True, type=dt_type, location="args")
query_score_parser.add_argument("price", required=True, type=Decimal, location="args")
query_score_parser.add_argument("name", required=False, type=str, location="args")


def sync_document(item, document: Document):
    document.filename = item["name"]
    document.link = item.get("webViewLink", "")
    document.link = f"https://drive.google.com/file/d/{item["id"]}/preview"
    document.date = datetime.fromisoformat(item["modifiedTime"])
    document.mime_type = item.get("mimeType")
    document.description = item.get("description")

    properties = item.get("properties", {})
    document.accounting_record = properties.get("accounting_record")
    document.company_name = properties.get("company_name")
    document.price = (
        Decimal(raw_price)
        if (raw_price := properties.get("price"))
        else None
    )
    document.accounting_date = (
        date.fromisoformat(raw_date)
        if (raw_date := properties.get("accounting_date"))
        else None
    )


class DocumentListResource(Resource):

    def get(self):
        args = query_parser.parse_args()
        query = DocumentQuery.get_documents(
            parent=args.parent,
            name_like=args.name,
        )
        return marshal(query.all(), resource_fields)


class DocumentScoreResource(Resource):

    def get(self):
        args = query_score_parser.parse_args()
        query = DocumentQuery.get_score(
            parent=args.parent,
            dt=args.date.date(),
            price=args.price,
            name_like=args.name,
        )
        return marshal(query.all(), resource_fields_score)


class DocumentResource(Resource):
    method_decorators = [token_required]

    def put(self, id):
        document = Document.query.get(id)
        if document is None:
            abort(404)


        data = parser.parse_args()
        item = update_file(
            id=document.google_id,
            filename=data["filename"],
            accounting_record=data["accounting_record"],
            accounting_date=data["accounting_date"] and data["accounting_date"].date(),
            description=data["description"] or "",
            company_name=data["company_name"],
            price=data["price"],
        )
        sync_document(item, document)
        db.session.add(document)
        db.session.commit()

        return marshal(document, resource_fields)


class DocumentSyncResource(Resource):
    method_decorators = [token_required]

    def post(self, month: str):
        dt = month_type(month)
        for item in find_files_by_date(dt.year, dt.month):
            google_id = item["id"]
            document = Document.query.filter_by(google_id=google_id).first()
            if document is None:
                document = Document(
                    google_id=google_id,
                    google_parent_id=item["parents"][-1],
                    parent=f"{dt.year:04d}-{dt.month:02d}",
                )
            sync_document(item, document)
            db.session.add(document)
        db.session.commit()

        return "", 204
