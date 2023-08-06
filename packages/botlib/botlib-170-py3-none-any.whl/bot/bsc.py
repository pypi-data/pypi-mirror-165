# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"basic"


import time


from op.hdl import Commands
from op.run import starttime
from op.utl import elapsed


def cmd(event):
    event.reply(",".join(sorted(Commands.cmd)))


def upt(event):
    event.reply(elapsed(time.time()-starttime))
