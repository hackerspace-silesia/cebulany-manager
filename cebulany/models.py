from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import MetaData

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
    main_line = db.Column(db.String(300))
    cost = db.Column(db.Numeric(precision=2))
    iban = db.Column(db.String(300))
    ref_id = db.Column(db.String(100), index=True)
    proposed_member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    proposed_type_name = db.Column(db.String(300))
    proposed_type_id = db.Column(db.Integer, db.ForeignKey('paymenttype.id'))
    proposed_budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))

    proposed_member = relationship('Member')
    proposed_payment_type = relationship('PaymentType')
    proposed_budget = relationship('Budget')


class Member(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    join_date = db.Column(db.Date, nullable=False)


class PaymentType(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)
    has_members = db.Column(db.Boolean, default=False, nullable=False)
    show_details_in_report = db.Column(db.Boolean, default=False, nullable=False)
    show_count_in_report = db.Column(db.Boolean, default=False, nullable=False)


class Budget(Base):
    __abstract__ = False
    name = db.Column(db.String(300), index=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)
    show_details_in_report = db.Column(db.Boolean, default=False, nullable=False)
    show_count_in_report = db.Column(db.Boolean, default=False, nullable=False)


class Payment(Base):
    __abstract__ = False
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    name = db.Column(db.String(300), index=True, nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('paymenttype.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Numeric(precision=2), nullable=False)

    member = relationship(Member, backref='payments')
    transaction = relationship(Transaction, backref='payments')
    payment_type = relationship(PaymentType, backref='payments')
    budget = relationship(Budget, backref='payments')
