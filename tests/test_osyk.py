from unittest import TestCase
import os
import osyk
DBF = os.path.join(os.path.dirname(osyk.__file__), 'osyk.sql3')


class TestOsyk(TestCase):

    def test_get_kpk_01(self):
        res = osyk.get_kpk(DBF, 5540, 913230, 201906)['synolo']
        self.assertEqual(res, 46.16)

    def test_get_kpk_02(self):
        res = osyk.get_kpk(DBF, 5540, 913230, 201905)['synolo']
        self.assertEqual(res, 46.66)

    def test_get_eid_01(self):
        res = osyk.get_eid(DBF, 5540, 201911)
        self.assertEqual(len(res), 65)

    def test_get_kad_by_name_01(self):
        res = osyk.get_kad_by_name(DBF, 'εστιατόΡΙΑ')[0]['kad']
        self.assertEqual(res, '5530')

    def test_get_eid_by_name_01(self):
        res = osyk.get_eid_by_name(DBF, 'λαντζ')[0]['eid']
        self.assertEqual(res, '913230')

    def test_get_kpk_history_01(self):
        res = osyk.get_kpk_history(DBF, 101)
        self.assertEqual(len(res), 7)
