from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class BaseWithTransaction(Base):
    __abstract__ = True
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))


class Transaction(Base):
    type = db.Column(db.String(20))
    date = db.Column(db.Date)
    send_date = db.Column(db.Date)
    title = db.Column(db.String(300))
    name = db.Column(db.String(300))
    address = db.Column(db.String(300))
    main_line = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))


class Member(BaseWithTransaction):
    name = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True)


class PayedMonth(BaseWithTransaction):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    date = db.Column(db.Date)
    cost = db.Column(db.Numeric(precision=2))
    payed = db.Column(db.Boolean, default=False)


class Donation(BaseWithTransaction):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Numeric(precision=2))
    name = db.Column(db.String(300))


class Bill(BaseWithTransaction):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Numeric(precision=2))
    name = db.Column(db.String(300))
    frequency_months = db.Column(db.Integer, default=0)

