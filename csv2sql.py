from sys import argv
from codecs import open as codecs_open
from decimal import Decimal
from datetime import datetime
from re import compile as re_compile

import itertools

TRANSACTION_TYPES = {
    'PRZELEW UZNANIOWY': re_compile(
        r'(?P<type>PRZELEW UZNANIOWY) '
        r'(\(NADANO (?P<send_date>\d+-\d+-\d+)\) )?'
        r'(?P<title>.+?)  +'
        r'(?P<name>.+?)(  +|$)'
        r'(?P<addr>.*)?'
    ),
    'PRZELEW OBCIĄŻENIOWY': re_compile(
        r'(?P<type>PRZELEW OBCIĄŻENIOWY) '
        r'(\(NADANO (?P<send_date>\d+-\d+-\d+)\) )?'
        r'(?P<title>.+?)  +'
        r'(?P<name>.*)?'
    ),
    'WPŁATA GOTÓWKOWA': re_compile(
        r'(?P<type>WPŁATA GOTÓWKOWA)'
        r'(?P<name>.+?)  +'
        r'(?P<title>.+)'
    )
}

TRANSACTION_TYPES_SQL = {
    'PRZELEW UZNANIOWY': 'payment',
    'PRZELEW OBCIĄŻENIOWY': 'payout',
    'WPŁATA GOTÓWKOWA': 'handy',
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
        date=datetime.strptime(date.strip(), DATE_FORMAT),
        cost=Decimal(cost),
        main=main,
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


def parse_main(main):
    data = get_data(main)
    send_date = data.get('send_date', '')
    send_date = send_date and datetime.strptime(send_date, REV_DATE_FORMAT)
    data_type = TRANSACTION_TYPES_SQL.get(data['type'], 'unknown')

    return dict(
        type=data_type,
        send_date=send_date,
        title=data['title'],
        name=data.get('name', ''),
        address=data.get('addr'),
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
    t = Decimal('0')
    for x in data:
        print(x['type'], x['date'].date(), x['title'], x['name'], x['cost'], sep='\t')

