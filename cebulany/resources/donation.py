from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Donation


class DonationListResource(TransactionTypeListResource):
    cls = Donation
    type_name = 'donation'


class DonationResource(ModelResource):
    cls = Donation
