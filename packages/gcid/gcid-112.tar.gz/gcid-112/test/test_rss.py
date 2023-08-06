# This file is placed in the Public Domain.


"rss tests"


import unittest


from gcid.rss import Fetcher


class TestRSS(unittest.TestCase):

    def test_fetcher(self):
        fetcher = Fetcher()
        self.assertEqual(type(fetcher), Fetcher)
