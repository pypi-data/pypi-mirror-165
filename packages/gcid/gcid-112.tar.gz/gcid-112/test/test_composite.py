# This file is placed in the Public Domain.
# pylint: disable=R0903

"composition tests"


import os
import unittest


from gcid.database import Database
from gcid.object import Object
from gcid.json import dump, load
from gcid.workdir import Wd


class Composite(Object):

    def __init__(self):
        super().__init__()
        self.dbs = Database()


class TestComposite(unittest.TestCase):

    def test_composite(self):
        composite = Composite()
        path = dump(composite, os.path.join(Wd.workdir, "compositetest"))
        composite2 = Composite()
        load(composite2, path)
        self.assertEqual(type(composite2.dbs), Database)
