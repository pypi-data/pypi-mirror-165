# This file is placed in the Public Domain.


"event"


import threading


from .bus import Bus
from .default import Default
from .object import update
from .parse import parse


class Event(Default):

    "basic event."

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._result = []
        self.orig = repr(self)
        self.type = "event"

    def bot(self):
        "return originating bot."
        return Bus.byorig(self.orig)

    def parse(self):
        "parse the event."
        if self.txt:
            update(self, parse(self.txt))

    def ready(self):
        "signal event as ready."
        self._ready.set()

    def reply(self, txt):
        "add text to the result."
        self._result.append(txt)

    def show(self):
        "display results."
        for txt in self._result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        "wait for event to be ready."
        self._ready.wait()
        return self._result
