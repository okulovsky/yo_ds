from yo_fluq import *
from unittest import TestCase


def _lazy():
    for i in range(10):
        yield i

class InitiatorsTest(TestCase):
    def assertKeyValuePair(self, keys, values, results):
        for key, value, result in zip(keys,values,results):
            self.assertIsInstance(result,KeyValuePair)
            self.assertEqual(key,result.key)
            self.assertEqual(value,result.value)

    def test_sized_en(self):
        self.assertEqual(3,Query.en([1,2,3]).length)

    def test_unsized_en(self):
        self.assertEqual(None,Query.en(_lazy()).length)

    def test_unsized_count(self):
        self.assertEqual(10,Query.en(_lazy()).count())

    def test_sized_select(self):
        self.assertEqual(3,Query.args(1,2,3).select(str).length)

    def test_size_args(self):
        self.assertEqual(3,Query.args(1,2,3).length)


    def test_dict(self):
        self.assertKeyValuePair(
            ['a','b','c'],
            [1,2,3],
            Query.dict(dict(a=1,b=2,c=3)).to_list()
        )

    def test_with_indices(self):
        self.assertKeyValuePair(
            [0,1,2],
            ['a','b','c'],
            Query.en('abc').with_indices().to_list()
        )
