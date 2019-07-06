#!/usr/bin/env python
# encoding: utf-8
from datetime import date, timedelta
from random import randint, choice, random
from decimal import Decimal
from string import ascii_uppercase
start_date = date.today() - timedelta(days=30)

firsts = [
    u'MAREK', u'DAREK', u'HENRYK', u'MICHAŁ', u'ZYGFRYD', u'PAWEŁ', u'STANISŁAW',
    u'ŁUKASZ', u'DAWID', u'FILIP', u'OKTAWIAN', u'BŁAŻEJ', u'BARTUŚ',
]
lasts = [
    'KOWALSKI', 'OWCZAREK', 'MARKOWSKI', 'PROSTACKI', 'RYBSKI', 'STAROWSKI',
    'CZARNOWSKI', 'WARSZAWSKI', 'NOWAK', 'CHOLERAWIECKI', 'TESTOWSKI',
]

names = [u'{} {}'.format(choice(firsts), choice(lasts)) for _ in range(30)]

for i in range(100):
    start_date += timedelta(days=randint(0, 5))
    dt = start_date.strftime('%d-%m-%Y')
    iban = ''.join(str(randint(0,9)) for _ in range(26))
    t_id = ''.join(choice(ascii_uppercase) for _ in range(50))
    name = choice(names)
    addr = f'{name} WOJSKA CZESKIEGO 43 BRNO'
    x = random()
    if x > .3:
        month = start_date.strftime('%m-%Y')
        desc = f'SKŁADKA CZŁONKOWSKA ZA MIESIĄC {month}'
        cost = Decimal(choice([16,32,64,128]))
    elif x > .1:
        desc = 'COS DO PLACENIA'
        cost = -Decimal(randint(256, 1024))
    else:
        desc = 'DAROWIZNA'
        cost = -Decimal(randint(256, 1024))
        cost = Decimal(randint(256, 1024))
    print(f'{dt};{cost};{addr};{desc};{iban};CEN{t_id};723')
