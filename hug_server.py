"""Rest API for EFKA"""
import hug
import osyk
import efka
# import mis
import taxes
from mis import calc_mis
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


@hug.get('/pmina', examples='kad=5241&eid=532030&per=201911&misthos=858')
def c_misthos(kad: hug.types.text,
              eid: hug.types.text,
              per: hug.types.number,
              misthos: hug.types.float_number,
              meres: hug.types.float_number = 25,
              oresnyxta: hug.types.float_number = 0,
              oresargia: hug.types.float_number = 0,
              meresargia: hug.types.float_number = 0,
              yperergasia: hug.types.float_number = 0
              ):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'misthos': misthos, 'meres': meres,
        'ores_nyxta': oresnyxta, 'ores_argia': oresargia,
        'meres_argia': meresargia, 'ores_yperergasia': yperergasia
    }
    return calc_mis(adi, DB_OSYK)


@hug.get('/pmera', examples='kad=5241&eid=532030&per=201911&imeromisthio=34.32&meres=25')
def c_imeromistio(kad: hug.types.text,
                  eid: hug.types.text,
                  per: hug.types.number,
                  imeromisthio: hug.types.float_number,
                  meres: hug.types.float_number,
                  oresnyxta: hug.types.float_number = 0,
                  oresargia: hug.types.float_number = 0,
                  meresargia: hug.types.float_number = 0,
                  yperergasia: hug.types.float_number = 0
                  ):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'imeromisthio': imeromisthio,
        'meres': meres, 'ores_nyxta': oresnyxta, 'ores_argia': oresargia,
        'meres_argia': meresargia, 'ores_yperergasia': yperergasia
    }
    return calc_mis(adi, DB_OSYK)


@hug.get('/pora', examples='kad=5241&eid=532030&per=201911&oromisthio=5.15&ores=166.6&meres=25')
def c_oromistio(kad: hug.types.text,
                eid: hug.types.text,
                per: hug.types.number,
                oromisthio: hug.types.float_number,
                ores: hug.types.float_number,
                meres: hug.types.number,
                oresnyxta: hug.types.float_number = 0,
                oresargia: hug.types.float_number = 0,
                yperergasia: hug.types.float_number = 0
                ):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'oromisthio': oromisthio,
        'ores': ores, 'ores_nyxta': oresnyxta, 'ores_argia': oresargia,
        'meres': meres, 'ores_yperergasia': yperergasia
    }
    return calc_mis(adi, DB_OSYK)


@hug.get('/taxmonth', examples='year=2019&income=719.43')
def c_tax_monthly(year: hug.types.number, income: hug.types.float_number):
    return taxes.calc_tax_monthly(year, income)
