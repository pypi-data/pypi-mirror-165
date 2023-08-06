# This file is placed in the Public Domain.
# pylint: disable=E1101


"database tests"


import shutil
import sys
import unittest


from gcid.database import Database, fns, find, hook
from gcid.object import Object
from gcid.json import dump, load, save
from gcid.utils import fntime, gettypes, listfiles
from gcid.workdir import Wd, getpath


FN = "store/gcid.object.Object/61cba0b9-29c7-4154-a6c4-10b7365b3730/2022-04-11/22:40:31.259218"


dbs = Database()


class TestDatabase(unittest.TestCase):

    def setUp(self):
        obj = Object()
        obj.txt = "test"
        save(obj)

    def tearDown(self):
        dbs.remove("gcid.object.Object", {"txt": "test"})

    def test_constructor(self):
        database = Database()
        self.assertTrue(type(database), Database)

    def test_find(self):
        obj = Object()
        obj.txt = "test"
        save(obj)
        res = dbs.find("gcid.object.Object")
        self.assertTrue(res)

    def test_findselect(self):
        res = dbs.find("gcid.object.Object", {"txt": "test"})
        self.assertTrue(res)

    def test_lastmatch(self):
        res = dbs.match("gcid.object.Object")
        self.assertTrue(res)

    def test_dblast(self):
        res = dbs.last("gcid.object.Object")
        self.assertTrue(res)

    def test_dbremove(self):
        obj = Object()
        obj.txt = "test"
        save(obj)
        res = dbs.remove("gcid.object.Object", {"txt": "test"})
        self.setUp()
        self.assertTrue(res)

    def test_types(self):
        res = gettypes(Wd.workdir)
        self.assertTrue("gcid.object.Object" in res)

    def test_wrongfilename(self):
        fnm, _o = dbs.last("gcid.object.Object")
        shutil.copy(fnm, fnm + "bork")
        res = dbs.find("gcid.object.Object")
        self.assertTrue(res)

    def test_wrongfilename2(self):
        ftm = fntime(FN+"bork")
        self.assertTrue(ftm, 1649709631.0)

    def test_fntime(self):
        fnt = fntime(FN)
        self.assertEqual(fnt,  1649709631.259218)

    def test_fns(self):
        filenames = fns(getpath("gcid.object.Object"))
        self.assertTrue(filenames)

    def test_hook(self):
        obj = Object()
        obj.txt = "test"
        path = save(obj)
        oobj = hook(path)
        self.assertTrue("gcid.object.Object" in str(type(oobj)) and oobj.txt == "test")

    def test_listfiles(self):
        filenames = listfiles(".test")
        self.assertTrue(filenames)

    def test_all(self):
        database = Database()
        filenames = database.all("gcid.object.Object")
        self.assertTrue(filenames)

    def test_dump(self):
        obj = Object()
        obj.txt = "test"
        path = dump(obj, ".test/store/%s" % obj.__stp__)
        print(path)
        oobj = Object()
        load(oobj, path)
        print(oobj)
        sys.stdout.flush()
        self.assertEqual(oobj.txt, "test")

    def test_dbfind(self):
        objs = find("gcid.object.Object", {"txt": "test"})
        self.assertTrue(objs)
