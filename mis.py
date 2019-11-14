"""
typ : 1=μισθός, 2=ημερομίσθιο, 3=ωρομίσθιο
"""
from utils import rnd
from efka import calc_efka
MISTHOS, IMEROMISTHIO, OROMISTHIO = 1, 2, 3
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


def calc_mis(dbf, par, typ='normal'):
    """Υπολογισμός μισθοδοσίας
       par: {'per': 201903,
             'kad': 5540,
             'eid': 913230,
             'typ': 1,
             'apod': 850.43,
             'meres-ika': 25,
             'meres': 10,
       }
    """
    par['perh'] = humanize_period(par['per'])
    if par['typ'] == MISTHOS:
        par['apod-periodoy'] = rnd(
            par['meres'] / par['meres-ika'] * par['apod'])

    elif par['typ'] == IMEROMISTHIO:
        par['apod-periodoy'] = rnd(par['meres'] * par['apod'])

    elif par['typ'] == OROMISTHIO:
        pass
    else:
        raise ValueError(f"Not legal par type={par['typ']}")
    defka = calc_efka(dbf, par['kad'], par['eid'],
                      par['per'], par['apod-periodoy'])
    final = {**par, **defka}
    return final
