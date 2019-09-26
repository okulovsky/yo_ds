from yo_fluq import *
from unittest import TestCase


class AggregationMethodsTests(TestCase):


    def test_count(self):
        self.assertEqual(3,Query.args(1,2,3).count())

    def test_count_float(self):
        t = Query.args(1,2,3).aggregate_with(agg.Count().astype(float))
        self.assertIsInstance(t,float)
        self.assertEqual(3.0,t)

    def test_sum(self):
        self.assertEqual(6,Query.args(1,2,3).sum())

    def test_sum_on_empty(self):
        self.assertRaises(ValueError, lambda: Query.args().sum())

    def test_sum_on_empty_default(self):
        self.assertIsNone(Query.args().aggregate_with(agg.Sum().default_if_empty()))

    def test_mean(self):
        self.assertEqual(2.0,Query.args(1,2,3).mean())

    def test_mean_on_empty(self):
        self.assertIsNone(Query.args().mean())

    def test_std(self):
        arr = [0.5488135039273248, 0.7151893663724195, 0.6027633760716439, 0.5448831829968969, 0.4236547993389047, 0.6458941130666561, 0.4375872112626925, 0.8917730007820798, 0.9636627605010293, 0.3834415188257777]
        std_expected = 0.18447489445957163
        self.assertAlmostEqual(std_expected,Query.en(arr).aggregate_with(agg.Std()),5)

    def test_std_single(self):
        self.assertIsNone(Query.args(1).aggregate_with(agg.Std()))


