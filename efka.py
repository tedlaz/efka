"""EFKA functions"""
from utils import rnd
from osyk import get_kpk


def calc_efka(database, kad, eid, per, amount):
    """Calculate efka"""
    kpk = get_kpk(database, kad, eid, per)
    if kpk is None:
        return {
            'error': 'Δεν βρέθηκε ΚΑΔ για το συνδυασμό kad, eid, per',
            'kad': kad, 'eid': eid, 'per': per
        }
    penos = kpk['ergnos'] / 100.0
    ptota = kpk['synolo'] / 100.0
    kpk['amount'] = amount
    kpk['efka-ergazomenos'] = rnd(amount * penos, 2)
    kpk['efka-total'] = rnd(amount * ptota, 2)
    kpk['efka-ergodotis'] = rnd(kpk['efka-total'] -
                                kpk['efka-ergazomenos'], 2)
    kpk['amount-after-efka'] = rnd(amount - kpk['efka-ergazomenos'], 2)
    kpk['total-kost'] = rnd(amount + kpk['efka-ergodotis'], 2)
    kpk['total-kost-check'] = rnd(kpk['efka-total'] +
                                  kpk['amount-after-efka'], 2)
    return kpk
