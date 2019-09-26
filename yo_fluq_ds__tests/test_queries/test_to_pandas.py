from yo_fluq_ds__tests.common import *
import numpy as np
import pandas as pd

class ToPandasTestCase(TestCase):
    def test_to_ndarray_1d(self):
        arr = Query.args(1,2,3).to_ndarray()
        self.assertEqual(type(arr),np.ndarray)

    def test_to_ndarray_2d(self):
        arr = Query.args([1,2],[3,4]).to_ndarray()
        self.assertListEqual([2,2],list(arr.shape))
        self.assertEqual(3,arr[1,0])

    def test_to_series_default(self):
        ser = Query.args(1,2,3).to_series()
        self.assertEqual(type(ser), pd.Series)
        self.assertListEqual([1,2,3],list(ser))

    def test_to_series_value_selector(self):
        ser = Query.args(1,2,3).to_series(str)
        self.assertListEqual(['1','2','3'],list(ser))

    def test_to_series_index_selector(self):
        ser = Query.args(1,2,3).to_series(key_selector=str)
        self.assertListEqual([1,2,3],list(ser))
        self.assertListEqual(['1','2','3'], list(ser.index))

    def test_to_series_both_selectors(self):
        ser = Query.args(1, 2, 3).to_series(lambda z: -z, str)
        self.assertListEqual([-1, -2, -3], list(ser))
        self.assertListEqual(['1', '2', '3'], list(ser.index))

    def test_to_series_key_value_pair(self):
        ser = Query.args(1,2,3).select(lambda z: KeyValuePair(z,str(z))).to_series()
        self.assertListEqual([1,2,3],list(ser.index))
        self.assertListEqual(['1','2','3'], list(ser))

    def test_to_series_special_case(self):
        ser = Query.args(1,2,3,4).group_by(lambda z: z%2).to_series(lambda z: len(z),lambda z: z.key)
        self.assertListEqual([2,2],list(ser))
        self.assertEqual([1,0],list(ser.index))

    def test_to_series_raises_on_mixture(self):
        self.assertRaises(
            ValueError,
            lambda: Query.dict(dict(a=2,b=2)).concat([1]).to_series()
        )

    def test_to_df(self):
        data = Query.en([1,2,3]).select_many(lambda a: Query.en(['a','b']).select(lambda b: Obj(A=a,B=b))).to_dataframe()
        self.assertListEqual(['A','B'], list(data.columns))
        self.assertEqual('int64',data.A.dtype.name)
        self.assertEqual('object',data.B.dtype.name)
        self.assertListEqual([1, 1, 2, 2, 3, 3], list(data.A))
        self.assertListEqual(['a', 'b', 'a', 'b', 'a', 'b'], list(data.B))

    def test_to_df_variable_length(self):
        df = Query.args(Obj(a=1),Obj(a=1,b=2)).to_dataframe()
        self.assertListEqual(['a','b'],list(df.columns))
