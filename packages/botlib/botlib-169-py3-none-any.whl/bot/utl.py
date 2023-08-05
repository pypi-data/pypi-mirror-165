# This file is placed in the Public Domain.
# pylint: disable=C0112,C0103,W0105,W0201


"utility"


import os
import pathlib
import time
import _thread


dblock = _thread.allocate_lock()


def locked(lock):

    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            lock.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        return lockedfunc

    return lockeddec


def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.split(".")[0]
    return time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))


def listfiles(workdir):
    path = os.path.join(workdir, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def spl(txt):
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
