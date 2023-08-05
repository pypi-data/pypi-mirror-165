# This file is placed in the Public Domain.


"timer"


import unittest


from genocide.tmr import Timer


def test():
    pass


class TestTimer(unittest.TestCase):

    def testcontructor(self):
        timer = Timer(60, test)
        self.assertEqual(type(timer), Timer)
