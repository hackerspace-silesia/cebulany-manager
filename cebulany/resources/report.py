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

        values = sum([
            self.compute_paids(),
            self.compute_bills(),
            self.compute_donations(),
            self.compute_others(),
        ])

        diff = total - values
        if diff > 0:
            self.rows.append(Money(u'NIE ROZLICZONE', diff))
        self.rows.append(Money(u'RAZEM', total))

    def compute_paids(self):
        query = db.session.query(
            sql_func.sum(PaidMonth.cost),
            sql_func.count(distinct(PaidMonth.member_id)),
        ).join(
            PaidMonth.transaction
        )

        paids_value, member_count = self.filterize_query(query).first()
        self.rows.append(Money(u'SKŁADKI', paids_value))
        self.rows.append(Row(u'WPŁACIŁO', member_count))
        return paids_value


    def compute_bills(self):
        query = db.session.query(
            Bill.name,
            sql_func.sum(Bill.cost),
        ).join(
            Bill.transaction
        ).group_by(sql_func.upper(Bill.name))
        query = self.filterize_query(query)

        total = Decimal('0.00')
        for name, cost in query.all():
            total += Decimal(cost)
            self.rows.append(Money(name, cost))

        self.rows.append(Money(u'SUMA RACHUNKÓW', total))

        return total

    def compute_donations(self):
        query = db.session.query(
            sql_func.sum(Donation.cost),
        ).join(
            Donation.transaction
        )

        donations_value = self.filterize_query(query).scalar() or 0
        if donations_value > 0:
            self.rows.append(Money(u'DAROWIZNY', donations_value))
        return donations_value

    def compute_others(self):
        query = db.session.query(
            Other.name,
            sql_func.sum(Other.cost),
        ).join(
            Other.transaction
        ).group_by(sql_func.upper(Other.name))
        query = self.filterize_query(query)

        total = Decimal(0)
        for name, cost in query.all():
            total += Decimal(cost) 
            self.rows.append(Money(name, cost))

        return total

    def filterize_query(self, query):
        if self.month is None:
            return query.filter(
                year_field == self.year,
            )
        else:
            return query.filter(
                year_field == self.year,
                month_field == self.month,
            )


class Row(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return str(self.value)

    def get_classes(self):
        return ''


class Money(Row):

    def get_value(self):
        return u'{:0.2f} zł'.format(self.value)
    
    def get_classes(self):
        if self.value < 0:
            return 'negative'
        return ''


@report_page.route('/report')
def basic():
    from datetime import date
    query_dates = db.session.query(
        year_field,
        month_field,
        sql_func.sum(Transaction.cost),
    ).group_by(
        year_field, month_field,
    ).order_by(
        year_field, month_field,
    ).filter(Transaction.date >= date(2015, 4, 1))
    months = [
        ReportMonth(year, month, total)
        for year, month, total in query_dates.all()
    ]
    """
    query_dates = db.session.query(
        year_field,
        sql_func.sum(Transaction.cost),
    ).group_by(
        year_field
    ).order_by(
        year_field
    ).filter(Transaction.date >= date(2015, 4, 1))
    months += [
        ReportMonth(year, None, total)
        for year, total in query_dates.all()
    ]"""

    return render_template('report.html', months=months)
