from unittest import TestCase
from yo_fluq import *

class AllAnyTest(TestCase):

    def test_all_1(self):
        self.assertEqual(True, Query.args(1, 2, 3).all(lambda z: z > 0))

    def test_all_2(self):
        self.assertEqual(False, Query.args(1, 2, 3).all(lambda z: z > 1))

    def test_all_3(self):
        self.assertEqual(True, Query.args(dict()).all())

    def test_all_4(self):
        self.assertEqual(True, Query.args().all())

    def test_all_5(self):
        self.assertEqual(False, Query.args(True,True,False).all())

    def test_all_6(self):
        self.assertEqual(True, Query.args(True,True).all())


    def test_any_1(self):
        self.assertEqual(True, Query.args(1, 2, 3).any(lambda z: z > 1))

    def test_any_2(self):
        self.assertEqual(False, Query.args(1, 2, 3).any(lambda z: z < 1))

    def test_any_3(self):
        self.assertEqual(True, Query.args(dict()).any())

    def test_any_4(self):
        self.assertEqual(False, Query.args().any())

    def test_any_5(self):
        self.assertEqual(False, Query.args(False,False).any())

    def test_any_6(self):
        self.assertEqual(True, Query.args(False,True).any())

