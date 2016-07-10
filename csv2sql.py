from sys import argv
from codecs import open as codecs_open
from decimal import Decimal
from datetime import datetime
from re import compile as re_compile

re_main = re_compile(
    r'PRZELEW (?P<type>UZNANIOWY|OBCIĄŻENIOWY) '
    r'(\(NADANO (?P<send_date>\d+-\d+-\d+)\) )?'
    r'(?P<title>.+?)  +'
    r'(?P<name>.+?)(  +|$)'
    r'(?P<addr>.*)?'
)
DATE_FORMAT = '%Y-%m-%d'
REV_DATE_FORMAT = '%d-%m-%Y'


def parse_lines(lines):
    return [parse_line(line.rstrip('\n')) for line in lines]


def parse_line(line):
    # problably main line has commas
    # unpacked as ((date, main), cost, total)
    date_main, cost, total = line.rsplit(',', 2)
    date, main = date_main.split(',', 1)
    data = parse_main(main)
    data.update(
        date=datetime.strptime(date.strip(), DATE_FORMAT),
        cost=Decimal(cost),
    )
    return data

def parse_main(main):
    match = re_main.match(main.strip())
    assert match is not None, repr(main.strip())
    data = match.groupdict()
    send_date = data['send_date'] and datetime.strptime(
            data['send_date'], REV_DATE_FORMAT)
    return dict(
        profit=data['type'] == 'UZNANIOWY',
        send_date=send_date,
        title=data['title'],
        name=data['name'],
        address=data['addr'],
    )
    

if __name__ == "__main__":
    with codecs_open(argv[1], encoding='windows-1250') as f:
        data = parse_lines(f.readlines()[1:-1])
    data.sort(key=lambda obj: obj['cost'])
    t = Decimal('0')
    for x in data:
        t += x['cost']
        print(x['date'].date(), x['title'], x['name'], x['cost'])
    print('TOTAL', t)
