"""
Δοκιμαστικό module

παρουσίες

περίοδος 201901

1. Λάζαρος 10
"""
from utils import rnd
from collections import defaultdict


class Templ:
    def __init__(self, name):
        self.name = name

    def as_dic(self):
        return {
            'name': self.name,
            'poso': self.poso,
            'pososto_ergazomenoy': self.pososto_ergazomenos,
            'pososto_ergodoti': self.pososto_ergodotis,
            'pososto_synolo': self.pososto_total,
            'kratiseis_ergazomenoy': self.ergazomenos,
            'kratiseis_ergodoti': self.ergodotis,
            'kratiseis_synolo': self.total,
            'katharo_ergazomenoy': self.ergazomenos_katharo,
            'kostos_ergodoti': self.kostos_ergodoti,
            'isok': self.isok
        }


class Cost:
    def __init__(self, ergazomenos=0, ergodotis=0):
        self.ergazomenos = rnd(ergazomenos)
        self.ergodotis = rnd(ergodotis)

    @property
    def total(self):
        return rnd(self.ergazomenos + self.ergodotis)

    def as_dic(self):
        return {'ergazomenos': self.ergazomenos,
                'ergodotis': self.ergodotis,
                'total': self.total}

    def __add__(self, another):
        enos = rnd(self.ergazomenos + another.ergazomenos)
        etis = rnd(self.ergodotis + another.ergodotis)
        return Cost(enos, etis)

    def __str__(self):
        return f'{self.ergazomenos}, {self.ergodotis}, {self.total}'


class CostPercent(Cost):
    def __init__(self, poso, penos, ptotal):
        self.poso = poso
        self.pososto_ergazomenos = penos
        self.pososto_total = ptotal
        self.pososto_ergodotis = ptotal - penos
        ergazomenos = rnd(penos * poso / 100)
        ttotal = rnd(ptotal * poso / 100)
        ergodotis = rnd(ttotal - ergazomenos)
        super().__init__(ergazomenos=ergazomenos, ergodotis=ergodotis)
        self.kostos_ergodoti = rnd(self.poso + ergodotis)
        self.ergazomenos_katharo = rnd(self.poso - ergazomenos)
        kostos_ergodoti_check = rnd(self.total + self.ergazomenos_katharo)
        self.isok = self.kostos_ergodoti == kostos_ergodoti_check

    def as_dic(self):
        return {'poso': self.poso,
                'pososto_ergazomenoy': self.pososto_ergazomenos,
                'pososto_ergodoti': self.pososto_ergodotis,
                'pososto_synolo': self.pososto_total,
                'kratiseis_ergazomenoy': self.ergazomenos,
                'kratiseis_ergodoti': self.ergodotis,
                'kratiseis_synolo': self.total,
                'katharo_ergazomenoy': self.ergazomenos_katharo,
                'kostos_ergodoti': self.kostos_ergodoti,
                'isok': self.isok
                }


class Parousies:
    def __init__(self):
        self.period = 201901
        self.erg = 'Lazaros'
        self.meres_ergasias = 4
        self.meres_kanonikis_adeias = 6
        self.ores_nyxterines = 0
        self.ores_yperergasia = 0
        self.ores_argia = 0
        self.meres_argia = 0
        self.meres_astheneias = [
            {'apo': '2019-01-05', 'eos': '2019-01-08',
                'al3': 3, 'am3': 6, 'epidoma': 350},
            {'apo': '2019-01-22', 'eos': '2019-01-28',
                'al3': 3, 'am3': 4, 'epidoma': 23.45}
        ]
        self.yperories = 0

    def total_astheneia(self):
        tmeresl3 = tmeresm3 = tepidoma = 0
        for asth in self.meres_astheneias:
            tmeresl3 += asth['al3']
            tmeresm3 += asth['am3']
            tepidoma += asth['epidoma']


class Erg:
    def __init__(self, val):
        self.eponymo = val['eponymo']
        self.onoma = val['onoma']
        self.patronymo = val['patronymo']
        self.mitronymo = val['mitronymo']
        self.birthday = val['birthday']
        self.afm = val['afm']
        self.amika = val['amika']
        self.amka = val['amka']
        self.nationality = val['nationality']
        self.taftotita_typ = val['taftotita_typ']
        self.taftotita_no = val['taftotita_no']
        self.address = val['address']


class Proslipsi:
    def __init__(self, val):
        self.erg = val['erg']
        self.eid = val['eid']
        self.proslipsi_date = val['proslipsi_date']
        self.erg_type = val['erg_type']  # Μισθωτός, ημερομίσθιος, ωρομίσθιος
        self.apolysi_date = None


class SymbasiType:
    def __init__(self, val):
        self.name = val['name']
        self.meres_ana_bdomada = 5
        self.ores_ana_bdomada = 40
        self.apasxolisi_type = val['proslipsi_type']  # Πλήρης, μερική
        self.diarkeia_type = val['diarkeia_type']  # Αορίστου, ορισμένου, έργου


class Symbasi:
    def __init__(self, val):
        self.name = val['name']
        self.apasxolisi_type = val['proslipsi_type']  # Πλήρης, μερική
        self.diarkeia_type = val['diarkeia_type']  # Αορίστου, ορισμένου, έργου


if __name__ == '__main__':
    cst = {}
    cst['1'] = Cost(100, 200)
    cst['efka'] = CostPercent(103.25, 15, 45)
    cst['s'] = Cost(.3, .1)
    cst['3'] = Cost(1000, 1000)
    totals = Cost()
    for val in cst.values():
        totals += val
    print(cst['efka'].as_dic())
    aa = Templ()
