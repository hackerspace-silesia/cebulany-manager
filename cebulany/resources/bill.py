from cebulany.resources.model import ModelResource, TransactionTypeListResource
from cebulany.models import Bill


class BillListResource(TransactionTypeListResource):
    cls = Bill
    type_name = 'bill'
