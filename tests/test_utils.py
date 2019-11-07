from unittest import TestCase
import utils


class TestUtils(TestCase):
    def test_rnd_01(self):
        self.assertEqual(utils.rnd(10.555, 2), 10.56)

    def test_rnd_02(self):
        self.assertEqual(utils.rnd(10.554, 2), 10.55)

    def test_grup_01(self):
        st1 = 'αάβΒιίϊεέΊ'
        st2 = 'ΑΑΒΒΙΙΙΕΕΙ'
        self.assertEqual(utils.grup(st1), st2)
