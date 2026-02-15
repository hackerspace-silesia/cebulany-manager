from os import environ

from flask.blueprints import Blueprint
from flask import request, abort

from cebulany.auth import token_required
from cebulany.app import db
from cebulany.accounting_report_parser.pdf import parse
from cebulany.models import Transaction

URL_PREFIX = environ.get('CEBULANY_APP_URL_PREFIX', '')


upload_page = Blueprint('upload_page', 'upload')


@upload_page.route(URL_PREFIX + '/api/transactions/upload', methods=['POST'])
@token_required
def upload_transactions():
    file = request.files.get('file')
    if file is None:
        abort(400, 'No file in args')

    if file.filename == '':
        abort(400, 'No selected file')


    lines = parse(file.stream)
    fill_transactions(lines)

    return 'OK', 200


def fill_transactions(data):
    for record in data:
        transaction_query = (
            db.session.query(Transaction)
            .filter_by(ref_id=record['ref_id'])
        )
        if transaction_query.first() is None:
            db.session.add(Transaction(**record))
        else:
            transaction_query.update(record)
    db.session.commit()