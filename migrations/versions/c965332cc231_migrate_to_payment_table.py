# coding=utf-8
"""migrate to payment table

Revision ID: c965332cc231
Revises: d46a231df696
Create Date: 2018-08-26 18:15:02.525754

"""
from datetime import date

from alembic import op
from sqlalchemy import String, Integer, Numeric, Date, Boolean
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'c965332cc231'
down_revision = 'd46a231df696'
branch_labels = None
depends_on = None


def upgrade():
    return # this migration is outdated
    payment = table('payment',
        column('id', Integer),
        column('name', String),
        column('cost', Numeric),
        column('transaction_id', Integer),
        column('payment_type_id', Integer),
        column('budget_id', Integer),
        column('member_id', Integer),
        column('date', Date),
    )

    budget = table('budget',
        column('id', Integer),
        column('name', String),
        column('color', String),
        column('show_details_in_report', Boolean),
        column('show_count_in_report', Boolean),
    )

    paymenttype = table('paymenttype',
        column('id', Integer),
        column('name', String),
        column('color', String),
        column('has_members', Boolean),
        column('show_details_in_report', Boolean),
        column('show_count_in_report', Boolean),
    )

    op.bulk_insert(budget, [
        dict(name=u'SKŁADKI', color='3AA655', show_details_in_report=False, show_count_in_report=False),
        dict(name=u'DAROWIZNY', color='1560BD', show_details_in_report=False, show_count_in_report=False),
        dict(name=u'DZIAŁALNOŚĆ ODPŁATNA', color='A9B2C3', show_details_in_report=False, show_count_in_report=False),
        dict(name=u'GRANT SZKOŁY', color='1560BD', show_details_in_report=False, show_count_in_report=False),
        dict(name=u'GRANT A', color='652DC1', show_details_in_report=False, show_count_in_report=False),
        dict(name=u'GRANT B', color='1AB385', show_details_in_report=False, show_count_in_report=False),
    ])

    op.bulk_insert(paymenttype, [
        dict(name=u'SKŁADKI', color='3AA655', has_members=True, show_count_in_report=True, show_details_in_report=False),
        dict(name=u'RACHUNKI', color='FD0E35', show_details_in_report=True, has_members=False, show_count_in_report=False),
        dict(name=u'DAROWIZNY', color='1560BD', has_members=False, show_details_in_report=False, show_count_in_report=False),
        dict(name=u'INNE', color='A9B2C3', has_members=False, show_details_in_report=False, show_count_in_report=False),
        dict(name=u'SPRZĘT', color='87421F', has_members=False, show_details_in_report=False, show_count_in_report=False),
    ])

    connection = op.get_bind()

    def _first(sql):
        exc = connection.execute(sql)
        return list(exc)[0]['id']

    def _date(s):
        keys = [int(x) for x in s.split('-')]
        return date(*keys)

    type_id = _first("select id from paymenttype where \"name\" == 'RACHUNKI'")
    budget_id = _first("select id from paymenttype where \"name\" == 'SKŁADKI'")
    rows = list(connection.execute('''
        select
          aa."name" as "name", aa."cost" as "cost", "transaction_id", "date"
        from bill as aa
        join "transaction" t on t.id == aa.transaction_id;
    '''))
    for row in rows:
        connection.execute(
            payment.insert().values(
                name=row['name'],
                date=_date(row['date']),
                cost=row['cost'],
                member_id=None,
                transaction_id=row['transaction_id'],
                payment_type_id=type_id,
                budget_id=budget_id,
            )
        )

    type_id = _first("select id from paymenttype where \"name\" == 'DAROWIZNY'")
    budget_id = _first("select id from budget where \"name\" == 'DAROWIZNY'")
    rows = list(connection.execute('''
        select
          aa."name" as "name", aa."cost" as "cost", "transaction_id", "date"
        from donation as aa
        join "transaction" t on t.id == aa.transaction_id;
    '''))
    for row in rows:
        connection.execute(
            payment.insert().values(
                name=row['name'],
                date=_date(row['date']),
                cost=row['cost'],
                member_id=None,
                transaction_id=row['transaction_id'],
                payment_type_id=type_id,
                budget_id=budget_id,
            )
        )

    type_id = _first("select id from paymenttype where \"name\" == 'INNE'")
    budget_id = _first("select id from budget where \"name\" == 'SKŁADKI'")
    rows = list(connection.execute('''
        select
          aa."name" as "name", aa."cost" as "cost", "transaction_id", "date"
        from other as aa
        join "transaction" t on t.id == aa.transaction_id;
    '''))
    for row in rows:
        connection.execute(
            payment.insert().values(
                name=row['name'],
                date=_date(row['date']),
                cost=row['cost'],
                member_id=None,
                transaction_id=row['transaction_id'],
                payment_type_id=type_id,
                budget_id=budget_id,
            )
        )

    type_id = _first("select id from paymenttype where \"name\" == 'SKŁADKI'")
    budget_id = _first("select id from budget where \"name\" == 'SKŁADKI'")
    rows = list(connection.execute('select * from paidmonth'))
    for row in rows:
        connection.execute(
            payment.insert().values(
                name='-',
                date=_date(row['date']),
                cost=row['cost'],
                member_id=row['member_id'],
                transaction_id=row['transaction_id'],
                payment_type_id=type_id,
                budget_id=budget_id,
            )
        )


def downgrade():
    # skip lol
    pass

