# This file is placed in the Public Domain.


"workdir"


import os


class Wd:

    "working directory."

    workdir = ""

    @staticmethod
    def get():
        "return working directory."
        return Wd.workdir

    @staticmethod
    def set(val):
        "set working directory."
        Wd.workdir = val


def getpath(path):
    "return a store's path."
    return os.path.join(Wd.workdir, "store", path)
