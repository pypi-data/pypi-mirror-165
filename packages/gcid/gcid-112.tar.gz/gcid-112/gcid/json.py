# This file is placed in the Public Domain.


"json"


import datetime
import json
import os


from json import JSONDecoder, JSONEncoder


from .object import Object, update
from .utils import cdir
from .workdir import Wd, getpath


class ObjectDecoder(JSONDecoder):

    "decode string to object."

    def  __init__(self, *args, **kwargs):
        ""
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        "do the decoding."
        value = json.loads(s)
        obj = Object()
        update(obj, value)
        return obj


    def raw_decode(self, s, *args, **kwargs):
        "deconding of raw string."
        return JSONDecoder.raw_decode(self, s, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    "encode to object from string."

    def  __init__(self, *args, **kwargs):
        ""
        JSONEncoder.__init__(self, *args, **kwargs)


    def encode(self, o):
        "encode object to string."
        return JSONEncoder.encode(self, o)


    def default(self, o):
        "return default string for object."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))):
            return o
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


    def iterencode(self, o, *args, **kwargs):
        "iterate while encoding."
        return JSONEncoder.iterencode(self, o, *args, **kwargs)


def dump(obj, opath):
    "dump object to file."
    cdir(opath)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            obj.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return obj.__stp__


def dumps(obj):
    "return json string."
    return json.dumps(obj, cls=ObjectEncoder)


def load(obj, opath):
    "load object from path."
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)
    obj.__stp__ = stp


def loads(jss):
    "return object from json string."
    return json.loads(jss, cls=ObjectDecoder)


def save(obj):
    "save an object to disk."
    prv = os.sep.join(obj.__stp__.split(os.sep)[:2])
    obj.__stp__ = os.path.join(
                       prv,
                       os.sep.join(str(datetime.datetime.now()).split())
                      )
    opath = getpath(obj.__stp__)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return obj.__stp__
