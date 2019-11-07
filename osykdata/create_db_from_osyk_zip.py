"""Create sqlite database file from osyk.zip file
Steps:
    1. Download osyk.zip file from:
        https://www.efka.gov.gr/el/ergodotes/entypa-downloads

    2. Unzip and rename files to kad.txt, eid.txt, kpk.txt, kek.txt

    3. Run create_database(<Database name>) and CHECK FOR ERRORS
"""
import sqlite3


def fix(some_text):
    ftxt = some_text.replace(',', ', ')
    ftxt = ftxt.replace('-', ' - ')
    ftxt = ftxt.replace('( ', '(')
    ftxt = ftxt.replace(' )', ')')
    ftxt = ftxt.replace(':', ': ')
    ftxt = ' '.join(ftxt.split())  # To remove more than one spaces
    return ftxt


def parse_kad(fname='kad.txt'):
    with open(fname, encoding='CP1253') as fil:
        errors = 0
        lkad = []
        for line in fil:
            if len(line) < 6:
                continue
            try:
                kad, kadp = (fld.strip() for fld in line.split(';'))
                lkad.append((kad, fix(kadp)))
            except ValueError:
                print('-->', line, len(line))
                errors += 1
    print(f'KAD Total Errors: {errors}')
    return lkad


def parse_eid(fname='eid.txt'):
    with open(fname, encoding='CP1253') as fil:
        errors = 0
        leid = []
        for line in fil:
            if len(line) < 6:
                continue
            try:
                eid, eidp = (fld.strip() for fld in line.split(';'))
                leid.append((eid, fix(eidp)))
            except ValueError:
                print('-->', line, len(line))
                errors += 1
    print(f'EID Total Errors: {errors}')
    return leid


def parse_kpk(fname='kpk.txt'):
    with open(fname, encoding='CP1253') as fil:
        errors = 0
        lkpk = []
        half_vals = None
        for line in fil:
            if len(line) < 6:
                continue
            try:
                if line.startswith(';'):
                    line = line[1:]
                vals = line.split(';')
                if len(vals) < 6 and not half_vals:
                    half_vals = vals
                    continue
                elif half_vals:
                    vals = half_vals + vals
                    half_vals = None
                if len(vals) != 6:
                    print(vals)
                    return
                kpk, kpkp, enos, etis, total, per = (
                    fld.strip() for fld in vals)
                enos = float(enos)
                etis = float(etis)
                total = float(total)
                lkpk.append((kpk, fix(kpkp), enos, etis, total, per))
            except ValueError:
                print('-->', line, len(line))
                errors += 1
    print(f'KPK Total Errors: {errors}')
    return lkpk


def parse_kek(fname='kek.txt'):
    with open(fname, encoding='CP1253') as fil:
        errors = 0
        lkek = []
        for line in fil:
            if len(line) < 6:
                continue
            try:
                kad, eid, kpk, apo, eos = (fld.strip()
                                           for fld in line.split(';'))
                lkek.append((kad, eid, kpk, apo, eos))
            except ValueError:
                print('-->', line, len(line))
                errors += 1
    print(f'KEK Total Errors: {errors}')
    return lkek


def create_database(dbf):
    conn = sqlite3.connect(dbf)
    c = conn.cursor()
    c.execute('CREATE TABLE kad (kad, kadp)')
    c.execute('CREATE TABLE eid (eid, eidp)')
    c.execute('CREATE TABLE kpk (kpk, kpkp, ergnos, etis, synolo, period)')
    c.execute('CREATE TABLE kadeidkpk (kad, eid, kpk, apo, eos)')
    c.executemany('INSERT INTO kad VALUES(?,?)', parse_kad())
    c.executemany('INSERT INTO eid VALUES(?,?)', parse_eid())
    c.executemany('INSERT INTO kpk VALUES(?,?,?,?,?,?)', parse_kpk())
    c.executemany('INSERT INTO kadeidkpk VALUES(?,?,?,?,?)', parse_kek())
    conn.commit()
    c.close()
    if dbf == ':memory:':
        return conn
    conn.close()
    return None


def test_memory_db():
    mdb = create_database(':memory:')
    cursor = mdb.cursor()
    cursor.execute("SELECT * FROM kpk WHERE kpk='101'")
    print(cursor.fetchall())
    cursor.close()
    mdb.close()


if __name__ == '__main__':
    create_database('osyk.sql3')
    # test_memory_db()
