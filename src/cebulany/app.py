from fastapi import FastAPI

app = FastAPI()

# app = Flask(__name__)
# URL_PREFIX = environ.get('CEBULANY_APP_URL_PREFIX', '')
# API_PREFIX = URL_PREFIX + '/api'
# CORS(app)
# api = Api(app)
# db.init_app(app)

# api.add_resource(TransactionsResource, API_PREFIX + '/transactions')
# api.add_resource(TransactionResource, API_PREFIX + '/transactions/<int:id>')
# api.add_resource(MemberListResource, API_PREFIX + '/members')
# api.add_resource(MemberResource, API_PREFIX + '/members/<int:id>')

# api.add_resource(PaymentTableResource, API_PREFIX + '/payment/table')
# api.add_resource(PaymentSummaryResource, API_PREFIX + '/payment/summary')
# api.add_resource(PaymentListResource, API_PREFIX + '/payment/')
# api.add_resource(PaymentResource, API_PREFIX + '/payment/<int:id>')
# api.add_resource(BudgetListResource, API_PREFIX + '/budget/')
# api.add_resource(BudgetResource, API_PREFIX + '/budget/<int:id>')
# api.add_resource(DocumentResource, API_PREFIX + '/document/<int:id>')
# api.add_resource(DocumentSyncResource, API_PREFIX + '/document/sync/<month>')
# api.add_resource(DocumentListResource, API_PREFIX + '/document/')
# api.add_resource(DocumentScoreResource, API_PREFIX + '/document/score')
# api.add_resource(AttachmentListResource, API_PREFIX + '/attachment/')
# api.add_resource(AttachmentResource, API_PREFIX + '/attachment/<int:id>')
# api.add_resource(InnerBudgetListResource, API_PREFIX + '/inner_budget/')
# api.add_resource(InnerBudgetResource, API_PREFIX + '/inner_budget/<int:id>')
# api.add_resource(PaymentTypeListResource, API_PREFIX + '/payment_type/')
# api.add_resource(PaymentTypeResource, API_PREFIX + '/payment_type/<int:id>')
# api.add_resource(AccountancyTypeListResource, API_PREFIX + '/accountancy_type/')
# api.add_resource(AccountancyTypeResource, API_PREFIX + '/accountancy_type/<int:id>')
# api.add_resource(InnerTransferListResource, API_PREFIX + '/inner_transfer/')
# api.add_resource(InnerTransferResource, API_PREFIX + '/inner_transfer/<int:id>')

# api.add_resource(LoginResource, API_PREFIX + '/login')
# api.add_resource(UserListResource, API_PREFIX + '/user/')
# api.add_resource(UserResource, API_PREFIX + '/user/<int:id>')
# api.add_resource(ChangePasswordResource, API_PREFIX + '/user/<int:id>/password')

# app.register_blueprint(report_page)
# app.register_blueprint(upload_page)
# app.register_blueprint(excel_page)


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
