from unittest import TestCase
from unittest.mock import patch
import db
import os
DBF = os.path.join(os.path.dirname(db.__file__), 'osyk.sql3')


class TestDb(TestCase):
    """
    @patch('db.listdir')
    def test_fpaths_in_dir(self, mock_listdir):
        mock_listdir.return_value = ['test1.txt', 'test2.txt']
        fpaths = db.fpaths_in_dir('some/dir')
        expected = ['some/dir/test1.txt', 'some/dir/test2.txt']
        self.assertEqual(fpaths, expected)
    """

    def test_select_01(self):
        res = db.select(DBF, "SELECT * FROM kad WHERE kad='5540'")
        self.assertEqual(len(res), 2)
