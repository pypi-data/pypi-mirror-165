# This file is placed in the Public Domain.
# pylint: disable=W0613


"threads tests"


import unittest


from gcid.thread import Thread


def test(event):
    pass


class TestThreads(unittest.TestCase):

    def test_thread(self):
        thr = Thread(test, "test")
        self.assertEqual(type(thr), Thread)
