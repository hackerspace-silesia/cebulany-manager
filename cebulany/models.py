from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Table

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class BaseWithTransaction(Base):
    __abstract__ = True
    @declared_attr
    def transaction_id(cls):
        return db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    
    @declared_attr
    def transaction(cls):
        return relationship('Transaction', backref='%ss' % cls.__tablename__)


class Transaction(Base):
    __abstract__ = False
    type = db.Column(db.String(20))
    line_num = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    send_date = db.Column(db.Date)
    title = db.Column(db.String(300))
    name = db.Column(db.String(300), index=True)
    address = db.Column(db.String(300))
    main_line = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))
    iban = db.Column(db.String(300))
    proposed_member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    proposed_member = relationship('Member')


class Member(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    join_date = db.Column(db.Date, nullable=False)


class PaidMonth(BaseWithTransaction):
    __abstract__ = False
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Numeric(precision=2), nullable=False)

    member = relationship(Member, backref='months')


class Donation(BaseWithTransaction):
    __abstract__ = False
    name = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Numeric(precision=2), nullable=False)


class Bill(BaseWithTransaction):
    __abstract__ = False
    name = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Numeric(precision=2), nullable=False)


class Other(BaseWithTransaction):
    __abstract__ = False
    name = db.Column(db.String(300), nullable=False)
    cost = db.Column(db.Numeric(precision=2), nullable=False)

