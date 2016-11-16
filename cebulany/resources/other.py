from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Other


class OtherListResource(TransactionTypeListResource):
    cls = Other

