"""Rest API for EFKA"""
import datetime
import hug
import osyk
import efka
import taxes
from mis import calc_mis, calc_mikta_apo_kathara, calc_doro, calc_ea
DB_OSYK = 'osyk.sql3'


@hug.get('/kpk', examples='kad=5540&eid=913230&period=201911')
@hug.local()
def gkpk(kad: hug.types.text,
         eid: hug.types.text,
         period: hug.types.number):
    """Get kpk given kad, eid and period"""
    return osyk.get_kpk(DB_OSYK, kad, eid, period)


@hug.get('/find_kad', examples='name=μπαρ')
@hug.local()
def find_kad(name: hug.types.text):
    """Search for kad by name"""
    return osyk.get_kad_by_name(DB_OSYK, name)


@hug.get('/find_eid', examples='name=λαντζ')
@hug.local()
def find_eid(name: hug.types.text):
    """Search for eid by name"""
    return osyk.get_eid_by_name(DB_OSYK, name)


@hug.get('/eidperkad', examples='kad=5540&period=201911')
@hug.local()
def eidperkad(kad: hug.types.text, period: hug.types.number):
    """For given kad and period, find all eid"""
    return osyk.get_eid(DB_OSYK, kad, period)


@hug.get('/kpkhistory', examples='kpk=101')
@hug.local()
def kpkhistory(kpk: hug.types.text):
    """Get all records for a given kpk"""
    return osyk.get_kpk_history(DB_OSYK, kpk)


@hug.get('/efka', examples='kad=5540&eid=913230&period=201911&amount=869.72')
@hug.local()
def calc_efka(kad: hug.types.text,
              eid: hug.types.text,
              period: hug.types.number,
              amount: hug.types.float_number):
    """Calculate efka given kad, eid, period and amount"""
    return efka.calc_efka(DB_OSYK, kad, eid, period, amount)


@hug.get('/payroll', examples='kad=5241&eid=532030&per=201911&typ=1&val=858')
def c_apod(kad: hug.types.text,
           eid: hug.types.text,
           per: hug.types.number,
           typ: hug.types.number,
           val: hug.types.float_number,
           meres: hug.types.float_number = 0,
           ores: hug.types.float_number = 0,
           oresnyxta: hug.types.float_number = 0,
           oresargia: hug.types.float_number = 0,
           meresargia: hug.types.float_number = 0,
           yperergasia: hug.types.float_number = 0,
           paidia: hug.types.number = 0
           ):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'typ': typ, 'val': val,
        'meres': meres, 'ores_nyxta': oresnyxta, 'ores_argia': oresargia,
        'meres_argia': meresargia, 'ores_yperergasia': yperergasia,
        'paidia': paidia, 'ores': ores
    }
    return calc_mis(adi, DB_OSYK)


@hug.get('/doro', examples='kad=5241&eid=532030&per=201912&typ=2&val=858&dtyp=2')
def c_doro(kad: hug.types.text,
           eid: hug.types.text,
           per: hug.types.number,
           typ: hug.types.number,
           val: hug.types.float_number,
           dtyp: hug.types.number,
           meres: hug.types.float_number = 0,
           paidia: hug.types.number = 0
           ):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'typ': typ, 'val': val,
        'meres': meres, 'doro_typ': dtyp, 'paidia': paidia
    }
    return calc_doro(adi, DB_OSYK)


@hug.get('/ea', examples='kad=5241&eid=532030&per=201912&typ=1&val=858&meres=25')
def c_doro(kad: hug.types.text,
           eid: hug.types.text,
           per: hug.types.number,
           typ: hug.types.number,
           val: hug.types.float_number,
           meres: hug.types.float_number = 0,
           paidia: hug.types.number = 0
           ):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'typ': typ, 'val': val,
        'meres': meres, 'paidia': paidia
    }
    return calc_ea(adi, DB_OSYK)


@hug.get('/taxmonth', examples='year=2019&income=719.43')
def c_tax_monthly(year: hug.types.number, income: hug.types.float_number):
    return taxes.calc_tax_monthly(year, income)


@hug.get('/mikta', examples='kathara=1600&kad=5241&eid=532030&per=201911')
def c_mikta_apo_kathara(kathara: hug.types.float_number,
                        kad: hug.types.text,
                        eid: hug.types.text,
                        per: hug.types.number = 0,
                        paidia: hug.types.number = 0
                        ):
    return calc_mikta_apo_kathara(kathara, kad, eid, per, paidia, DB_OSYK)
