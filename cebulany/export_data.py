from itertools import chain
from cebulany.csv import open_and_parse
from cebulany.app import app, db
from cebulany.models import Transaction
from sys import argv


if __name__ == "__main__":
    data = list(chain.from_iterable(
        open_and_parse(arg) for arg in argv[1:]
    ))

    with app.app_context():
        for record in data:
            transaction_query = (
                db.session.query(Transaction)
                .filter_by(ref_id=record['ref_id'])
            )
            if transaction_query.first() is None:
                last_transaction = transaction_query = (
                    db.session.query(Transaction)
                    .filter_by(iban=record['iban'])
                    .order_by(Transaction.date.desc())
                    .first()
                )
                if last_transaction is not None:
                    record['proposed_member_id'] = last_transaction.proposed_member_id
                    record['proposed_type_name'] = last_transaction.proposed_type_name
                    record['proposed_type'] = last_transaction.proposed_type
                db.session.add(Transaction(**record))
            else:
                transaction_query.update(record)
        db.session.commit()

