from flask_security import http_auth_required

from cebulany.resources.model import ModelResource
from cebulany.models import Other


class OtherResource(ModelResource):
    method_decorators = [http_auth_required]

    cls = Other

