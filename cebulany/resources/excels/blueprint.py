from os import environ

from flask import Blueprint

URL_PREFIX = environ.get('CEBULANY_APP_URL_PREFIX', '') + '/api/excel'

excel_page = Blueprint('excel_page', 'excel')
