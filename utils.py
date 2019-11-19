"""Varius utilities"""
import math


def rnd(number, decimals=2):
    """Round half up float number"""
    multiplier = 10 ** decimals
    return math.floor(number * multiplier + 0.5) / multiplier


def grup(txtval):
    """Trasforms a string to uppercase special for Greek comparison

    :param txtval:
    :return:
    """
    txtval = '' if txtval is None else str(txtval).upper()
    ar1 = "ΆΈΉΊΌΎΏΪΫ"
    ar2 = "ΑΕΗΙΟΥΩΙΥ"
    adi = dict(zip(ar1, ar2))
    return ''.join([adi.get(letter, letter.upper()) for letter in txtval])


MON = [
    'Ιανουάριος', 'Φεβρουάριος', 'Μάρτιος', 'Απρίλιος', 'Μάϊος', 'Ιούνιος',
    'Ιούλιος', 'Αύγουστος', 'Σεπτέμβριος', 'Οκτώβριος', 'Νοέμβριος',
    'Δεκέμβριος'
]


def humanize_period(period):
    per = str(period)
    assert len(per) == 6
    year = per[:4]
    month = int(per[4:])
    return f'{MON[month-1]} {year}'
