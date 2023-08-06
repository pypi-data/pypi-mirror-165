# This file is placed in the Public Domain.


"irc tests"


import unittest


from gcid.irc import IRC


class TestIRC(unittest.TestCase):

    def test_irc(self):
        irc = IRC()
        self.assertEqual(type(irc), IRC)
