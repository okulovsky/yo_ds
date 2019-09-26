from yo_fluq import *
from unittest import TestCase



class LittleMethodsTests(TestCase):

    def test_min(self):
        self.assertEqual(1,Query.args(1,2,3).min())

    def test_min_on_empty_with_default(self):
        self.assertIsNone(Query.args().min(default=None))

    def test_min_on_empty(self):
        self.assertRaises(ValueError,lambda: Query.args().min())

    def test_min_with_selector(self):
        self.assertEqual(-3,Query.args(1,2,3).min(lambda z: -z))


    def test_max(self):
        self.assertEqual(3,Query.args(1,2,3).max())

    def test_max_on_empty_with_default(self):
        self.assertIsNone(Query.args().max(default=None))

    def test_max_on_empty(self):
        self.assertRaises(ValueError,lambda: Query.args().max())

    def test_max_with_selector(self):
        self.assertEqual(-1,Query.args(1,2,3).max(lambda z: -z))


    def test_argmax_1(self):
        self.assertEqual(-1, Query.args(-1, 0, 1).argmax(lambda z: abs(z)))

    def test_argmax_2(self):
        self.assertRaises(ValueError,lambda: Query.args().argmax(lambda z: abs(z)))

    def test_argmax_or_default_1(self):
        self.assertEqual(-1, Query.args(-1, 0, 1).argmax(lambda z: abs(z), default=10))

    def test_argmax_or_default_2(self):
        self.assertEqual(-10, Query.args().argmax(lambda z: abs(z), default = -10))

    def test_argmin_1(self):
        self.assertEqual(0, Query.args(-1, 0, 1).argmin(lambda z: abs(z)))

    def test_argmin_2(self):
        self.assertRaises(ValueError,lambda: Query.args().argmin(lambda z: abs(z)))


    def test_argmin_or_default_1(self):
        self.assertEqual(0, Query.args(-1, 0, 1).argmin(lambda z: abs(z),default=-10))

    def test_argmin_or_default_2(self):
        self.assertEqual(-10, Query.args().argmin(lambda z: abs(z), -10))

