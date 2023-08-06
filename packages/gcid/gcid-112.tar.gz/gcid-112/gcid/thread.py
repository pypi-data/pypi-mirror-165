# This file is placed in the Public Domain.


"thread"


import queue
import threading


from .utils import getname


class Thread(threading.Thread):

    "implements a iterable, result returning on join, thread."

    def __init__(self, func, name, *args, daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._exc = None
        self._evt = None
        self.name = name or getname(func)
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self._result = None

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        "join this thread."
        super().join(timeout)
        return self._result

    def run(self):
        "run the thead's function."
        func, args = self.queue.get()
        if args:
            self._evt = args[0]
        self.setName(self.name)
        self._result = func(*args)
        return self._result


def launch(func, *args, **kwargs):
    "run a function into a thread."
    name = kwargs.get("name", getname(func))
    thr = Thread(func, name, *args)
    thr.start()
    return thr
