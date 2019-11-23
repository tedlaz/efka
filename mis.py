"""Υπολογισμός μισθοδοσίας
    Για κάθε εργασιακή παρουσία του εργαζομένου υπολογίζονται:
    1. Μισθός περιόδου
    2. Αναλογία δώρου εορτών
    3. Αναλογία επιδόματος αδείας
    4. Αναλογία ημερών αδείας
"""
import datetime
from utils import rnd, humanize_period
import settings as s
from efka import calc_efka
from taxes import calc_tax_monthly, calc_tax_doro_pasxa_epidoma_adeias


def check_par(par):
    status = True
    st1 = {}
    if par['typ'] == 1 and par['ores'] > 0:
        st1['ores'] = 'Δεν έχει νόημα να δοθούν ώρες ενώ έχουμε μιθωτούς'
        status = False
    if par['typ'] == 2:
        if par['ores'] > 0:
            st1['ores'] = 'Οχι ώρες(ores) ενώ έχουμε ημερομισθίους'
            status = False
        if par['meres'] == 0:
            st1['meres'] = 'Για ημερομίσθιους θα πρέπει να δωθούν μέρες(meres)'
            status = False
    if par['typ'] == 3:
        if par['ores'] == 0:
            st1['ores'] = 'Για ωρομισθίους θα πρέπει να δοθούν ώρες(ores)'
            status = False
        if par['meres'] == 0:
            st1['meres'] = 'Για ωρομισθίους θα πρέπει να δοθούν μέρες(meres)'
            status = False
    return status, {'error': st1}


def calc_mis(par, osyk_db):
    """
    par: Dictionary με τις παρουσίες του εργαζομένου
    """
    par['ores'] = par.get('ores', 0)
    # Έλεγχοι για να έχουμε είτε μισθο είτε ημερομίσθιο είτε ωρομίσθιο
    valid_par, error_dic = check_par(par)
    if not valid_par:
        return error_dic
    par['month_year'] = humanize_period(par['per'])
    par['ores_nyxta'] = par.get('ores_nyxta', 0)
    par['ores_argia'] = par.get('ores_argia', 0)
    par['ores_yperergasia'] = par.get('ores_yperergasia', 0)
    par['meres_argia'] = par.get('meres_argia', 0)
    par['paidia'] = par.get('paidia', 0)
    par['mtype'] = 'Μισθοδοσία μηνός'
    fin = {'par': par}
    apo = {}
    if par['typ'] == 1:
        par['ttype'] = 'Μισθωτών'
        if par['meres'] == 0:
            par['meres'] = 25
        apo['misthos'] = par['val']
        apo['imeromisthio'] = rnd(par['val'] / s.EFKA_MERES_MHNA)
        apo['oromisthio'] = rnd(apo['imeromisthio'] *
                                s.EFKA_MERES_BDOMADA / s.EFKA_ORES_BDOMADA)
        apo['a_meres'] = rnd(par['meres'] / s.EFKA_MERES_MHNA * par['val'])
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
    elif par['typ'] == 2:
        par['ttype'] = 'Ημερομισθίων'
        apo['imeromisthio'] = par['val']
        apo['oromisthio'] = rnd(par['val'] *
                                s.EFKA_MERES_BDOMADA / s.EFKA_ORES_BDOMADA)
        apo['a_meres'] = rnd(par['meres'] * par['val'])
        apo['a_yperergasia'] = rnd(par['ores_yperergasia'] * apo['oromisthio'])
        apo['a_nyxta'] = rnd(par['ores_nyxta'] *
                             apo['oromisthio'] * s.POSOSTO_NYXTA)
        apo['a_argia_ores'] = rnd(par['ores_argia'] *
                                  apo['oromisthio'] * s.POSOSTO_ARGIA)
        apo['a_argia_meres'] = rnd(par['meres_argia'] *
                                   par['val'] * s.POSOSTO_ARGIA)
        apo['a_total'] = rnd(apo['a_meres'] + apo['a_yperergasia'] +
                             apo['a_nyxta'] + apo['a_argia_ores'] +
                             apo['a_argia_meres'])
        apo['meres_efka'] = par['meres']
        fin['apo'] = apo
    elif par['typ'] == 3:
        par['ttype'] = 'Ωρομισθίων'
        apo['oromisthio'] = par['val']
        apo['a_ores'] = rnd(par['ores'] * par['val'])
        apo['a_yperergasia'] = rnd(par['ores_yperergasia'] * par['val'])
        apo['a_nyxta'] = rnd(par['ores_nyxta'] *
                             par['val'] * s.POSOSTO_NYXTA)
        apo['a_argia_ores'] = rnd(par['ores_argia'] *
                                  par['val'] * s.POSOSTO_ARGIA)
        apo['a_total'] = rnd(apo['a_ores'] + apo['a_yperergasia'] +
                             apo['a_nyxta'] + apo['a_argia_ores'])

        apo['oresAnaMera'] = rnd(par['ores'] / par['meres'])
        apo['imeromisthio'] = rnd(apo['oresAnaMera'] * par['val'])
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
    taxes = calc_tax_monthly(year, efka['amount-after-efka'], par['paidia'])
    fin['taxes'] = taxes
    return fin


def calc_doro(par, osyk_db):
    """
        par: {
            'imeromisthio': 55,
            'total_meres': 15
        }
        dtyp: 1=Πάσχα, 2=Χριστούγεννα
    """
    # Έλεγχοι για να έχουμε είτε μισθο είτε ημερομίσθιο είτε ωρομίσθιο
    valid_par, error_dic = check_par(par)
    if not valid_par:
        return error_dic
    par['paidia'] = par.get('paidia', 0)
    par['dtyp'] = par.get('dtyp', 2)
    fin = {'par': par}
    if par['dtyp'] == 1:
        syn = 6.5
        par['mtype'] = 'Μισθοδοσία Δώρου Πάσχα'
    else:
        syn = 8
        par['mtype'] = 'Μισθοδοσία Δώρου Χριστουγέννων'
    apo = {}
    if par['type'] == 1:
        par['ttype'] = 'Μισθωτών'
        apo['a_doro'] = rnd(par['val'] / 8)
    elif par['type'] == 2:
        par['ttype'] = 'Ημερομισθίων'
        apo['a_doro'] = rnd(par['val'] *
                            par['meres'] / syn)
    elif par['type'] == 3:
        par['ttype'] = 'Ωρομισθίων'
        apo['a_doro'] = rnd(par['val'] / 8)
    else:
        fin['apo'] = {'error': 'Λάθος τύπος μισθοδοσίας'}
        return fin
    apo['a_total'] = rnd(apo['a_doro'] * s.PROSAFKSISI_DOROY)
    fin['apo'] = apo
    efka = calc_efka(osyk_db, par['kad'], par['eid'], par['per'],
                     apo['a_total'])
    fin['efka'] = efka
    year = str(par['per'])[:4]
    taxes = calc_tax_doro_pasxa_epidoma_adeias(
        year, efka['amount-after-efka'], par['paidia'])
    fin['taxes'] = taxes
    return fin


def calc_mikta_apo_kathara(kat, kad, eid, per, paidia, osyk_db):
    """Υπολογισμός μικτών απόδοχών από καθαρές αποδοχές"""
    if per == 0:
        now = datetime.datetime.now()
        per = int(now.isoformat()[:7].replace('-', ''))
    apr = kat
    i = 0
    delta = 10
    while delta > 0.001:
        if i > 100:
            break
        i += 1
        arr = {'val': apr, 'meres': 25, 'paidia': paidia, 'typ': 1,
               'per': per, 'kad': kad, 'eid': eid}
        res = calc_mis(arr, osyk_db)
        val = res['taxes']['katharo']
        delta = kat - val
        apr += delta
        arr['misthos'] = apr
    return {'kathara': kat, 'mikta': rnd(apr), 'kad': kad, 'eid': eid,
            'per': per, 'paidia': paidia, 'iterations': i}


if __name__ == '__main__':
    print(calc_mikta_apo_kathara(1600, 5241, 532030, 201911, 0, 'osyk.sql3'))
    print(calc_doro({'imeromisthio': 55, 'kad': '5540', 'dtyp': 1,
                     'eid': '348220', 'total_meres': 15,
                     'per': 201904}, 'osyk.sql3'))
