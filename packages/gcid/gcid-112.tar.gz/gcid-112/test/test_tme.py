# This file is placed in the Public Domain.
# pylint: disable=W0613

"time tests"


import unittest


from gcid.timer import Timer


def test(event):
    pass


class TestTime(unittest.TestCase):

    def test_timer(self):
        timer = Timer(60, test)
        self.assertEqual(type(timer), Timer)
