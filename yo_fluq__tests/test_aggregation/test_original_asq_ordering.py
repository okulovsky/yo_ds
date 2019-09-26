from unittest import TestCase
from yo_fluq import *

class OrderingTests(TestCase):

    def test_order_by(self):
        self.assertListEqual(
            ['a','bb','ccc'],
            Query.args('ccc', 'bb', 'a').order_by(len).to_list()
        )


    def test_order_by_descending(self):
        self.assertListEqual(
            ['ccc','bb','a'],
            Query.args('ccc', 'bb', 'a').order_by_descending(len).to_list()
        )

    def test_order_then_1(self):
        self.assertListEqual(
            ['a1','a2','b1','b2'],
            Query.args('a2', 'b1', 'b2', 'a1').order_by(lambda z: z[0]).then_by(lambda z: z[1]).to_list()
        )

    def test_order_then_2(self):
        self.assertListEqual(
            ['a2','a1','b2','b1'],
            Query.args('a2', 'b1', 'b2', 'a1').order_by(lambda z: z[0]).then_by_descending(lambda z: z[1]).to_list()
        )

    def test_order_then_3(self):
        self.assertListEqual(
            ['b1', 'b2', 'a1', 'a2'],
            Query.args('a2', 'b1', 'b2', 'a1').order_by_descending(lambda z: z[0]).then_by(lambda z: z[1]).to_list()
        )

    def test_order_then_4(self):
        self.assertListEqual(
            ['b2','b1','a2','a1'],
            Query.args('a2', 'b1', 'b2', 'a1').order_by_descending(lambda z: z[0]).then_by_descending(lambda z: z[1]).to_list(),
        )

    def test_then(self):
        self.assertRaises(ValueError, lambda: Query.args(1, 2).then_by(lambda z: z).to_list())

    def test_then_desc(self):
        self.assertRaises(ValueError, lambda: Query.args(1, 2).then_by_descending(lambda z: z).to_list())

