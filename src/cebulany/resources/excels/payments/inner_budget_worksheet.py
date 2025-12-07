from cebulany.queries.payment import PaymentQuery
from cebulany.models import InnerBudget

from .type_worksheet import fill_type_worksheet, types_to_rows, enhance_query



def fill_inner_budget_worksheet(sheet, args): 
    fill_type_worksheet(
        sheet,
        types_to_rows(
            sheet,
            enhance_query(
                PaymentQuery.get_query_group_by_inner_budget(**args).join(
                    InnerBudget
                ),
                InnerBudget,
            ),
        ),
    )