#! coding: utf-8
from flask import Blueprint, render_template
from sqlalchemy import func as sql_func
from sqlalchemy import distinct
from decimal import Decimal

from cebulany.models import (
    db,
    Transaction,
    PaidMonth,
    Bill,
    Donation,
    Other,
)

report_page = Blueprint('report_page', 'report', template_folder='../templates')
month_field = sql_func.extract('month', Transaction.date)
year_field = sql_func.extract('year', Transaction.date)

class ReportMonth(object):

    def __init__(self, year, month, total):
        self.year = year
        self.month = month
        self.rows = []

        paids_value = self.compute_paids()
        bills_value = self.compute_bills()

        self.rows.append(Row(
            u'NIE ROZLICZONE',
            total - (paids_value + bills_value),
            u'zł'
        ))
        self.rows.append(Row(u'RAZEM', total, u'zł'))

    def compute_paids(self):
        query = db.session.query(
            sql_func.sum(PaidMonth.cost),
            sql_func.count(distinct(PaidMonth.member_id)),
        ).join(
            PaidMonth.transaction
        ).filter(year_field == self.year, month_field == self.month)

        paids_value, member_count = query.first()
        # todo: maybe i18n lol im too lazy
        self.rows.append(Row(u'SKŁADKI', round(paids_value, 2), u'zł'))
        self.rows.append(Row(u'WPŁACIŁO', member_count , u'osób'))
        if member_count > 0:
            avg_paid = round(paids_value / member_count, 2)
            self.rows.append(Row(u'ŚREDNIA SKŁADEK', avg_paid , u'zł'))
        return paids_value

    def compute_bills(self):
        query = db.session.query(
            Bill.name,
            Bill.cost,
        ).join(
            Bill.transaction
        ).filter(
            year_field == self.year,
            month_field == self.month,
        ).group_by(sql_func.upper(Bill.name))

        total = Decimal('0.00')
        for name, cost in query.all():
            cost = round(cost, 2)
            total += Decimal(cost)
            self.rows.append(Row(name, cost, u'zł'))

        self.rows.append(Row(u'SUMA RACHUNKÓW', round(total, 2), u'zł'))

        return total

class Row(object):

    def __init__(self, name, value, suffix=''):
        self.name = name
        self.value = value
        self.suffix = suffix


@report_page.route('/report')
def basic():
    query_dates = db.session.query(
        year_field,
        month_field,
        sql_func.sum(Transaction.cost),
    ).group_by(
        year_field, month_field,
    ).order_by(
        year_field, month_field,
    )
    months = [
        ReportMonth(year, month, total)
        for year, month, total in query_dates.all()
    ]


    return render_template('report.html', months=months)
