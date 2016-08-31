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
            db.session.add(Transaction(**record))
        db.session.commit()

