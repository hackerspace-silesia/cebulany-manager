from flask_security import http_auth_required

from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Bill


class BillListResource(TransactionTypeListResource):
    method_decorators = [http_auth_required]
    cls = Bill
    type_name = 'bill'


class BillResource(ModelResource):
    method_decorators = [http_auth_required]
    cls = Bill
