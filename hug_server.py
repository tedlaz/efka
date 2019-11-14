"""Rest API for EFKA"""
import hug
import osyk
import efka
import mis
DBF = 'osyk.sql3'


@hug.get('/kpk', examples='kad=5540&eid=913230&period=201911')
@hug.local()
def gkpk(kad: hug.types.text,
         eid: hug.types.text,
         period: hug.types.number):
    """Get kpk given kad, eid and period"""
    return osyk.get_kpk(DBF, kad, eid, period)


@hug.get('/find_kad', examples='name=μπαρ')
@hug.local()
def find_kad(name: hug.types.text):
    """Search for kad by name"""
    return osyk.get_kad_by_name(DBF, name)


@hug.get('/find_eid', examples='name=λαντζ')
@hug.local()
def find_eid(name: hug.types.text):
    """Search for eid by name"""
    return osyk.get_eid_by_name(DBF, name)


@hug.get('/eidperkad', examples='kad=5540&period=201911')
@hug.local()
def eidperkad(kad: hug.types.text, period: hug.types.number):
    """For given kad and period, find all eid"""
    return osyk.get_eid(DBF, kad, period)


@hug.get('/kpkhistory', examples='kpk=101')
@hug.local()
def kpkhistory(kpk: hug.types.text):
    """Get all records for a given kpk"""
    return osyk.get_kpk_history(DBF, kpk)


@hug.get('/efka', examples='kad=5540&eid=913230&period=201911&amount=869.72')
@hug.local()
def calc_efka(kad: hug.types.text,
              eid: hug.types.text,
              period: hug.types.number,
              amount: hug.types.float_number):
    """Calculate efka given kad, eid, period and amount"""
    return efka.calc_efka(DBF, kad, eid, period, amount)


@hug.get('/mis', examples='kad=5540&eid=348220&per=201911&typ=2&apod=55&meres=3')
def c_mis(kad: hug.types.text,
          eid: hug.types.text,
          per: hug.types.number,
          typ: hug.types.number,
          apod: hug.types.float_number,
          meres: hug.types.float_number):
    adi = {
        'kad': kad, 'eid': eid, 'per': per, 'typ': typ, 'apod': apod,
        'meres-ika': 25, 'meres': meres
    }
    return mis.calc_mis(DBF, adi)
