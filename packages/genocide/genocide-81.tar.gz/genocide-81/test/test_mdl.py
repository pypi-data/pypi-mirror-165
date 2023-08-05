# pylint: disable=E1101,C0116,E0611
# This file is placed in the Public Domain.


"model"


import unittest


from genocide.mdl import oorzaak


class TestComposite(unittest.TestCase):

    def test_composite(self):
        self.assertEqual(type(oorzaak), dict)
