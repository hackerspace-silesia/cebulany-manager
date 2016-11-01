from cebulany.resources.model import ModelResource
from cebulany.models import Bill


class BillResource(ModelResource):
    cls = Bill
