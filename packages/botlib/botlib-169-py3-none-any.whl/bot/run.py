# This file is placed in the Public Domain.
# pylint: disable=E1101,E0611,C0116,C0413,W0201,C0411


"runtime"


import time


from .obj import Default


starttime = time.time()


Cfg = Default()


def wait():
    while True:
        time.sleep(1.0)
