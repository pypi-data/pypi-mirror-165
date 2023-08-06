# This file is placed in the Public Domain.
# pylint: disable=E1101,C0116,C0413,C0411


"command"


import unittest


from op.clt import Client
from op.obj import Object, get
from op.run import Cfg, docmd
from op.tbl import Commands

evts = []
skip = ["cfg",]


param = Object()
param.cmd = [""]
param.cfg = ["nick=bot", "server=localhost", "port=6699"]
param.fnd = ["log", "log txt==test", "config", "config name=bot", "config server==localhost"]
param.flt = ["0", ""]
param.log = ["test1", "test2"]
param.mre = [""]
param.thr = [""]


class CLI(Client):

    "test cli class"

    @staticmethod
    def raw(txt):
        if Cfg.verbose:
            print(txt)


cli = CLI()


def consume(events):
    fixed = []
    res = []
    for evt in events:
        evt.wait()
        fixed.append(evt)
    for evt in fixed:
        try:
            events.remove(evt)
        except ValueError:
            continue
    return res


class TestCommands(unittest.TestCase):

    "commands test class."

    def test_commands(self):
        cmds = sorted(Commands.cmds)
        for cmd in cmds:
            if cmd in skip:
                continue
            for ex in get(param, cmd, ""):
                evt = docmd(cli, cmd + " " + ex)
                evts.append(evt)
        consume(evts)
        self.assertTrue(not evts)
