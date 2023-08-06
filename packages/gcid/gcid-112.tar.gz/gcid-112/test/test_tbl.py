# This file is placed in the Public Domain.


"table tests"


import unittest


from gcid.table import Table



class TestTable(unittest.TestCase):

    def test_table(self):
        table = Table()
        self.assertEqual(type(table), Table)
