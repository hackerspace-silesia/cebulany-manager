from sqlalchemy import func as sql_func, Date

from cebulany.models import db


def get_year_month_col(column: Date):
    database_type = db.engine.dialect.name
    if database_type == 'postgresql':
        return sql_func.to_char(column, 'YYYY-MM')
    if database_type == 'sqlite':
        return sql_func.strftime('%Y-%m', column)

    raise AttributeError(f'Unknown database type: {database_type}')


def get_year_col(column: Date):
    database_type = db.engine.dialect.name
    if database_type == 'postgresql':
        return sql_func.to_char(column, 'YYYY')
    if database_type == 'sqlite':
        return sql_func.strftime('%Y', column)

    raise AttributeError(f'Unknown database type: {database_type}')
