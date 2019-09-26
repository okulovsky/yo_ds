from unittest import TestCase
from yo_fluq import *

class ExtendedMethodsTests(TestCase):
    def test_foreach(self):
        buf = []
        Query.args(1, 2, 3).foreach(buf.append)
        self.assertListEqual([1,2,3],buf)

    def test_foreach_and_continue(self):
        buf = []
        Query.args(1, 2, 3).foreach_and_continue(lambda z: buf.append(z + 10)).foreach(buf.append)
        self.assertListEqual([11,1,12,2,13,3], buf)

    def test_append(self):
        self.assertListEqual(
            [1,2,5,6],
            Query.args(1, 2).append(5, 6).to_list()
        )

    def test_prepend(self):
        self.assertListEqual(
            [5, 6, 1, 2],
            Query.args(1, 2).prepend(5, 6).to_list()
        )