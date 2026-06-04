from fastapi.routing import APIRouter
from pydantic import BaseModel

from cebulany.deps import SessionDep
from cebulany.models import Budget

from ._sql_utils import get_all, get_by_id

router = APIRouter(prefix="/budget")

class BudgetModel(BaseModel):
    id: int
    name: str
    color: str
    show_details_in_report: bool
    show_count_in_report: bool
    description_on_negative: str
    description_on_positive: str


@router.get("/")
def list(session: SessionDep) -> list[BudgetModel]:
    return await get_all[Budget, BudgetModel](session)


@router.get("/{id:int}")
def get(session: SessionDep) -> BudgetModel:
    return await get_by_id[Budget, BudgetModel](session)


class BudgetListResource(ModelListResource):
    cls = Budget
    parser = parser
    resource_fields = resource_fields


class BudgetResource(ModelResource):
    cls = Budget
    parser = parser
    resource_fields = resource_fields
