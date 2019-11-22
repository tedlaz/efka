
from utils import rnd, humanize_period
import settings as s
from efka import calc_efka
from taxes import calc_tax_monthly


def calc_mis(par, osyk_db):
    """
    par: Dictionary με τις παρουσίες του εργαζομένου
    """
    par['month_year'] = humanize_period(par['per'])
    par['ores_nyxta'] = par.get('ores_nyxta', 0)
    par['ores_argia'] = par.get('ores_argia', 0)
    par['ores_yperergasia'] = par.get('ores_yperergasia', 0)
    par['meres_argia'] = par.get('meres_argia', 0)
    fin = {'par': par}
    # Έλεγχοι για να έχουμε είτε μισθο είτε ημερομίσθιο είτε ωρομίσθιο
    if 'misthos' in par and 'imeromisthio' in par and 'oromisthio' in par:
        fin['apo'] = {'error': 'misthos, imeromisthio, oromisthio mazi'}
        return fin
    elif 'misthos' in par and 'imeromisthio' in par:
        fin['apo'] = {'error': 'misthos, imeromisthio together'}
        return fin
    elif 'misthos' in par and 'oromisthio' in par:
        fin['apo'] = {'error': 'misthos, oromisthio together'}
        return fin
    elif 'imeromisthio' in par and 'oromisthio' in par:
        fin['apo'] = {'error': 'misthos, oromisthio together'}
        return fin
    # Αφου σιγουρέψαμε ότι δεν υπάρχουν διπλοί, τριπλοί συνεχίζουμε
    apo = {}
    if 'misthos' in par:
        apo['imeromisthio'] = rnd(par['misthos'] / s.EFKA_MERES_MHNA)
        apo['oromisthio'] = rnd(apo['imeromisthio'] *
                                s.EFKA_MERES_BDOMADA / s.EFKA_ORES_BDOMADA)
        apo['a_meres'] = rnd(par['meres'] / s.EFKA_MERES_MHNA * par['misthos'])
        apo['a_yperergasia'] = rnd(par['ores_yperergasia'] * apo['oromisthio'])
        apo['a_nyxta'] = rnd(par['ores_nyxta'] *
                             apo['oromisthio'] * s.POSOSTO_NYXTA)
        apo['a_argia_ores'] = rnd(par['ores_argia'] *
                                  apo['oromisthio'] * s.POSOSTO_ARGIA)
        apo['a_argia_meres'] = rnd(par['meres_argia'] *
                                   apo['imeromisthio'] * s.POSOSTO_ARGIA)
        apo['a_total'] = rnd(apo['a_meres'] + apo['a_yperergasia'] +
                             apo['a_nyxta'] + apo['a_argia_ores'] +
                             apo['a_argia_meres'])
        apo['meres_efka'] = par['meres']
        fin['apo'] = apo
    elif 'imeromisthio' in par:
        apo['oromisthio'] = rnd(par['imeromisthio'] *
                                s.EFKA_MERES_BDOMADA / s.EFKA_ORES_BDOMADA)
        apo['a_meres'] = rnd(par['meres'] * par['imeromisthio'])
        apo['a_yperergasia'] = rnd(par['ores_yperergasia'] * apo['oromisthio'])
        apo['a_nyxta'] = rnd(par['ores_nyxta'] *
                             apo['oromisthio'] * s.POSOSTO_NYXTA)
        apo['a_argia_ores'] = rnd(par['ores_argia'] *
                                  apo['oromisthio'] * s.POSOSTO_ARGIA)
        apo['a_argia_meres'] = rnd(par['meres_argia'] *
                                   par['imeromisthio'] * s.POSOSTO_ARGIA)
        apo['a_total'] = rnd(apo['a_meres'] + apo['a_yperergasia'] +
                             apo['a_nyxta'] + apo['a_argia_ores'] +
                             apo['a_argia_meres'])
        apo['meres_efka'] = par['meres']
        fin['apo'] = apo
    elif 'oromisthio' in par:
        apo['a_ores'] = rnd(par['ores'] * par['oromisthio'])
        apo['a_yperergasia'] = rnd(par['ores_yperergasia'] * par['oromisthio'])
        apo['a_nyxta'] = rnd(par['ores_nyxta'] *
                             par['oromisthio'] * s.POSOSTO_NYXTA)
        apo['a_argia_ores'] = rnd(par['ores_argia'] *
                                  par['oromisthio'] * s.POSOSTO_ARGIA)
        apo['a_total'] = rnd(apo['a_ores'] + apo['a_yperergasia'] +
                             apo['a_nyxta'] + apo['a_argia_ores'])

        apo['oresAnaMera'] = rnd(par['ores'] / par['meres'])
        apo['imeromisthio'] = rnd(apo['oresAnaMera'] * par['oromisthio'])
        if apo['imeromisthio'] >= s.EFKA_CLASS_1:
            par['meres_efka'] = par['meres']
        else:
            par['meres_efka'] = rnd(apo['a_total'] / s.EFKA_CLASS_1, 0)

        fin['apo'] = apo
    else:
        fin['apo'] = {'error': 'Λάθος τύπος μισθοδοσίας'}
        return fin
    # Εφ όσον έχουν πάει όλα καλά μέχρι εδώ συνεχίζουμε
    efka = calc_efka(osyk_db, par['kad'], par['eid'], par['per'],
                     apo['a_total'])
    fin['efka'] = efka
    year = str(par['per'])[:4]
    taxes = calc_tax_monthly(year, efka['amount-after-efka'])
    fin['taxes'] = taxes
    return fin
