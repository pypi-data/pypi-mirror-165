# This file is placed in the Public Domain.
# pylint: disable=R0903


"default"


from .object import Object


class Default(Object):

    "provides returning a default value."

    def __getattr__(self, key):
        return self.__dict__.get(key, "")
