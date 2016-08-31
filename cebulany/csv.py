# -*- coding: utf-8 -*-
from __future__ import print_function
from sys import argv
from codecs import open as codecs_open
from decimal import Decimal
from datetime import datetime
from re import compile as re_compile

import itertools

re_iban = re_compile(ur'\d\d( *\d{4}){6}')

TRANSACTION_TYPES = {
    u'PRZELEW UZNANIOWY': re_compile(
        ur'(?P<type>PRZELEW UZNANIOWY) '
        ur'(\(NADANO (?P<send_date>\d+-\d+-\d+)\) )?'
        ur'(?P<title>.+?)  +'
        ur'(?P<name>.+?)(  +|$)'
        ur'(?P<addr>.*)?'
    ),
    u'PRZELEW OBCIĄŻENIOWY': re_compile(
        ur'(?P<type>PRZELEW OBCIĄŻENIOWY) '
        ur'(\(NADANO (?P<send_date>\d+-\d+-\d+)\) )?'
        ur'(?P<title>.+?)  +'
        ur'(?P<name>.*)?'
    ),
    u'WPŁATA GOTÓWKOWA': re_compile(
        ur'(?P<type>WPŁATA GOTÓWKOWA)'
        ur'(?P<name>.+?)  +'
        ur'(?P<title>.+)'
    )
}

TRANSACTION_TYPES_SQL = {
    u'PRZELEW UZNANIOWY': 'payment',
    u'PRZELEW OBCIĄŻENIOWY': 'payout',
    u'WPŁATA GOTÓWKOWA': 'handy',
}

DATE_FORMAT = '%Y-%m-%d'
REV_DATE_FORMAT = '%d-%m-%Y'


def parse_lines(lines):
    return [parse_line(line.rstrip('\n')) for line in lines]


def parse_line(line):
    # problably main line has commas
    # unpacked as ((date, main), cost, total)
    date_main, cost, total = line.rsplit(',', 2)
    date, main = date_main.split(',', 1)
    main = main.strip()
    data = parse_main(main)
    data.update(
        date=datetime.strptime(date.strip(), DATE_FORMAT).date(),
        cost=Decimal(cost),
    )
    return data


def get_data(main):
    for transaction_type, regex in TRANSACTION_TYPES.items():
        if not main.startswith(transaction_type):
            continue
        match = regex.match(main)
        if match is not None:
            return match.groupdict()
    else:
        raise ValueError(main)

def get_iban(main):
    match = re_iban.search(main)
    if match is None:
        return main, ''
    return main[:match.start(0)], match.group(0)


def parse_main(main):
    without_iban, iban = get_iban(main)
    data = get_data(without_iban)
    send_date = data.get('send_date')
    send_date = send_date and datetime.strptime(send_date, REV_DATE_FORMAT)
    data_type = TRANSACTION_TYPES_SQL.get(data['type'], 'unknown')

    return dict(
        type=data_type,
        send_date=send_date and send_date.date(),
        title=data['title'],
        name=data.get('name', ''),
        address=data.get('addr'),
        iban=iban or None,
        main_line=main,
    )

def open_and_parse(arg):
    with codecs_open(arg, encoding='windows-1250') as f:
        return parse_lines(f.readlines()[1:-1])
    
if __name__ == "__main__":
    data = list(itertools.chain.from_iterable(
        open_and_parse(arg) for arg in argv[1:]
    ))
    data.sort(key=lambda obj: obj['date'])
    for x in data:
        print(x['type'], x['date'], x['title'], x['name'], x['cost'], sep='\t')

