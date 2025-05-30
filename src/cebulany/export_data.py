from cebulany.pdf import parse
from cebulany.models import Transaction


def fill_transactions(data):
    from cebulany.app import app, db  # cyclic import - sorry guys
    with app.app_context():
        for record in data:
            transaction_query = (
                db.session.query(Transaction)
                .filter_by(ref_id=record['ref_id'])
            )
            if transaction_query.first() is None:
                db.session.add(Transaction(**record))
            else:
                transaction_query.update(record)
        db.session.commit()


if __name__ == "__main__":
    from sys import argv
    from itertools import chain
    for arg in argv[1:]:
        with open(arg) as file:
            gen = parse(file)
            fill_transactions(gen)
