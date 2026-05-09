from os import environ
from typing import Iterable

from flask.blueprints import Blueprint
from flask import request, abort

from cebulany.auth import token_required
from cebulany.app import db
from cebulany.accounting_report_parser.pdf import Record, parse
from cebulany.accounting_report_parser.zip import load_pdf_zip
from cebulany.models import Transaction

URL_PREFIX = environ.get('CEBULANY_APP_URL_PREFIX', '')


upload_page = Blueprint('upload_page', 'upload')


@upload_page.route(URL_PREFIX + '/api/transactions/upload', methods=['POST'])
@token_required
def upload_transactions():
    file = request.files.get('file')
    if file is None:
        abort(400, 'No file in args')

    filename = file.filename
    if not filename:
        abort(400, 'No selected file')

    if filename.endswith(".zip"):
        records = load_pdf_zip(file.stream)
    elif filename.endswith(".pdf"):
        records = parse(file.stream)
    else:
        abort(400, "unknown media")

    fill_transactions(records)
    return 'OK', 200


def fill_transactions(records: Iterable[Record]):
    for record in records:
        transaction_query = (
            db.session.query(Transaction)
            .filter_by(ref_id=record['ref_id'])
        )
        if transaction_query.first() is None:
            db.session.add(Transaction(**record))
        else:
            transaction_query.update(record)
    db.session.commit()