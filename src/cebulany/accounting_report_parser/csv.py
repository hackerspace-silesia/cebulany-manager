# -*- coding: utf-8 -*-
from __future__ import print_function
from sys import argv
from codecs import open as codecs_open
from decimal import Decimal
from datetime import datetime
from re import compile as re_compile

import itertools


TRANSACTION_TYPES = {
    u'PRZELEW UZNANIOWY': re_compile(
        r'(?P<type>PRZELEW UZNANIOWY) '
        r'(\(NADANO (?P<send_date>[\d ]+-[\d ]+-[\d ]+)\) )?'
        r'(?P<title>.+?)(  +|$)'
        r'(?P<name>.+)?'
    ),
    u'PRZELEW OBCIĄŻENIOWY': re_compile(
        r'(?P<type>PRZELEW OBCIĄŻENIOWY) '
        r'(\(NADANO (?P<send_date>[\d ]+-[\d ]+-[\d ]+)\) )?'
        r'(?P<title>.+?)(  +|$)'
        r'(?P<name>.*)?'
    ),
    u'WPŁATA GOTÓWKOWA': re_compile(
        r'(?P<type>WPŁATA GOTÓWKOWA)'
        r'(?P<name>.+?)  +'
        r'(?P<title>.+)'
    ),
    u'': re_compile(
        r'(?P<type>)'
        r'(?P<name>)'
        r'(?P<title>)'
    ),
}

DATE_FORMATS = (
    '%d-%m-%Y',
    '%Y-%m-%d',
)


def to_date(raw):
    raw = raw.strip()
    for date_format in DATE_FORMATS:
        try:
            dt = datetime.strptime(raw, date_format)
        except ValueError:
            continue
        else:
            return dt.date()
    raise ValueError(f"unknown date format: {raw}")


def parse_lines(lines):
    return [
        parse_line(line.rstrip('\n'), line_num)
        for line_num, line in enumerate(lines, start=1)
    ]


def parse_line(line, line_num=None):
    date, cost, name, main, iban, ref_id, op_code = line.split(u';', 6)
    main = main.strip()
    name = name.strip()
    if not name:
        data = parse_main(main, line_num)
    else:
        data = dict(
            main_line=u'{} {}'.format(name, main),
            title=main,
            name=name,
        )
    data.update(
        date=to_date(date),
        cost=Decimal(cost),
        line_num=line_num,
        iban=iban,
        ref_id=ref_id if ref_id.startswith('CEN') else f'{ref_id}::{date}::{op_code}',
    )
    return data


def get_data(main, line_num=None):
    for transaction_type, regex in TRANSACTION_TYPES.items():
        if not main.startswith(transaction_type):
            continue
        match = regex.match(main)
        if match is not None:
            return match.groupdict()
    else:
        raise ValueError(repr(main), line_num)


def parse_main(main, line_num=None):
    data = get_data(main, line_num)

    return dict(
        title=data['title'],
        name=data.get('name') or main,
        main_line=main,
    )


def open_and_parse(arg):
    with codecs_open(arg, encoding='utf-8') as f:
        return parse_lines(f.readlines())


if __name__ == "__main__":
    data = list(itertools.chain.from_iterable(
        open_and_parse(arg) for arg in argv[1:]
    ))
    data.sort(key=lambda obj: obj['date'])
    s = 0
    for x in data:
        s += x['cost']
        line = u'\t'.join([
            str(x['date']), x['title'], x['name'], str(x['cost'])
        ])
        print(line.encode('utf-8'))
    print('SUM', str(s))
