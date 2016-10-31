from flask import Flask
from flask_restful import Api
from cebulany.models import db

from cebulany.resources.transaction import TransactionResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)
db.init_app(app)

api.add_resource(TransactionResource, '/api/transactions')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
