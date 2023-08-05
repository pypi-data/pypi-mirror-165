# This file is placed in the Public Domain.


"bus"


import unittest


from bot.hdl import Bus, Client


class TestClient(Client):

    gotcha = False

    def raw(self, txt):
        self.gotcha = True


class TestBus(unittest.TestCase):

    def test_construct(self):
        bus = Bus()
        self.assertEqual(type(bus), Bus)

    def test_add(self):
        bus = Bus()
        clt = Client()
        bus.add(clt)
        self.assertTrue(clt in bus.objs)

    def test_announce(self):
        bus = Bus()
        clt = TestClient()
        bus.add(clt)
        bus.announce("test")
        self.assertTrue(clt.gotcha)

    def test_byorig(self):
        bus = Bus()
        clt = Client()
        self.assertEqual(bus.byorig(repr(clt)), clt)

    def test_say(self):
        bus = Bus()
        clt = TestClient()
        bus.add(clt)
        bus.say(repr(clt), "#test", "test")
        self.assertTrue(clt.gotcha)
