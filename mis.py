"""
typ : 1=μισθός, 2=ημερομίσθιο, 3=ωρομίσθιο
"""
from utils import rnd, humanize_period
from efka import calc_efka
MISTHOS, IMEROMISTHIO, OROMISTHIO = 1, 2, 3


def calc_mis(dbf, par, typ='normal'):
    """Υπολογισμός μισθοδοσίας
       par: {'per': 201903,
             'kad': 5540,
             'eid': 913230,
             'typ': 1,
             'apod': 850.43,
             'meres': 10,
       }
    """
    par['perh'] = humanize_period(par['per'])
    par['meres-bdomada'] = par.get('meres-bdomada', 6)
    par['ores-bdomada'] = par.get('ores-bdomada', 40)

    par['pososto-nyxta'] = 0.25
    par['pososto-argia'] = 0.75
    if par['typ'] == MISTHOS:
        par['meres-ika'] = par.get('meres-ika', 25)
        par['ores-nyxta'] = par.get('ores-nyxta', 0)
        par['meres-argia'] = par.get('meres-argia', 0)
        par['ores-argia'] = par.get('ores-argia', 0)
        par['imeromisthio'] = rnd(par['apod'] / par['meres-ika'])
        par['oromisthio'] = rnd(par['imeromisthio'] *
                                par['meres-bdomada'] / par['ores-bdomada'])
        par['apod-normal'] = rnd(
            par['meres'] / par['meres-ika'] * par['apod'])

    elif par['typ'] == IMEROMISTHIO:
        par['ores-nyxta'] = par.get('ores-nyxta', 0)
        par['meres-argia'] = par.get('meres-argia', 0)
        par['ores-argia'] = par.get('ores-argia', 0)
        par['imeromisthio'] = par['apod']
        par['oromisthio'] = rnd(par['imeromisthio'] *
                                par['meres-bdomada'] / par['ores-bdomada'])
        par['apod-normal'] = rnd(par['meres'] * par['apod'])

    elif par['typ'] == OROMISTHIO:
        par['ores-nyxta'] = par.get('ores-nyxta', 0)
        par['meres-argia'] = par.get('meres-argia', 0)
        if par['meres-argia'] != 0:
            raise ValueError('Δεν μπορεί ο ωρομίσθιος να έχει μέρες αργίας')
        par['ores-argia'] = par.get('ores-argia', 0)
        par['imeromisthio'] = 0
        par['oromisthio'] = par['apod']
        par['apod-normal'] = rnd(par['ores'] * par['oromisthio'])

    else:
        raise ValueError(f"Not legal par type={par['typ']}")
    par['pros-nyxta'] = rnd(par['ores-nyxta'] *
                            par['oromisthio'] * par['pososto-nyxta'])
    par['pros-argia-meres'] = rnd(par['meres-argia']
                                  * par['imeromisthio'] * par['pososto-argia'])
    par['pros-argia-ores'] = rnd(par['ores-argia']
                                 * par['oromisthio'] * par['pososto-argia'])
    par['apod-periodoy'] = par['apod-normal'] + par['pros-nyxta'] + \
        par['pros-argia-meres'] + par['pros-argia-ores']
    defka = calc_efka(dbf, par['kad'], par['eid'],
                      par['per'], par['apod-periodoy'])
    final = {**par, **defka}
    return final


def calc_misthos(dbf, par):
    """Υπολογισμός μηνιαίων αποδοχών μισθωτών
        par: {
            'per': 201903,
            'kad': 5540,
            'eid': 913230,
            'misthos': 864.25,
            'meres': 25  (default 25)
        }

    """
    par['month_year'] = humanize_period(par['per'])
    par['misth_type'] = 'Μισθοδοσία μισθωτών'
    par['minasmeres'] = par.get('minasmeres', 25)
    par['bdommeres'] = par.get('bdommeres', 6)
    par['bdomores'] = par.get('bdomores', 40)
    par['nyxta%'] = 0.25
    par['argia%'] = 0.75
    par['oresnyxta'] = par.get('oresnyxta', 0)
    par['oresargia'] = par.get('oresargia', 0)
    par['meresargia'] = par.get('meresargia', 0)
    par['imeromistio'] = rnd(par['misthos'] / par['minasmeres'])
    par['oromistio'] = rnd(par['imeromistio'] *
                           par['bdommeres'] / par['bdomores'])
    if par['meres'] == par['minasmeres']:
        par['apodnormal'] = rnd(par['misthos'])
    else:
        par['apodnormal'] = rnd(
            par['meres'] / par['minasmeres'] * par['misthos'])
    par['prosnyxta'] = rnd(par['oresnyxta'] *
                           par['oromistio'] * par['nyxta%'])
    par['prosargiaores'] = rnd(par['oresargia']
                               * par['oromistio'] * par['argia%'])
    par['prosargiameres'] = rnd(par['meresargia']
                                * par['imeromistio'] * par['argia%'])
    par['apodperiodoy'] = rnd(
        par['apodnormal'] + par['prosnyxta']
        + par['prosargiameres'] + par['prosargiaores'])
    par['meresEFKA'] = par['meres']
    defka = calc_efka(dbf, par['kad'], par['eid'],
                      par['per'], par['apodperiodoy'])
    final = {**par, **defka}
    return final


def calc_imeromistio(dbf, par):
    """Υπολογισμός μηνιαίων αποδοχών ημερομισθίων
        par: {
            'per': 201903,
            'kad': 5540,
            'eid': 913230,
            'imeromistio': 25.44,
            'meres': 26
        }

    """
    par['month_year'] = humanize_period(par['per'])
    par['misth_type'] = 'Μισθοδοσία ημερομισθίων'
    par['bdommeres'] = par.get('bdommeres', 6)
    par['bdomores'] = par.get('bdomores', 40)
    par['nyxta%'] = 0.25
    par['argia%'] = 0.75
    par['oresnyxta'] = par.get('oresnyxta', 0)
    par['oresargia'] = par.get('oresargia', 0)
    par['meresargia'] = par.get('meresargia', 0)
    par['oromistio'] = rnd(par['imeromistio'] *
                           par['bdommeres'] / par['bdomores'])
    par['apodnormal'] = rnd(par['imeromistio'] * par['meres'])
    par['prosnyxta'] = rnd(par['oresnyxta'] *
                           par['oromistio'] * par['nyxta%'])
    par['prosargiaores'] = rnd(par['oresargia']
                               * par['oromistio'] * par['argia%'])
    par['prosargiameres'] = rnd(par['meresargia']
                                * par['imeromistio'] * par['argia%'])
    par['apodperiodoy'] = rnd(
        par['apodnormal'] + par['prosnyxta']
        + par['prosargiameres'] + par['prosargiaores'])
    par['meresEFKA'] = par['meres']
    defka = calc_efka(dbf, par['kad'], par['eid'],
                      par['per'], par['apodperiodoy'])
    final = {**par, **defka}
    return final


def calc_oromistio(dbf, par):
    """Υπολογισμός μηνιαίων αποδοχών ωρομισθίων
        par: {
            'per': 201903,
            'kad': 5540,
            'eid': 913230,
            'oromistio': 5.7,
            'ores': 22,
            'meres': 20
        }

    """
    par['month_year'] = humanize_period(par['per'])
    par['misth_type'] = 'Μισθοδοσία ωρομισθίων'
    par['bdommeres'] = par.get('bdommeres', 6)
    par['bdomores'] = par.get('bdomores', 40)
    par['nyxta%'] = 0.25
    par['argia%'] = 0.75
    par['class1'] = 11.06
    par['oresnyxta'] = par.get('oresnyxta', 0)
    par['oresargia'] = par.get('oresargia', 0)
    par['apodnormal'] = rnd(par['oromistio'] * par['ores'])
    par['prosnyxta'] = rnd(par['oresnyxta'] *
                           par['oromistio'] * par['nyxta%'])
    par['prosargiaores'] = rnd(par['oresargia']
                               * par['oromistio'] * par['argia%'])
    par['apodperiodoy'] = rnd(
        par['apodnormal'] + par['prosnyxta'] + par['prosargiaores']
    )
    par['oresAnaMera'] = rnd(par['ores'] / par['meres'])
    par['imeromistio'] = rnd(par['oresAnaMera'] * par['oromistio'])
    if par['imeromistio'] >= par['class1']:
        par['meresEFKA'] = par['meres']
    else:
        par['meresEFKA'] = rnd(par['apodperiodoy'] / par['class1'], 0)
    defka = calc_efka(dbf, par['kad'], par['eid'],
                      par['per'], par['apodperiodoy'])
    final = {**par, **defka}
    return final
