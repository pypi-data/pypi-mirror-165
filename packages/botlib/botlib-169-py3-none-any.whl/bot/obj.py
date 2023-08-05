# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,W0105,W0201


"big Object."


import datetime
import json
import os
import pathlib
import uuid


from json import JSONDecoder, JSONEncoder


def __dir__():
    return (
            'Default',
            'Object',
            'ObjectDecoder',
            'ObjectEncoder',
            'Wd',
            'edit',
            'find',
            'get',
            'items',
            'keys',
            'last',
            'load',
            'prt',
            'register',
            'save',
            'update',
            'values'
           )


def getpath(path):
    return os.path.join(Wd.workdir, "store", path) + os.sep


def otype(o):
    return str(type(o)).split()[-1][1:-2]


def types():
    path = os.path.join(Wd.workdir, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


class Wd:

    workdir = '.obj'


class Object:

    "big Object"

    __slots__ = (
        '__dict__',
        '__stp__'
    )

    @staticmethod
    def __new__(cls, *args, **kwargs):
        o = object.__new__(cls)
        o.__stp__ = os.path.join(
                                 otype(o),
                                 str(uuid.uuid4()),
                                 os.sep.join(str(datetime.datetime.now()).split())
                                )
        return o

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return self.__stp__

    def __str__(self):
        return str(self. __dict__)


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class ObjectDecoder(JSONDecoder):

    ""

    def  __init__(self, *args, **kwargs):
        ""
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        ""
        value = json.loads(s)
        o = Object()
        update(o, value)
        return o


    def raw_decode(self, s, *args, **kwargs):
        ""
        return JSONDecoder.raw_decode(self, s, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    ""

    def  __init__(self, *args, **kwargs):
        ""
        JSONEncoder.__init__(self, *args, **kwargs)


    def encode(self, o):
        ""
        return JSONEncoder.encode(self, o)


    def default(self, o):
        ""
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))):
            return o
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


    def iterencode(self, o, *args, **kwargs):
        ""
        return JSONEncoder.iterencode(self, o, *args, **kwargs)


def delete(o, key):
    delattr(o, key)


def dump(o, opath):
    if not os.path.exists(opath):
        if opath.split(os.sep)[-1].count(":") == 2:
            dirpath = os.path.dirname(opath)
            pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            o.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return o.__stp__


def edit(o, setter):
    for key, value in items(setter):
        register(o, key, value)


def get(o, key, default=None):
    return o.__dict__.get(key, default)


def items(o):
    try:
        return o.__dict__.items()
    except AttributeError:
        return o.items()


def keys(o):
    try:
        return o.__dict__.keys()
    except (AttributeError, TypeError):
        return o.keys()


def load(o, opath):
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(o, res)
    o.__stp__ = stp


def prt(o, args="", skip="_", empty=False, plain=False, **kwargs):
    keyz = list(keys(o))
    res = []
    if args:
        try:
            keyz = args.split(",")
        except (TypeError, ValueError):
            pass
    for key in keyz:
        try:
            skips = skip.split(",")
            if key in skips or key.startswith("_"):
                continue
        except (TypeError, ValueError):
            pass
        value = getattr(o, key, None)
        if not value and not empty:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    return " ".join(res)


def register(o, key, value):
    setattr(o, key, value)


def save(o, stime=None):
    prv = os.sep.join(o.__stp__.split(os.sep)[:2])
    o.__stp__ = os.path.join(
                                prv,
                                os.sep.join(str(datetime.datetime.now()).split())
                               )
    opath = os.path.join(Wd.workdir, "store", o.__stp__)
    dump(o, opath)
    os.chmod(opath, 0o444)
    return o.__stp__


def update(o, data):
    try:
        o.__dict__.update(vars(data))
    except TypeError:
        o.__dict__.update(data)
    return o


def values(o):
    try:
        return o.__dict__.values()
    except TypeError:
        return o.values()
