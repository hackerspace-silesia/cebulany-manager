from datetime import datetime, timedelta
from urllib.parse import quote
import base64
import os

import onetimepass
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import MetaData
from werkzeug.security import generate_password_hash

db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "ix": 'ix_%(column_0_label)s',
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(column_0_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )
)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Transaction(Base):
    __abstract__ = False
    line_num = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    title = db.Column(db.String(300))
    name = db.Column(db.String(300), index=True)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    iban = db.Column(db.String(40), index=True)
    ref_id = db.Column(db.String(100), index=True)
    additional_info = db.Column(db.String(300), server_default="", nullable=False)

    suggestion = relationship('Suggestion', foreign_keys=[iban], 
                              primaryjoin='Transaction.iban == Suggestion.iban')


class Suggestion(db.Model):
    __tablename__ = "suggestion"
    iban = db.Column(db.String(40), primary_key=True, nullable=False)

    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    type_name = db.Column(db.String(300))
    type_id = db.Column(db.Integer, db.ForeignKey('paymenttype.id'))
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))
    inner_budget_id = db.Column(db.Integer, db.ForeignKey('innerbudget.id'), nullable=True)

    member = relationship('Member')
    payment_type = relationship('PaymentType')
    budget = relationship('Budget')
    inner_budget = relationship('InnerBudget')


class Member(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    join_date = db.Column(db.Date, nullable=False)


class AccountancyType(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)


class PaymentType(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)
    has_members = db.Column(db.Boolean, default=False, nullable=False)
    show_details_in_report = db.Column(db.Boolean, default=False, nullable=False)
    show_count_in_report = db.Column(db.Boolean, default=False, nullable=False)

    accountancy_type_id = db.Column(db.Integer, db.ForeignKey('accountancytype.id'), nullable=True)
    accountancy_type = relationship(AccountancyType, backref='payment_types')


class Budget(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)
    show_details_in_report = db.Column(db.Boolean, default=False, nullable=False)
    show_count_in_report = db.Column(db.Boolean, default=False, nullable=False)
    description_on_negative = db.Column(db.String(300), server_default="", nullable=False)
    description_on_positive = db.Column(db.String(300), server_default="", nullable=False)


class InnerBudget(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)


class Payment(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('paymenttype.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)
    inner_budget_id = db.Column(db.Integer, db.ForeignKey('innerbudget.id'), nullable=True)

    member = relationship(Member, backref='payments')
    transaction = relationship(Transaction, backref='payments')
    payment_type = relationship(PaymentType, backref='payments')
    budget = relationship(Budget, backref='payments')
    inner_budget = relationship(InnerBudget, backref='payments')


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    otp_secret = db.Column(db.String(16))
    token = db.Column(db.String(32))
    token_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def generate_token(self):
        self.token = base64.b32encode(os.urandom(20)).decode('utf-8')

    def update_token_time(self):
        seconds = current_app.config['TOKEN_TIME']
        self.token_time = datetime.utcnow() + timedelta(seconds=seconds)

    @property
    def totp_uri(self):
        app_name = quote(current_app.config['APP_NAME'])
        username = quote(self.username)
        return (
           # from https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask (thx btw)
           f'otpauth://totp/{app_name}:{username}'
           f'?secret={self.otp_secret}&issuer={app_name}'
        )

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)
