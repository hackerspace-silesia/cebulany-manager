from __future__ import absolute_import
from cebulany.app import app, db
from cebulany.models import Member

from itertools import chain
from sys import argv
from datetime import datetime

from csv import reader

def get_users(filename):
    with open(filename) as f:
        return list(reader(f, delimiter=','))

if __name__ == "__main__":
    data = list(chain.from_iterable(
        get_users(arg) for arg in argv[1:]
    ))

    with app.app_context():
        for name, date, raw_active in data:
            name = name.strip().decode('utf-8')
            active = raw_active == 'y'
            member_query = (
                db.session.query(Member)
                .filter_by(
                    name=name,
                )
            )
            record = dict(
                name=name,
                is_active=active,
                join_date=datetime.strptime(date, u'%Y-%m'),
            )
            if member_query.first() is None:
                db.session.add(Member(**record))
            else:
                member_query.update(record)
        db.session.commit()

