from flask_security import http_auth_required

from cebulany.resources.model import ModelResource
from cebulany.models import Bill


class BillResource(ModelResource):
    method_decorators = [http_auth_required]

    cls = Bill
