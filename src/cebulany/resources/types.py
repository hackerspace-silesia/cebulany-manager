from datetime import datetime

VALID_BOOLEANS = {
    'true': True,
    '1': True,
    '0': False,
    'false': False,
}


def boolean(value):
    try:
        return VALID_BOOLEANS[value.strip().lower()]
    except KeyError:
        raise ValueError('valid values are true, 1, 0 or false')


def dt_type(value):
    return datetime.strptime(value, '%Y-%m-%d')


def month_type(value):
    return datetime.strptime(value, '%Y-%m')
