# This file is placed in the Public Domain.

"client"


from .handler import Handler, dispatch


class Client(Handler):

    "input/output handler."

    def __init__(self):
        Handler.__init__(self)
        self.ignore = []
        self.orig = repr(self)
        self.register("event", dispatch)

    def announce(self, txt):
        "annouce text."
        self.raw(txt)

    def raw(self, txt):
        "raw echo of text."
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        "say text into channel."
        if channel not in self.ignore:
            self.raw(txt)
