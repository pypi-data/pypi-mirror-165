# This file is placed in the Public Domain.


"composition tests"


import unittest


from gcid.handler import Handler


class TestHandler(unittest.TestCase):

    def test_handler(self):
        hdl = Handler()
        self.assertEqual(type(hdl), Handler)
