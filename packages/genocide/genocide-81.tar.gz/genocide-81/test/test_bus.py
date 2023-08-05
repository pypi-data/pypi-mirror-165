# This file is placed in the Public Domain.


"bus"


import unittest


from genocide.hdl import Bus, Client


class MyClient(Client):

    def __init__(self):
        Client.__init__(self)
        self.gotcha = False

    def raw(self, txt):
        self.gotcha = True


class TestBus(unittest.TestCase):

    def test_add(self):
        clt = MyClient()
        Bus.add(clt)
        self.assertTrue(clt in Bus.objs)

    def test_announce(self):
        clt = MyClient()
        clt.gotcha = False
        Bus.add(clt)
        Bus.announce("test")
        self.assertTrue(clt.gotcha)

    def test_byorig(self):
        clt = MyClient()
        Bus.add(clt)
        self.assertEqual(Bus.byorig(clt.orig), clt)

    def test_say(self):
        clt = MyClient()
        clt.gotcha = False
        Bus.add(clt)
        Bus.say(clt.orig, "#test", "test")
        self.assertTrue(clt.gotcha)
