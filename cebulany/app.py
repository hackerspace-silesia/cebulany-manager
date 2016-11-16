from flask import Flask, send_from_directory
from flask_restful import Api
from cebulany.models import db

from cebulany.resources.transaction import TransactionResource
from cebulany.resources.member import MemberResource, MemberListResource
from cebulany.resources.paid_month import PaidMonthListResource
from cebulany.resources.bill import BillListResource
from cebulany.resources.donation import DonationListResource
from cebulany.resources.other import OtherListResource 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)
db.init_app(app)

api.add_resource(TransactionResource, '/api/transactions')
api.add_resource(PaidMonthListResource, '/api/paid_month')
api.add_resource(MemberListResource, '/api/members')
api.add_resource(MemberResource, '/api/members/<int:id>')
api.add_resource(BillListResource, '/api/bill')
api.add_resource(DonationListResource, '/api/donation')
api.add_resource(OtherListResource, '/api/other')


@app.route('/')
def index():
    return send_from_directory('../spa', 'index.html')


@app.route('/main.css')
def css():
    return send_from_directory('../spa', 'main.css')


@app.route('/<path>/<file>')
def pseudo_static(path, file):
    return send_from_directory('../spa', '{}/{}'.format(path, file))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
