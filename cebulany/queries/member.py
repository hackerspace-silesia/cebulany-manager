from cebulany.models import Member


class MemberQuery:

    @classmethod
    def get_list_query(cls, name=None, limit=None, order="name"):
        query = Member.query
        if order == "name":
            query = query.order_by(Member.name)
        elif order == "table":
            query = query.order_by(Member.is_active.desc(), Member.join_date, Member.name)
        query = cls._filter_by_name(query, name)
        query = cls._limit(query, limit)
        return query

    @staticmethod
    def _filter_by_name(query, name):
        name = name and name.strip()
        if not name:
            return query
        args = [
            Member.name.ilike('%%%s%%' % arg.replace('%', r'\%'))
            for arg in name.split()
        ]
        return query.filter(*args)

    @staticmethod
    def _limit(query, limit):
        if limit is None:
            return query
        return query.limit(limit)
