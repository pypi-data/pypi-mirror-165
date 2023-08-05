# This file is placed in the Public Domain.
# pylint: disable=E1101,E0611,C0116,C0413,W0105,W0201


"thread"


import inspect
import os
import queue
import threading
import time
import types


from .dbs import Class
from .obj import Default, Object, delete,  get, register, update


class Thread(threading.Thread):

    def __init__(self, func, name, *args, daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._exc = None
        self._evt = None
        self.name = name
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self._result = None

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self):
        func, args = self.queue.get()
        if args:
            self._evt = args[0]
        self.setName(self.name)
        self._result = func(*args)
        return self._result


def getname(obj):
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def launch(func, *args, **kwargs):
    name = kwargs.get("name", getname(func))
    thr = Thread(func, name, *args)
    thr.start()
    return thr


class Bus(Object):

    objs = []

    @staticmethod
    def add(obj):
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for obj in Bus.objs:
            if obj and "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def byorig(orig):
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig, channel, txt):
        obj = Bus.byorig(orig)
        if obj and "say" in dir(obj):
            obj.say(channel, txt)


class Callbacks(Object):

    cbs = Object()

    @staticmethod
    def add(name, cbs):
        register(Callbacks.cbs, name, cbs)

    @staticmethod
    def callback(event):
        func = Callbacks.get(event.type)
        if not func:
            event.ready()
            return
        func(event)

    @staticmethod
    def dispatch(event):
        Callbacks.callback(event)

    @staticmethod
    def get(cmd):
        return get(Callbacks.cbs, cmd)


class Commands(Object):

    cmd = Object()

    @staticmethod
    def add(cmd):
        register(Commands.cmd, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        return get(Commands.cmd, cmd)


    @staticmethod
    def remove(cmd):
        delete(Commands.cmd, cmd)


def dispatch(evt):
    evt.parse()
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()


class Parsed(Object):

    def __init__(self):
        Object.__init__(self)
        self.args = []
        self.cmd = ""
        self.gets = Default()
        self.index = 0
        self.opts = ""
        self.rest = ""
        self.sets = Default()
        self.toskip = Default()
        self.otxt = ""
        self.txt = ""

    def parse(self, txt=None):
        self.otxt = txt or self.txt
        spl = self.otxt.split()
        args = []
        _nr = -1
        for word in spl:
            if word.startswith("-"):
                try:
                    self.index = int(word[1:])
                except ValueError:
                    self.opts += word[1:2]
                continue
            try:
                key, value = word.split("==")
                if value.endswith("-"):
                    value = value[:-1]
                    register(self.toskip, value, "")
                register(self.gets, key, value)
                continue
            except ValueError:
                pass
            try:
                key, value = word.split("=")
                register(self.sets, key, value)
                continue
            except ValueError:
                pass
            _nr += 1
            if _nr == 0:
                self.cmd = word
                continue
            args.append(word)
        if args:
            self.args = args
            self.rest = " ".join(args)
            self.txt = self.cmd + " " + self.rest
        else:
            self.txt = self.cmd


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    return prs


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._result = []
        self.orig = None
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self):
        if self.txt:
            update(self, parse(self.txt))

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self._result.append(txt)

    def show(self):
        for txt in self._result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        return self._result


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cache = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Bus.add(self)

    @staticmethod
    def forever():
        while 1:
            time.sleep(1.0)

    @staticmethod
    def handle(event):
        Callbacks.dispatch(event)

    def loop(self):
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put_nowait(event)

    @staticmethod
    def register(typ, cbs):
        register(Callbacks, typ, cbs)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("event", dispatch)

    def announce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)


def scan(mod):
    scancls(mod)
    scancmd(mod)
    return mod


def scancls(mod):
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)
    return mod


def scancmd(mod):
    for _k, obj in inspect.getmembers(mod, inspect.isfunction):
        if "event" in obj.__code__.co_varnames:
            Commands.add(obj)
    return mod


def scandir(path, func):
    if not os.path.exists(path):
        return ("", "")
    res = []
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


def docmd(clt, txt):
    cmd = Event()
    cmd.channel = ""
    cmd.orig = repr(clt)
    cmd.txt = txt
    clt.handle(cmd)
    cmd.wait()
    return cmd


Callbacks.add("event", dispatch)
