from unittest import TestCase
from yo_fluq import *

class TestListAggreagation(TestCase):
    def test_aggregate_with(self):
        self.assertEqual(
            3,
            Query.args(1,2,3).aggregate_with(agg.Count())
        )

    def test_aggregate_list(self):
        self.assertDictEqual(
            dict(count=3,mean=2.0),
            Query.args(1,2,3).aggregate_with(agg.Count(),agg.Mean())
        )

    def test_throw_if_empty(self):
        self.assertRaises(ValueError,lambda:Query.args().aggregate_with(agg.Count().throw_if_empty()))