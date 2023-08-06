# This file is placed in the Public Domain.


"model tests"


import unittest


from gcid.model import oorzaak


class TestModel(unittest.TestCase):

    def test_oorzaaktype(self):
        self.assertEqual(type(oorzaak), type({}))
