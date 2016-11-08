from flask_security import http_auth_required

from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Donation


class DonationListResource(TransactionTypeListResource):
    method_decorators = [http_auth_required]
    cls = Donation
    type_name = 'donation'


class DonationResource(ModelResource):
    method_decorators = [http_auth_required]
    cls = Donation
