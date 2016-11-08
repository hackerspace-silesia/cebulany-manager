from flask import Flask, send_from_directory
from flask_restful import Api

from flask_security import http_auth_required

from cebulany.auth import init_auth
from cebulany.models import db
from cebulany.resources.transaction import TransactionResource
from cebulany.resources.member import MemberResource, MemberListResource
from cebulany.resources.paid_month import PaidMonthListResource, PaidMonthResource, PaidMonthTableResource
from cebulany.resources.bill import BillListResource, BillResource
from cebulany.resources.donation import DonationListResource, DonationResource
from cebulany.resources.other import OtherListResource, OtherResource
from cebulany.resources.report import report_page

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)
db.init_app(app)

api.add_resource(TransactionResource, '/api/transactions')
api.add_resource(MemberListResource, '/api/members')
api.add_resource(MemberResource, '/api/members/<int:id>')

api.add_resource(PaidMonthListResource, '/api/paid_month')
api.add_resource(PaidMonthTableResource, '/api/paid_month/table')
api.add_resource(PaidMonthResource, '/api/paid_month/<int:id>')
api.add_resource(BillListResource, '/api/bill')
api.add_resource(BillResource, '/api/bill/<int:id>')
api.add_resource(DonationListResource, '/api/donation')
api.add_resource(DonationResource, '/api/donation/<int:id>')
api.add_resource(OtherListResource, '/api/other')
api.add_resource(OtherResource, '/api/other/<int:id>')

app.register_blueprint(report_page)

security = init_auth(app)


@app.route('/')
@http_auth_required
def index():
    return send_from_directory('../spa', 'index.html')


@app.route('/main.css')
@http_auth_required
def css():
    return send_from_directory('../spa', 'main.css')


@app.route('/<path>/<file>')
@http_auth_required
def pseudo_static(path, file):
    return send_from_directory('../spa', '{}/{}'.format(path, file))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
