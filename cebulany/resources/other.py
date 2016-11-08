from flask_security import http_auth_required

from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Other


class OtherListResource(TransactionTypeListResource):
    method_decorators = [http_auth_required]
    cls = Other
    type_name = 'other'


class OtherResource(ModelResource):
    method_decorators = [http_auth_required]
    cls = Other
