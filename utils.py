"""Varius utilities"""
import math


def rnd(number, decimals=0):
    """Round half up float number"""
    multiplier = 10 ** decimals
    return math.floor(number * multiplier + 0.5) / multiplier


def grup(txtval):
    """Trasforms a string to uppercase special for Greek comparison

    :param txtval:
    :return:
    """
    txtval = '' if txtval is None else str(txtval).upper()
    ar1 = "ΆΈΉΊΌΎΏΪΫ"
    ar2 = "ΑΕΗΙΟΥΩΙΥ"
    adi = dict(zip(ar1, ar2))
    return ''.join([adi.get(letter, letter.upper()) for letter in txtval])
