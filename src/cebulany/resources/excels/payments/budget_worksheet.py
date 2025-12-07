from cebulany.queries.payment import PaymentQuery
from cebulany.models import Budget

from .type_worksheet import fill_type_worksheet, types_to_rows, enhance_query



def fill_budget_worksheet(sheet, args): 
    fill_type_worksheet(
        sheet,
        types_to_rows(
            sheet,
            enhance_query(
                PaymentQuery.get_query_group_by_budget(**args).join(Budget), Budget
            ),
        ),
    )