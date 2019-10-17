from unittest import TestCase
from yo_fluq import *

class CoreTestCase(TestCase):
    def test_simple_aggregation(self):
        self.assertEqual(
            2.0,
            Query.push().mean()([1,2,3])
        )

    def test_select(self):
        self.assertListEqual(
            [10,20,30],
            Query.push().select(lambda z: z*10).to_list()([1,2,3])
        )

    def test_select_many(self):
        self.assertListEqual(
            ['a','b','c','d','e','f'],
            Query.push().select_many(lambda z: z).to_list()(['abc','','de','f'])
        )

    def test_where(self):
        self.assertListEqual(
            [1,2],
            Query.push().where(lambda z: z<3).to_list()([1,2,3,4,5])
        )

    def test_split_group(self):
        self.assertDictEqual(
            {
                0: [2,4],
                1: [1,3]
            },
            Query.push().split_by_group(lambda z: z%2).to_list()([1,2,3,4])
        )

    def test_split_group_always_dict(self):
        self.assertDictEqual(
            {
                0: [0]
            },
            Query.push().split_by_group(lambda z: z).to_list()([0])
        )

    def test_split_group_with_total(self):
        self.assertDictEqual(
            {
                0: [2,4],
                1: [1,3],
                'total': [1,2,3,4]
            },
            Query.push().split_by_group(lambda z: z%2,'total').to_list()([1,2,3,4])
        )

    def test_split_dict(self):
        self.assertDictEqual(
            dict(
                one = 2,
                ten = 20,
                hundred = 200
            ),
            Query.push().select(lambda z: dict(one=z,ten=z*10, hundred=z*100)).split_dictionary().sum()([1,1])
        )

    def test_split_dict_raise(self):
        self.assertRaises(
            ValueError,
            lambda: Query.push().split_dictionary().mean()([1])
        )



    def test_split_pipelines(self):
        self.assertDictEqual(
            dict(odds=[1,3], evens=[2,4]),
            Query.push().split_pipelines(
                odds = Query.push().where(lambda z: z%2==1).to_list(),
                evens = Query.push().where(lambda z: z%2==0).to_list(),
            )([1,2,3,4])
        )

    def test_subscription_raises_by_leaves(self):
        self.assertRaises(
            ValueError,
            lambda: Query.push().mean().mean()
        )

    def test_empty_pq_raises(self):
        self.assertRaises(
            ValueError,
            lambda: Query.push()([1,2])
        )

    def test_empty_observable(self):
        self.assertIsNone(
            Query.push().select(lambda z: z)([1,2])
        )
