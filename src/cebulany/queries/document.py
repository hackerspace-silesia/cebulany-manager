from datetime import date
from decimal import Decimal
from sqlalchemy import or_

from cebulany.models import Document, db


class DocumentQuery:

    @classmethod
    def _base_query(
        cls,
        parent: str | None = None,
        name_like: str | None = None,
        columns=Document.__table__.columns,
    ):
        query = db.session.query(*columns)
        if parent:
            query = query.filter(Document.parent == parent)
        if name_like:
            escaped = f"%%{name_like.replace("%", r"\%")}%%"
            query = query.filter(
                or_(
                    Document.filename.ilike(escaped),
                    Document.company_name.ilike(escaped),
                    Document.accounting_record.ilike(escaped),
                    Document.description.ilike(escaped),
                )
            )
        return query

    @classmethod
    def get_documents(
        cls,
        parent: str | None = None,
        name_like: str | None = None,
        ordering: str = "filename",
    ):
        query = cls._base_query(parent, name_like)
        return query.order_by(ordering)

    @classmethod
    def get_score(
        cls,
        dt: date,
        price: Decimal,
        parent: str,
        name_like: str | None = None,
    ):
        diff_date = db.func.abs(Document.date - dt)
        diff_price = db.func.abs(db.func.abs(Document.price) - db.func.abs(price))
        score_column = (diff_date + diff_price * 10).label("score")
        query = cls._base_query(parent, name_like)
        return query.add_columns(score_column).order_by("score").limit(10)
