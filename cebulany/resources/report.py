#! coding: utf-8
from flask import Blueprint, render_template
from sqlalchemy import func as sql_func
from sqlalchemy import distinct
from decimal import Decimal
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from io import BytesIO
from base64 import b64encode
from datetime import date
from math import ceil, floor

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


def accumulate_sum(iterable):  # py2.7 why
    values = []
    s = 0.0
    for i in iterable:
        s += float(i)
        values.append(s)
    return values


def save_plot(fig):
    bio = BytesIO()
    fig.savefig(bio, format='png')
    return b64encode(bio.getvalue())


class ReportMonth(object):

    def __init__(self, year, month, total):
        self.year = year
        self.month = month
        self.rows = []
        self.graphs = {}

        paids_value = self.compute_paids()
        donations_value = self.compute_donations()
        bills_value, bills = self.compute_bills()
        others_value, others = self.compute_others()

        self.add_positive_graph(paids_value, donations_value, others) 
        self.add_negative_graph(bills, others) 

        values = sum([
            paids_value,
            donations_value,
            bills_value,
            others_value,
        ])

        diff = total - values
        if abs(diff) > Decimal('0.01'):
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

        bills = [Money(name, cost) for name, cost in query.all()]
        total = sum((Decimal(obj.value) for obj in bills), Decimal('0.00'))

        self.rows += bills

        self.rows.append(Money(u'SUMA RACHUNKÓW', total))

        return total, bills

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
        ).group_by(
            sql_func.upper(Other.name)
        )
        query = self.filterize_query(query)

        others = [Money(name, cost) for name, cost in query.all()]
        total = sum((Decimal(obj.value) for obj in others), Decimal('0.00'))

        self.rows += others

        return total, others

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

    def add_positive_graph(self, paids_values, donations_values, others):
        labels = [obj.name for obj in others if int(obj.value) > 0]
        values = [obj.value for obj in others if int(obj.value) > 0]
        if donations_values > 0:
            labels.insert(0, u'DOTACJE')
            values.insert(0, donations_values)
        if paids_values > 0:
            labels.insert(0, u'SKŁADKI')
            values.insert(0, paids_values)
        self.graphs['positive'] = self.make_pie(u'PRZYCHÓD', values, labels)

    def add_negative_graph(self, bills, others):
        labels = [obj.name for obj in bills] + [
                obj.name for obj in others if int(obj.value) < 0]
        values = [-obj.value for obj in bills] + [
                -obj.value for obj in others if int(obj.value) < 0]
        self.graphs['negative'] = self.make_pie(u'WYDATKI', values, labels)

    @staticmethod
    def make_pie(title, values, labels):
        fig = plt.figure(figsize=(3, 3))
        plt.title(title)
        patches, _, _ = plt.pie(values, autopct=u'%.0f%%')
        plt.tight_layout()
        plt.legend(patches, labels, loc='best', fontsize='x-small')
        return save_plot(fig)



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

def get_costs_graph():
    key_fields = (year_field, month_field)
    query_total = db.session.query(
        sql_func.sum(Transaction.cost),
        *key_fields
    ).group_by(*key_fields).order_by(*key_fields)
    query_paids = db.session.query(
        sql_func.sum(PaidMonth.cost), *key_fields
    ).join(Transaction).group_by(*key_fields)
    query_bills = db.session.query(
        sql_func.sum(Bill.cost), *key_fields
    ).join(Transaction).group_by(*key_fields)
    data = query_total.all()
    def format_key(o):
        return '{}-{:02}'.format(o[1], o[2])
    labels = [format_key(o) for o in data]
    label_indexs = range(len(labels))
    def values_sorted_by_date(query):
        data = {format_key(o): o[0] for o in query.all()}
        return [data.get(key, 0) for key in labels]
        
    values = values_sorted_by_date(query_total)
    paid_values = values_sorted_by_date(query_paids)
    bill_values = values_sorted_by_date(query_bills)
    acc_values = accumulate_sum(values)
    min_value = int(floor(min(values) / 1000) * 1000)
    max_value = int(ceil(max(acc_values) / 1000) * 1000)

    fig, ax = plt.subplots(figsize=(8, 3))
    plt.grid(which='major', color='silver', linestyle='--')

    plt.plot(values, label=u'Przychód / Strata')
    plt.plot(paid_values, label=u'Składki', color='green')
    plt.plot(bill_values, label=u'Rachunki', color='orange')
    plt.fill_between(label_indexs, 0, acc_values, color='deepskyblue', label='Stan konta')
    plt.xlim([0, len(labels) - 1])
    plt.ylim([min_value - 250, max_value + 250])

    plt.xticks(label_indexs, labels, rotation=45)
    ax.yaxis.set_major_formatter(FormatStrFormatter(u'%.0f zł'))
    plt.yticks(range(min_value, max_value, 500))
    plt.tick_params(axis='x', labelsize='x-small')
    plt.tick_params(axis='y', labelsize='x-small')
    plt.axhline(color='r')
    plt.tight_layout()
    plt.legend(loc='upper left')
    return save_plot(fig)


@report_page.route('/report')
def basic():
    query_dates = db.session.query(
        year_field,
        month_field,
        sql_func.sum(Transaction.cost),
    ).group_by(
        year_field, month_field,
    ).order_by(
        year_field.desc(), month_field.desc(),
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


    return render_template('report.html', months=months, fig_total=get_costs_graph())
