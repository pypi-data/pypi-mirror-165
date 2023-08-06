# This file is placed in the Public Domain.


"bus"


from .object import Object


class Bus(Object):

    "list of bots"

    objs = []

    @staticmethod
    def add(obj):
        "add a listener to the bus."
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        "annouce text on the joined listeners."
        for obj in Bus.objs:
            if obj and "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def byorig(orig):
        "return listener by origin (repr)."
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig, channel, txt):
        "say text into channel of specific listener."
        obj = Bus.byorig(orig)
        if obj and "say" in dir(obj):
            obj.say(channel, txt)
