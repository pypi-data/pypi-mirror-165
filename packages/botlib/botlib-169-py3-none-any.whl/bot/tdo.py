# This file is placed in the Public Domain.
# pylint: disable=E1101,C0116,C0413,C0411


"todo"


import time


from .obj import Object, save
from .dbs import Db
from .tmr import elapsed
from .utl import fntime


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    dbs = Db()
    for _fn, obj in dbs.find("todo", selector):
        obj.__deleted__ = True
        save(obj)
        event.reply("ok")
        break


def tdo(event):
    if not event.rest:
        _nr = 0
        dbs = Db()
        for _fn, obj in dbs.find("todo"):
            event.reply("%s %s %s" % (
                                      _nr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(_fn)))
                                     )
            _nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    save(obj)
    event.reply("ok")
