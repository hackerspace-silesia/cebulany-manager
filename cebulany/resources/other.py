from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Other


class OtherListResource(TransactionTypeListResource):
    cls = Other
    type_name = 'other'


class OtherResource(ModelResource):
    cls = Other
