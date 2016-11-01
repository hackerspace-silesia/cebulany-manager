#!/usr/bin/env python
# encoding: utf-8
from datetime import date, timedelta
from random import randint, choice, random
from decimal import Decimal
start_date = date(2015, 1, 1)
money = Decimal('2000.00')

firsts = [
    u'MAREK', u'DAREK', u'HENRYK', u'MICHAŁ', u'ZYGFRYD', u'PAWEŁ', u'STANISŁAW',
    u'ŁUKASZ', u'DAWID', u'FILIP', u'OKTAWIAN', u'BŁAŻEJ', u'BARTUŚ',
]
lasts = [
    'KOWALSKI', 'OWCZAREK', 'MARKOWSKI', 'PROSTACKI', 'RYBSKI', 'STAROWSKI',
    'CZARNOWSKI', 'WARSZAWSKI', 'NOWAK', 'CHOLERAWIECKI', 'TESTOWSKI',
]

names = [u'{} {}'.format(choice(firsts), choice(lasts)) for _ in range(30)]

print('Data operacji,Opis,Kwota transakcji,Saldo po operacji'.encode('windows-1250'))

for i in range(1000):
    start_date += timedelta(days=randint(0, 2))
    dt = start_date.strftime('%Y-%m-%d')
    rev_dt = start_date.strftime('%d-%m-%Y')
    iban = ''.join(str(randint(0,9)) for _ in range(26))
    x = random()
    if x > .2:
        desc = (
            u'PRZELEW UZNANIOWY (NADANO {dt})'
            u' SKŁADKA CZŁONKOWSKA ZA MIESIĄC {month}'
            u'  {name}'
            u'  WOJSKA CZESKIEGO 43 BRNO {iban}'
        ).format(
            dt=rev_dt,
            month=start_date.strftime('%m-%Y'),
            iban=iban,
            name=choice(names),
        )
        cost = Decimal(choice([16,32,64,128]))
    elif x > .1:
        desc = (
            u'PRZELEW OBCIĄŻENIOWY (NADANO {dt})'
            u' COS DO PLACENIA'
            u'  {name}'
            u'  WOJSKA CZESKIEGO 43 BRNO {iban}'
        ).format(
            dt=rev_dt,
            iban=iban,
            name=choice(['UPC', 'TAURON', 'LOKAL'])
        )
        cost = -Decimal(randint(256, 1024))
    else:
        desc = (
            u'PRZELEW UZNANIOWY (NADANO {dt})'
            u' DAROWIZNA'
            u'  {name}'
            u'  WOJSKA CZESKIEGO 43 BRNO {iban}'
        ).format(
            dt=rev_dt,
            iban=iban,
            name=choice(names),
        )
        cost = Decimal(randint(256, 1024))
    money -= cost
    ss = u'{dt},{desc},{cost},{money}'.format(
        dt=dt,
        desc=desc,
        cost=cost,
        money=money,
    )
    print(ss.encode('windows-1250'))
print('\r')
