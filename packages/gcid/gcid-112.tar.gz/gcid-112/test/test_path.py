# This file is placed in the Public Domain.


"path tests"


import unittest


from gcid.utils import fntime


FN = "store/gcid.evt.Event/61cba0b9-29c7-4154-a6c4-10b7365b3730/2022-04-11/22:40:31.259218"


class TestPath(unittest.TestCase):


    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.259218)
