from os import environ

from flask.blueprints import Blueprint
from flask import request, abort

from cebulany.auth import token_required
from cebulany.export_data import fill_transactions
from cebulany.pdf import parse

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
