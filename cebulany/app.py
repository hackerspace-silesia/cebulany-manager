from flask import Flask, send_from_directory, safe_join
from flask_restful import Api
from cebulany.models import db
from cebulany.resources.payment_summary import PaymentSummaryResource

from cebulany.resources.transaction import TransactionResource
from cebulany.resources.member import MemberResource, MemberListResource
from cebulany.resources.paid_month import PaymentTableResource
from cebulany.resources.report import report_page
from cebulany.resources.upload import upload_page
from cebulany.resources.login import LoginResource
from cebulany.resources.budget import BudgetListResource, BudgetResource
from cebulany.resources.payment_type import PaymentTypeListResource
from cebulany.resources.payment_type import PaymentTypeResource
from cebulany.resources.payment import PaymentListResource, PaymentResource

from os import environ

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['TOKEN_TIME'] = int(environ.get('CEBULANY_TOKEN_TIME', '600'))
app.config['APP_NAME'] = environ.get('CEBULANY_APP_NAME', 'cebulany manager')
api = Api(app)
db.init_app(app)

api.add_resource(TransactionResource, '/api/transactions')
api.add_resource(MemberListResource, '/api/members')
api.add_resource(MemberResource, '/api/members/<int:id>')

api.add_resource(PaymentTableResource, '/api/payment/table')
api.add_resource(PaymentSummaryResource, '/api/payment/summary')
api.add_resource(PaymentListResource, '/api/payment/')
api.add_resource(PaymentResource, '/api/payment/<int:id>')
api.add_resource(BudgetListResource, '/api/budget/')
api.add_resource(BudgetResource, '/api/budget/<int:id>')
api.add_resource(PaymentTypeListResource, '/api/payment_type/')
api.add_resource(PaymentTypeResource, '/api/payment_type/<int:id>')

api.add_resource(LoginResource, '/api/login')

app.register_blueprint(report_page)
app.register_blueprint(upload_page)


@app.route('/')
def index():
    return send_from_directory('../spa/dist', 'index.html')


@app.route('/static/<mod>/<filename>')
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
