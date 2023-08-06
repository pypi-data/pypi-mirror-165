# This file is placed in the Public Domain.


"timer"


import threading
import time


from gcid.thread import launch
from gcid.object import Object
from gcid.utils import getname


def __dir__():
    return (
        "Repeater",
        "Timer",
    )



class Timer(Object):

    "run a function at a delta time from now."

    def __init__(self, sleep, func, *args, name=None):
        super().__init__()
        self.args = args
        self.func = func
        self.sleep = sleep
        self.name = name or getname(self.func)
        self.state = Object()
        self.timer = None

    def run(self):
        "run the function."
        self.state.latest = time.time()
        launch(self.func, *self.args)

    def start(self):
        "start the timer."
        timer = threading.Timer(self.sleep, self.run)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        "stop the timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    "call a function repeatedly."

    def run(self):
        "run the function."
        thr = launch(self.start)
        super().run()
        return thr
