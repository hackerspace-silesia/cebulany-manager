from flask import Flask, send_from_directory, safe_join
from flask_cors import CORS
from flask_restful import Api

from cebulany.models import db
from cebulany.resources.transaction import TransactionResource
from cebulany.resources.member import MemberResource, MemberListResource
from cebulany.resources.paid_month import PaymentTableResource
from cebulany.resources.report import report_page
from cebulany.resources.upload import upload_page
from cebulany.resources.excels import excel_page
from cebulany.resources.login import LoginResource
from cebulany.resources.budget import BudgetListResource, BudgetResource
from cebulany.resources.payment_type import PaymentTypeListResource
from cebulany.resources.payment_type import PaymentTypeResource
from cebulany.resources.payment import PaymentListResource, PaymentResource
from cebulany.resources.payment_summary import PaymentSummaryResource

from os import environ

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['TOKEN_TIME'] = int(environ.get('CEBULANY_TOKEN_TIME', '600'))
app.config['TOTP_SUPPORT'] = environ.get('TOTP_SUPPORT', 'yes') == 'yes'
app.config['APP_NAME'] = environ.get('CEBULANY_APP_NAME', 'cebulany manager')
URL_PREFIX = environ.get('CEBULANY_APP_URL_PREFIX', '')
API_PREFIX = URL_PREFIX + '/api'
CORS(app)
api = Api(app)
db.init_app(app)

api.add_resource(TransactionResource, API_PREFIX + '/transactions')
api.add_resource(MemberListResource, API_PREFIX + '/members')
api.add_resource(MemberResource, API_PREFIX + '/members/<int:id>')

api.add_resource(PaymentTableResource, API_PREFIX + '/payment/table')
api.add_resource(PaymentSummaryResource, API_PREFIX + '/payment/summary')
api.add_resource(PaymentListResource, API_PREFIX + '/payment/')
api.add_resource(PaymentResource, API_PREFIX + '/payment/<int:id>')
api.add_resource(BudgetListResource, API_PREFIX + '/budget/')
api.add_resource(BudgetResource, API_PREFIX + '/budget/<int:id>')
api.add_resource(PaymentTypeListResource, API_PREFIX + '/payment_type/')
api.add_resource(PaymentTypeResource, API_PREFIX + '/payment_type/<int:id>')

api.add_resource(LoginResource, API_PREFIX + '/login')

app.register_blueprint(report_page)
app.register_blueprint(upload_page)
app.register_blueprint(excel_page)


@app.route(URL_PREFIX or '/')
@app.route(URL_PREFIX + '/index.html')
@app.route(URL_PREFIX + '/')
def index():
    return send_from_directory('../spa/dist', 'index.html')


@app.route(URL_PREFIX + '/static/<mod>/<filename>')
def pseudo_static(mod, filename):
    return send_from_directory('../spa/dist/static/%s' % mod, filename)


if app.debug:
    @app.after_request
    def add_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST, PATCH, PUT, DELETE, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
