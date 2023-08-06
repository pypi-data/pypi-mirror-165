# This file is placed in the Public Domain.


"table"


from .object import Object, delete, get, register


class Callbacks(Object):

    "callbacks"

    cbs = Object()

    @staticmethod
    def add(typ, cbs):
        "add a callback."
        if typ not in Callbacks.cbs:
            register(Callbacks.cbs, typ, cbs)

    @staticmethod
    def callback(event):
        "run a callback (on event.type)."
        func = Callbacks.get(event.type)
        if not func:
            event.ready()
            return
        func(event)

    @staticmethod
    def dispatch(event):
        "dispatch an event."
        Callbacks.callback(event)

    @staticmethod
    def get(typ):
        "return callback."
        return get(Callbacks.cbs, typ)


class Class():

    "registered classes that can be saved."

    cls = {}

    @staticmethod
    def add(clz):
        "add a class."
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def full(name):
        "return matching class names."
        name = name.lower()
        res = []
        for cln in Class.cls:
            if cln.split(".")[-1].lower() == name:
                res.append(cln)
        return res

    @staticmethod
    def get(name):
        "return specific class name."
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name):
        "remove a class name."
        del Class.cls[name]


Class.add(Object)

class Commands(Object):

    "commands."

    cmds = Object()

    @staticmethod
    def add(cmd):
        "add a command."
        register(Commands.cmds, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        "return a command."
        return get(Commands.cmds, cmd)

    @staticmethod
    def remove(cmd):
        "remove a command."
        delete(Commands.cmds, cmd)


class Table(Object):

    "table"

    mods = Object()

    @staticmethod
    def add(mod):
        "add a module."
        register(Table.mods, mod.__name__, mod)

    @staticmethod
    def get(modname):
        "return a module."
        return get(Table, modname)

    @staticmethod
    def remove(modname):
        "remove a module."
        delete(Table.mods, modname)
