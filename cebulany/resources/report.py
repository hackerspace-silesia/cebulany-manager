#! coding: utf-8
from flask import Blueprint, render_template
from sqlalchemy import func as sql_func
from decimal import Decimal
from io import BytesIO
from base64 import b64encode
from datetime import date

from cebulany.models import db, Transaction, Payment, PaymentType

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

        positive_graphs = []
        negative_graphs = []

        types = db.session.query(PaymentType).order_by(PaymentType.name)
        for payment_type in types:
            if payment_type.show_details_in_report:
                query = (
                    db.session
                    .query(Payment.name, sql_func.sum(Payment.cost))
                    .join(Payment.transaction)
                    .filter(Payment.payment_type_id == payment_type.id)
                    .group_by(sql_func.upper(Payment.name))
                )
                query = self.filterize_query(query)
                fname = payment_type.name.upper()

                payments = [Money(fname + ': ' + name, cost) for name, cost in query.all()]
                if len(payments) == 0:
                    continue
                total = sum((Decimal(obj.value) for obj in payments), Decimal('0.00'))
                self.rows += payments
                self.rows.append(Money(fname + u': SUMA', total))
                positive_graphs += [payment for payment in payments if payment.value > 0]
                negative_graphs += [payment for payment in payments if payment.value < 0]
            else:
                query = (
                    db.session
                    .query(sql_func.sum(Payment.cost))
                    .join(Payment.transaction)
                    .filter(Payment.payment_type_id == payment_type.id)
                )
                query = self.filterize_query(query)
                name = payment_type.name.upper()
                cost = query.first()[0]
                if cost is None:
                    continue
                payment = Money(name, cost)

                self.rows.append(payment)

                if cost > 0:
                    positive_graphs.append(payment)
                elif cost < 0:
                    negative_graphs.append(payment)

        self.add_graph('positive', positive_graphs)
        self.add_graph('negative', negative_graphs)

        # diff = total - values
        # if abs(diff) > Decimal('0.01'):
        #     self.rows.append(Money(u'NIE ROZLICZONE', diff))
        # self.rows.append(Money(u'RAZEM', total))

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

    def add_graph(self, name, graphs):
        labels = [obj.name for obj in graphs]
        values = [obj.value for obj in graphs]
        self.graphs[name] = self.make_pie(values, labels)

    @staticmethod
    def make_pie(values, labels):
        return {
            'vals': [float(val) for val in values],
            'labels': [label.upper() for label in labels],
        }


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


def get_costs_plot_data():
    key_fields = (year_field, month_field)
    query_total = db.session.query(
        sql_func.sum(Transaction.cost),
        *key_fields
    ).group_by(*key_fields).order_by(*key_fields)
    data = query_total.all()

    def format_key(o):
        return '{}-{:02}'.format(o[1], o[2])

    labels = [format_key(o) for o in data]

    def values_sorted_by_date(query):
        data = {format_key(o): o[0] for o in query.all()}
        return [float(data.get(key, 0)) for key in labels]
        
    values = values_sorted_by_date(query_total)
    acc_values = accumulate_sum(values)

    return {
        'dates': labels,
        'moneys': values,
        'acc': acc_values,
    }


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


    return render_template(
        'report.html',
        months=months,
        main_plot=get_costs_plot_data()
    )
