from yo_fluq import *
from unittest import TestCase


class ToCollectionMethodsTests(TestCase):
    def test_to_dictionary_normal(self):
        d = Query.args(1,2,3).to_dictionary(lambda z: z, lambda z: str(z))
        self.assertDictEqual({1:'1',2:'2',3:'3'},d)

    def test_to_dictionary_duplicating(self):
        self.assertRaises(ValueError,lambda: Query.args(1,1,2).to_dictionary(lambda z: z, lambda z: str(z)))

    def test_to_dictionary_key_value_pair(self):
        d = Query.args(1,2,3).select(lambda z: KeyValuePair(z,str(z))).to_dictionary()
        self.assertDictEqual({1: '1', 2: '2', 3: '3'}, d)

    def test_to_dictionary_key_value_pair_override(self):
        d = Query.dict(dict(a=1,b=2)).to_dictionary(lambda z: z.key.upper(), lambda z: z.value+1)
        self.assertDictEqual(dict(A=2,B=3),d)

    def test_to_dictionary_mixture(self):
        self.assertRaises(ValueError,lambda: Query.args(KeyValuePair(1,2),1).to_dictionary())

    def test_to_dictionary_without_key_selector(self):
        self.assertRaises(ValueError, lambda: Query.args(1).to_dictionary())

    def test_to_dictionary_without_value_selector(self):
        self.assertRaises(ValueError, lambda: Query.args(1).to_dictionary(lambda z: z))

    def test_to_dictionary_grby(self):
        result = Query.args(1,2,3,4).group_by(lambda z: z%2).to_dictionary()
        self.assertDictEqual({0:[2,4],1:[1,3]},result)

    def test_to_tuple(self):
        t = Query.args(1, 2, 3).to_tuple()
        self.assertIsInstance(t, tuple)
        self.assertListEqual([1, 2, 3], list(t))

    def test_to_set_1(self):
        st = Query.args(1, 2, 3).to_set()
        self.assertSetEqual({1, 2, 3}, st)

    def test_to_set_2(self):
        self.assertRaises(ValueError, lambda: Query.args(1, 2, 2).to_set())

