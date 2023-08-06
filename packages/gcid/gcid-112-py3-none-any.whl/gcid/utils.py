# This file is placed in the Public Domain.
# pylint: disable=W0613


"utility"


import os
import pathlib
import time
import types
import _thread


dblock = _thread.allocate_lock()


def locked(lock):

    "locking decorator (provide the lock)."

    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        return lockedfunc

    return lockeddec


def cdir(path):
    "create directory."
    if os.path.exists(path):
        return
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def elapsed(seconds, short=True):
    "elapsed number of seconds to a string."
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def fntime(daystr):
    "create time from a file path."
    after = 0
    daystr = " ".join(daystr.split(os.sep)[-2:])
    if "." in daystr:
        daystr, after = daystr.rsplit(".")
    tme = time.mktime(time.strptime(daystr, "%Y-%m-%d %H:%M:%S"))
    if after:
        try:
            tme = tme + float(".%s"% after)
        except ValueError:
            pass
    return tme


def getname(obj):
    "return full qualified name of a object."
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def listfiles(workdir):
    "list files in store."
    path = os.path.join(workdir, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def otype(obj):
    "return type of a object."
    return str(type(obj)).split()[-1][1:-2]


def printable(obj, args, skip="_", empty=False, plain=False):
    "return printable string of an object."
    res = []
    try:
        keyz = args.split(",")
    except (AttributeError, TypeError, ValueError):
        keyz = args
    for key in keyz:
        try:
            skips = skip.split(",")
            if key in skips or key.startswith("_"):
                continue
        except (TypeError, ValueError):
            pass
        value = getattr(obj, key, None)
        if not value and not empty:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    return " ".join(res)


def spl(txt):
    "split comma seperated string into list."
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def gettypes(path):
    "return types in store."
    print(path)
    path = os.path.join(path, "store")
    print(path)
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))
