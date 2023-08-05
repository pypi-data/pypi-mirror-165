# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,W0105,W0201


"database"


import os
import _thread


from .obj import Wd, Object, getpath, load, otype, update
from .obj import save, items, get
from .utl import locked, fntime


dblock = _thread.allocate_lock()


class Class():

    cls = {}

    @staticmethod
    def add(clz):
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def full(name):
        name = name.lower()
        res = []
        for cln in Class.cls:
            if cln.split(".")[-1].lower() == name:
                res.append(cln)
        return res

    @staticmethod
    def get(name):
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name):
        del Class.cls[name]


Class.add(Object)


class Db(Object):

    @staticmethod
    def all(otp, timed=None):
        result = []
        for fnm in fns(getpath(otp), timed):
            o = hook(fnm)
            if "__deleted__" in o and o.__deleted__:
                continue
            result.append((fnm, o))
        if not result:
            return []
        return result

    @staticmethod
    def find(name, selector=None, index=None, timed=None, names=None):
        if not names:
            names = Class.full(name)
        for nme in names:
            for fnm, o in Db.findtype(nme, selector, index, timed):
                yield fnm, o

    @staticmethod
    def findtype(otp, selector=None, index=None, timed=None):
        if selector is None:
            selector = {}
        _nr = -1
        result = []
        for fnm in fns(getpath(otp), timed):
            o = hook(fnm)
            if selector and not Db.search(o, selector):
                continue
            if "__deleted__" in o and o.__deleted__:
                continue
            _nr += 1
            if index is not None and _nr != index:
                continue
            result.append((fnm, o))
        return result

    @staticmethod
    def last(o):
        path, _obj = Db.lastfn(otype(o))
        if _obj:
            update(o, _obj)
        if path:
            splitted = path.split(os.sep)
            stp = os.sep.join(splitted[-4:])
            return stp
        return None

    @staticmethod
    def lastmatch(otp, selector=None, index=None, timed=None):
        dbs = Db()
        res = sorted(dbs.find(otp, selector, index, timed),
                     key=lambda x: fntime(x[0]))
        if res:
            return res[-1]
        return (None, None)

    @staticmethod
    def lasttype(otp):
        fnn = fns(getpath(otp))
        if fnn:
            return hook(fnn[-1])
        return None

    @staticmethod
    def lastfn(otp):
        fnm = fns(getpath(otp))
        if fnm:
            fnn = fnm[-1]
            return (fnn, hook(fnn))
        return (None, None)

    @staticmethod
    def remove(otp, selector=None):
        has = []
        for _fn, o in Db.find(otp, selector or {}):
            o.__deleted__ = True
            has.append(o)
        for o in has:
            save(o)
        return has

    @staticmethod
    def search(o, selector):
        res = False
        for key, value in items(selector):
            val = get(o, key)
            if value in str(val):
                res = True
                break
        return res

    @staticmethod
    def types():
        path = os.path.join(Wd.workdir, "store")
        if not os.path.exists(path):
            return []
        return sorted(os.listdir(path))


@locked(dblock)
def fns(path, timed=None):
    if not path:
        return []
    if not os.path.exists(path):
        return []
    res = []
    dpath = ""
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        if dirs:
            dpath = sorted(dirs)[-1]
            if dpath.count("-") == 2:
                ddd = os.path.join(rootdir, dpath)
                fls = sorted(os.listdir(ddd))
                if fls:
                    opath = os.path.join(ddd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(opath) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(opath) > timed.to:
                        continue
                    res.append(opath)
    return sorted(res, key=fntime)


@locked(dblock)
def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    cls = Class.get(cname)
    if cls:
        o = cls()
    else:
        o = Object()
    fnm = os.sep.join(oname)
    load(o, fnm)
    return o
