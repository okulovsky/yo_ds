from unittest import TestCase
from yo_fluq import *


class GeneralSelectorsTests(TestCase):

    def test_select(self):
        self.assertListEqual(
            ['1','2'],
            Query.args(1, 2).select(str).to_list()
        )

    def test_select_length(self):
        self.assertEqual(3,Query.en([1,2,3]).select(str).length)

    def test_select_many(self):
        self.assertListEqual(
            [0, 0, 1, 0, 1, 2],
            Query.args(1, 2, 3).select_many(lambda z: range(z)).to_list())

    def test_distinct(self):
        self.assertListEqual(
            [1, 2, 3],
            Query.args(1, 2, 2, 3, 3).distinct().to_list()
        )

    def test_distinct_1(self):
        self.assertListEqual(
            ['aa','b'],
            Query.args('aa', 'ab', 'b').distinct(lambda z: z[0]).to_list()
        )

    def test_where(self):
        self.assertListEqual(
            [2,4],
            Query.args(1, 2, 3, 4).where(lambda z: z % 2 == 0).to_list()
        )

    def test_group_by(self):
        result = Query.args(2, 3, 1, 4).group_by(lambda z: z % 2).to_list()
        self.assertEqual(0, result[0].key)
        self.assertListEqual([2, 4], result[0].value)
        self.assertEqual(1, result[1].key)
        self.assertListEqual([3, 1], result[1].value)

    def test_group_by_1(self):
        result = Query.args(2,3,1,4).group_by(lambda z: z%2).select(lambda z: (z.key,Query.en(z).sum())).to_list()
        self.assertListEqual(
            [(0,6),(1,4)],
            result)

    def test_group_by_2(self):
        result = Query.args(2,3,1,4).group_by(lambda z: z%2).to_dictionary()
        self.assertDictEqual({0:[2,4],1:[3,1]},result)

    def test_aggrerate(self):
        self.assertEqual('123', Query.args('1', '2', '3').aggregate(lambda acc, el: acc + el))

    def test_concat(self):
        self.assertListEqual(
            [1,2,3,3,4,5],
            Query.args(1,2,3).concat([3,4,5]).to_list()
        )

    def test_intersect(self):
        self.assertListEqual(
            [2,3],
            Query.args(1,2,3).intersect([2,3,4]).to_list()
        )

    def test_skip_while(self):
        self.assertListEqual(
            [3,4,5],
            Query.args(1,2,3,4,5).skip_while(lambda z: z<3).to_list()
        )

    def test_take_while(self):
        self.assertListEqual(
            [1,2],
            Query.args(1,2,3,4,5).take_while(lambda z: z<3).to_list()
        )

    def test_skip(self):
        self.assertListEqual(
            [4,5],
            Query.args(1, 2, 3, 4, 5).skip(3).to_list()
        )

    def test_take(self):
        self.assertListEqual(
            [1,2],
            Query.args(1, 2, 3, 4, 5).take(2).to_list()
        )

    def test_iter(self):
        buf = []
        for e in Query.args(1,2,3):
            buf.append(e)
        self.assertListEqual([1,2,3],buf)

    def test_feed(self):
        self.assertListEqual(
            [1,2,3],
            Query.args(1,2,3).feed(list)
        )