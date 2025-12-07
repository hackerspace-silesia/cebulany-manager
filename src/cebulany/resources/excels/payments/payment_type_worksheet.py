from cebulany.queries.inner_transfer import InnerTransferQuery
from cebulany.queries.payment import PaymentQuery
from cebulany.models import db, PaymentType

from .type_worksheet import fill_type_worksheet, types_to_rows, inner_transfers_to_rows, enhance_query
from .common import ArgsObj



def fill_payment_type_worksheet(sheet, args, obj_args: ArgsObj): 
    transfers = InnerTransferQuery.get_agg_query(
        start_date=args.start_date,
        end_date=args.end_date,
        inner_budget_id=args.inner_budget_id,
        budget_id=args.budget_id,
    )
    payment_types = enhance_query(
        PaymentQuery.get_query_group_by_type(**args), PaymentType
    )
    fill_type_worksheet(
        sheet,
        types_to_rows(sheet, payment_types),
        inner_transfers_to_rows(
            sheet,
            obj_args.budget,
            obj_args.inner_budget,
            db.session.execute(transfers),
        ),
    )