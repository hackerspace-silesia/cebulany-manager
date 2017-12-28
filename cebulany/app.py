from flask import Flask, send_from_directory, safe_join
from flask_restful import Api
from cebulany.models import db

from cebulany.resources.transaction import TransactionResource
from cebulany.resources.member import MemberResource, MemberListResource
from cebulany.resources.paid_month import (
    PaidMonthListResource,
    PaidMonthResource,
    PaidMonthTableResource,
)
from cebulany.resources.bill import BillListResource, BillResource
from cebulany.resources.donation import DonationListResource, DonationResource
from cebulany.resources.other import OtherListResource, OtherResource
from cebulany.resources.report import report_page
from cebulany.resources.upload import upload_page

from os import environ

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
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
app.register_blueprint(upload_page)


@app.route('/')
def index():
    return send_from_directory('../spa/dist', 'index.html')


@app.route('/static/<mod>/<filename>')
def pseudo_static(mod, filename):
    return send_from_directory('../spa/dist/static/%s' % mod, filename)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
