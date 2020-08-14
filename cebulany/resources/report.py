#! coding: utf-8
from io import BytesIO
from base64 import b64encode
from datetime import date, timedelta
from itertools import accumulate
from decimal import Decimal
from os import environ

from flask import Blueprint, render_template
from sqlalchemy import func as sql_func

from cebulany.models import db, Transaction, Payment, Budget, PaymentType

URL_PREFIX = '/' + environ.get('CEBULANY_APP_URL_PREFIX', '')


report_page = Blueprint('report_page', 'report', template_folder='../templates')
month_field = sql_func.extract('month', Transaction.date)
year_field = sql_func.extract('year', Transaction.date)


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

        rest_cost = 0

        types = db.session.query(PaymentType).order_by(PaymentType.name)
        for payment_type in types:
            if payment_type.show_details_in_report:
                cost, rows, graphs = self.get_payments_with_details(payment_type)
            else:
                cost, rows, graphs = self.get_total_payments(payment_type)

            rest_cost += cost
            positive_graphs += [payment for payment in graphs if payment.value > 0]
            negative_graphs += [payment for payment in graphs if payment.value < 0]
            self.rows += rows

        self.add_graph('positive', positive_graphs)
        self.add_graph('negative', negative_graphs, multiple=-1)

        diff = total - rest_cost
        if abs(diff) > Decimal('0.01'):
            self.rows.append(Money(u'NIE ROZLICZONE', diff))
        self.rows.append(Money(u'RAZEM', total))

    def get_total_payments(self, payment_type):
        query = (
            db.session
            .query(sql_func.sum(Payment.cost), sql_func.count(Payment.id))
            .join(Payment.transaction)
            .filter(Payment.payment_type_id == payment_type.id)
        )
        query = self.filterize_query(query)
        name = payment_type.name.upper()
        query_row = query.first()
        cost, count = query_row
        if cost is None:
            return 0, [], []
        payment = Money(name, cost)
        rows = [payment]

        # broken - todo fix
        #if payment_type.show_count_in_report:
        #    rows.append(Row(u'{}: {}'.format(name, u'ILOŚĆ'), count))

        return cost, rows, [payment]

    def get_payments_with_details(self, payment_type):
        query = (
            db.session
            .query(Payment.name, sql_func.sum(Payment.cost))
            .join(Payment.transaction)
            .filter(Payment.payment_type_id == payment_type.id)
            .group_by(sql_func.upper(Payment.name))
        )
        query = self.filterize_query(query)
        payment_type_name = payment_type.name.upper()

        payments = [
            Money(u'{}: {}'.format(payment_type_name, name), cost)
            for name, cost in query.all()
        ]

        if len(payments) == 0:
            return 0, [], []
        total = sum((Decimal(obj.value) for obj in payments), Decimal('0.00'))
        rows = payments + [Money(payment_type_name + u': SUMA', total)]

        return total, rows, payments

    def filterize_query(self, query):
        if self.month is None:
            return query.filter(year_field == self.year)
        else:
            return query.filter(
                year_field == self.year,
                month_field == self.month,
            )

    def add_graph(self, name, graphs, multiple=1):
        labels = [obj.name for obj in graphs]
        values = [obj.value * multiple for obj in graphs]
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

    def __repr__(self):
        name = self.__class__.__name__
        return u'{}<{!r}, {!r}>'.format(name, self.name, self.value)


class Money(Row):

    def get_value(self):
        return u'{:0.2f} zł'.format(self.value)

    def get_classes(self):
        if self.value < 0:
            return 'negative'
        return ''


def get_costs_plot_data(day):
    KEY_FIELDS = (year_field, month_field)

    query_total = (
        db.session
        .query(
            sql_func.sum(Transaction.cost),
            *KEY_FIELDS,
        )
        .filter(Transaction.date >= day)
        .group_by(*KEY_FIELDS)
        .order_by(*KEY_FIELDS)
    )
    data = query_total.all()

    def format_key(o):
        return '{}-{:02}'.format(o[1], o[2])

    labels = [format_key(o) for o in data]

    def values_sorted_by_date(query):
        data = {format_key(o): o[0] for o in query.all()}
        return [float(data.get(key, 0)) for key in labels]

    def values_on_budget_query(budget):
        query = (
            db.session
            .query(
                sql_func.sum(Payment.cost),
                *KEY_FIELDS,
            )
            .join(Transaction)
            .filter(
                Transaction.date >= day,
                Payment.budget == budget,
            )
            .group_by(*KEY_FIELDS)
            .order_by(*KEY_FIELDS)
        )
        return {
            'name': budget.name,
            'color': '#' + budget.color,
            'moneys': values_sorted_by_date(query)
        }

    def values_on_type_query(payment_type):
        query = (
            db.session
            .query(
                sql_func.sum(Payment.cost),
                *KEY_FIELDS,
            )
            .join(Transaction)
            .filter(
                Transaction.date >= day,
                Payment.payment_type == payment_type,
            )
            .group_by(*KEY_FIELDS)
            .order_by(*KEY_FIELDS)
        )
        return {
            'name': payment_type.name,
            'color': '#' + payment_type.color,
            'moneys': values_sorted_by_date(query)
        }

    start_value = float(
        db.session
        .query(sql_func.sum(Transaction.cost))
        .filter(Transaction.date < day)
        .scalar()
    )

    values = values_sorted_by_date(query_total)
    acc_values = [x + start_value for x in accumulate(values)]

    return {
        'dates': labels,
        'moneys': values,
        'acc': acc_values,
        'budgets': [
            values_on_budget_query(budget)
            for budget in (
                db.session
                .query(Budget)
                .filter(Budget.show_count_in_report == True)
            )
        ],
        'payment_types': [
            values_on_type_query(payment_type)
            for payment_type in (
                db.session
                .query(PaymentType)
                .filter(PaymentType.show_count_in_report == True)
            )
        ]
    }


@report_page.route(URL_PREFIX + '/report')
def basic():
    day = date.today() - timedelta(days=365 * 2)
    day = day.replace(day=1)
    query_dates = db.session.query(
        year_field,
        month_field,
        sql_func.sum(Transaction.cost),
    ).group_by(
        year_field, month_field,
    ).order_by(
        year_field.desc(), month_field.desc(),
    ).filter(Transaction.date >= day)
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
        main_plot=get_costs_plot_data(day)
    )
