# This file is placed in the Public Domain.


"basic"


import time


from .hdl import Commands
from .run import starttime
from .tmr import elapsed


def cmd(event):
    event.reply(",".join(sorted(Commands.cmd)))


def upt(event):
    event.reply(elapsed(time.time()-starttime))
