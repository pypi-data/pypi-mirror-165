# This file is placed in the Public Domain.


"scan"


import inspect
import os


from .table import Class, Commands


def scan(mod):
    "scan a module for classes and commands."
    scancls(mod)
    scancmd(mod)
    return mod


def scancls(mod):
    "scan a module for classes."
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)
    return mod


def scancmd(mod):
    "scan a module for commands."
    for _k, obj in inspect.getmembers(mod, inspect.isfunction):
        if "event" in obj.__code__.co_varnames:
            Commands.add(obj)
    return mod


def scandir(path, func):
    "scan modules in a directory, provide your import function."
    res = []
    if not os.path.exists(path):
        return res
    for _fn in os.listdir(path):
        if _fn.endswith("~") or _fn.startswith("__"):
            continue
        try:
            pname = _fn.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = _fn.split(os.sep)[-1][:-3]
        res.append(func(pname, mname))
    return res
