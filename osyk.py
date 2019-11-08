""" osyk.py
Functions to find osyk data (kad, eid, kpk) and calculate efka
"""
from utils import grup
from db import select


def get_kpk(database, kad, eid, period):
    """ΚΠΚ ανά kad, eid, period"""
    # kad = str(kad)
    # eid = str(eid)
    # period = str(period)
    sql = (
        "select kad.kad, kad.kadp, eid.eid, eid.eidp, kpk.kpk, kpk.kpkp, "
        "kpk.ergnos, kpk.etis, kpk.synolo, kpk.period as validFromPeriod "
        "from kad "
        "inner join kadeidkpk on kad.kad = kadeidkpk.kad "
        "inner join eid on eid.eid = kadeidkpk.eid "
        "inner join kpk on kpk.kpk = kadeidkpk.kpk "
        f"where kad.kad = '{kad}' "
        f"and eid.eid = '{eid}' "
        f"and kpk.period <= '{period}' "
        f"and '{period}' between kadeidkpk.apo and kadeidkpk.eos "
        "order by kpk.period desc"
    )
    result = select(database, sql)
    if result:
        result['period'] = str(period)
    return result


def get_eid(database, kad, period):
    """Όλες οι ειδικότητες ανά kad, period"""
    # kad = str(kad)
    # period = str(period)
    sql = (
        "select kad.kad, kad.kadp, eid.eid, eid.eidp, kpk.kpk, kpk.kpkp, "
        "kpk.ergnos, kpk.etis, kpk.synolo, max(kpk.period) as kpkmaxper "
        "from kad "
        "inner join kadeidkpk on kad.kad = kadeidkpk.kad "
        "inner join eid on eid.eid = kadeidkpk.eid "
        "inner join kpk on kpk.kpk = kadeidkpk.kpk "
        f"where kad.kad = '{kad}' "
        f"and kpk.period <= '{period}' "
        f"and '{period}' between kadeidkpk.apo and kadeidkpk.eos "
        "group by kad.kad, eid.eid "
        "order by eid.eid"
    )
    return select(database, sql, howmany="many")


def get_kad_by_name(database, name):
    """Αναζήτηση kad με την ονομασία του"""
    upname = grup(name)
    sql = f"SELECT * from kad WHERE grup(kadp) like '%{upname}%'"
    return select(database, sql, howmany='many', grup_on=True)


def get_eid_by_name(database, name):
    """Αναζήτηση eid με την ονομασία"""
    upname = grup(name)
    sql = f"SELECT * from eid WHERE grup(eidp) like '%{upname}%'"
    return select(database, sql, howmany='many', grup_on=True)


def get_kpk_history(database, kpk):
    """Όλες οι τιμές ιστορικά του kpk"""
    sql = f"SELECT * FROM kpk WHERE kpk='{kpk}' ORDER by period DESC"
    return select(database, sql, howmany='many', grup_on=False)
