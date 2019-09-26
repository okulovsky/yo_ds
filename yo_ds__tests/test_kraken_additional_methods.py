import unittest
from yo_ds import *

class KrakenMethodsTests(unittest.TestCase):
    def test_invoke(self):
        obj = dict(ctor=dict,a=1,b=2)
        result = kraken.invoke(obj)
        self.assertDictEqual(dict(a=1,b=2),obj['instance'])
        self.assertEqual('dict',obj['name'])

    def test_extract_id(self):
        df = Query.combinatorics.grid(a=[1,2],b=[3,4],c=[5,6]).to_dataframe()
        df, ids = kraken.extract_id(df,'t','a','b')
        self.assertListEqual(['1/3','1/3','1/4','1/4','2/3','2/3','2/4','2/4'],list(df.t))
        self.assertListEqual(list(ids.a.astype(str)+"/"+ids.b.astype(str)),list(ids.t))

