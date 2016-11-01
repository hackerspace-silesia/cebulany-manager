from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Table

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class BaseWithTransaction(Base):
    __abstract__ = True
    @declared_attr
    def transaction_id(cls):
        return db.Column(db.Integer, db.ForeignKey('transaction.id'))
    
    @declared_attr
    def transaction(cls):
        return relationship('Transaction', backref='%ss' % cls.__tablename__)


class Transaction(Base):
    __abstract__ = False
    type = db.Column(db.String(20))
    line_num = db.Column(db.Integer, index=True)
    date = db.Column(db.Date, index=True)
    send_date = db.Column(db.Date)
    title = db.Column(db.String(300))
    name = db.Column(db.String(300))
    address = db.Column(db.String(300))
    main_line = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))
    iban = db.Column(db.String(300))


class Member(Base):
    __abstract__ = False
    name = db.Column(db.String(300))
    email = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    join_date = db.Column(db.Date)


class PaidMonth(BaseWithTransaction):
    __abstract__ = False
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    date = db.Column(db.Date)
    cost = db.Column(db.Numeric(precision=2))

    member = relationship(Member, backref='months')


class Donation(BaseWithTransaction):
    __abstract__ = False
    name = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))


class Bill(BaseWithTransaction):
    __abstract__ = False
    name = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))


class Other(BaseWithTransaction):
    __abstract__ = False
    name = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))
