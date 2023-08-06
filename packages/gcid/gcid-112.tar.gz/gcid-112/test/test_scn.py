# This file is placed in the Public Domain.


"composition tests"


import unittest


from gcid.scan import scan
from gcid.table import Commands


from gcid import irc


class TestScan(unittest.TestCase):

    def test_composite(self):
        scan(irc)
        self.assertTrue("cfg" in Commands.cmds)
