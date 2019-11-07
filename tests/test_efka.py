from unittest import TestCase
import os
import efka
DBF = os.path.join(os.path.dirname(efka.__file__), 'osyk.sql3')


class TestEfka(TestCase):
    def test_calc_efka_01(self):
        res = efka.calc_efka(DBF, 5540, 913230, 201911, 100)['total-kost']
        self.assertEqual(res, 126.96)

    def test_calc_efka_02(self):
        res = efka.calc_efka(DBF, 55400, 913230, 201911, 100)
        self.assertTrue('error' in res)
