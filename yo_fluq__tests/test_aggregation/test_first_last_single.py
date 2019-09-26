from yo_fluq import *
from unittest import TestCase

def lazy_en_for_first():
    yield 0
    raise ValueError('First is not Lazy') #pragma: no cover
    yield 1                               #pragma: no cover

class LittleMethodsTests(TestCase):


    def test_first_1(self):
        self.assertEqual(1, Query.args(1, 2, 3).first())


    def test_first_2(self):
        self.assertRaises(ValueError,lambda: Query.args().first())

    def test_first_or_default_1(self):
        self.assertEqual(1, Query.args(1, 2, 3).first_or_default())


    def test_first_or_default_2(self):
        self.assertEqual(-1, Query.args().first_or_default(-1))

    def test_first_lazy(self):
        self.assertEqual(0,Query.en(lazy_en_for_first()).first())

    def test_last_1(self):
        self.assertEqual(3, Query.args(1, 2, 3).last())


    def test_last_2(self):
        self.assertRaises(ValueError, lambda: Query.args().last())


    def test_last_or_default_1(self):
        self.assertEqual(3, Query.args(1, 2, 3).last_or_default())


    def test_last_or_default_2(self):
        self.assertEqual(-1, Query.args().last_or_default(-1))


    def test_single_1(self):
        self.assertEqual(1, Query.args(1).single())


    def test_single_2(self):
        self.assertRaises(ValueError,lambda: Query.args().last())


    def test_single_3(self):
        self.assertRaises(ValueError,lambda: Query.args(1, 2).single())


    def test_single_or_default_1(self):
        self.assertEqual(1, Query.args(1).single_or_default())


    def test_single_or_default_2(self):
        self.assertEqual(-1, Query.args().single_or_default(-1))


    def test_single_or_default_3(self):
        self.assertRaises(ValueError,lambda:Query.args(1, 2).single_or_default())




