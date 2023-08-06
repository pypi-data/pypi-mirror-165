# This file is placed in the Public Domain.


"handler"


import queue
import threading
import time


from .bus import Bus
from .object import Object
from .table import Callbacks, Commands
from .thread import launch


class Handler(Object):

    "event handler."

    def __init__(self):
        Object.__init__(self)
        self.cache = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Bus.add(self)

    @staticmethod
    def forever():
        "run forever."
        while 1:
            time.sleep(1.0)

    @staticmethod
    def handle(event):
        "handle the event."
        Callbacks.dispatch(event)

    def loop(self):
        "handle events until stopped."
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self):
        "return an event to be handled."
        return self.queue.get()

    def put(self, event):
        "put an event into the waiting queue."
        self.queue.put_nowait(event)

    @staticmethod
    def register(typ, cbs):
        "register a callback."
        Callbacks.add(typ, cbs)

    def restart(self):
        "stop/start the handler."
        self.stop()
        self.start()

    def start(self):
        "start the handler."
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        "stop the handler."
        self.stopped.set()


def dispatch(evt):
    "dispatch an event."
    evt.parse()
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()
