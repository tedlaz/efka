"""Database functions"""
import sqlite3
import os
from utils import grup


def _dict_factory(cursor, row):
    """Dictionary factory function to be used with sqlite"""
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary


def select(database, sql, howmany='one', grup_on=False):
    """Select function"""
    if not os.path.isfile(database):
        return None
    with sqlite3.connect(database) as con:
        con.row_factory = _dict_factory
        if grup_on:
            con.create_function("grup", 1, grup)
        cursor = con.cursor()
        cursor.execute(sql)
        if howmany == 'one':
            res = cursor.fetchone()
        else:
            res = cursor.fetchall()
        cursor.close()
    return res
