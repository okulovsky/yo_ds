from yo_fluq import *
from unittest import TestCase

class TestFeed(TestCase):
    def test_feed_execute(self):
        lst = Query.en([1,2,3]).take(2).feed(list)
        self.assertListEqual([1,2], lst)

    def test_feed_several_arguments(self):
        q = Query.en([1,2,3]).take(2)
        self.assertIsNone(q.length)
        q = q.feed(list,Query.en)
        self.assertEqual(2, q.length)


