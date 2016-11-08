from flask_security import http_auth_required

from cebulany.resources.model import ModelResource
from cebulany.models import Donation


class DonationResource(ModelResource):
    method_decorators = [http_auth_required]

    cls = Donation
