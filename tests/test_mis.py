from unittest import TestCase
import os
import mis
DBF = os.path.join(os.path.dirname(mis.__file__), 'osyk.sql3')


class TestMis(TestCase):
    def test_mis(self):
        # mis.calc_mis(DBF, {
        #     'per': 201911,
        #     'typ': 1,
        #     'kad': 5540,
        #     'eid': 913230,
        #     'apod': 1000.36,
        #     'meres-ika': 25,
        #     'meres': 10,
        # })
        mis.calc_mis(DBF, {
            'per': 201911,
            'typ': 2,
            'kad': 5540,
            'eid': 348220,
            'apod': 55,
            'meres': 3,
        })
