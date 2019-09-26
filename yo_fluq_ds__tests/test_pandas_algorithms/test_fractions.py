from yo_fluq_ds__tests.common import *

class FractionsTests(TestCase):
    def test_groupby(self):
        df = pd.DataFrame({'a':[1,1,2,2,2]})
        series = df.groupby('a').feed(fluq.fractions()).feed(Query.series).to_dictionary()
        self.assertDictEqual({1:0.4,2:0.6},series)
    def test_series(self):
        s = pd.Series([1,2,2]).feed(fluq.fractions()).feed(list)
        self.assertListEqual([0.2,0.4,0.4],s)

    def test_else(self):
        self.assertRaises(TypeError,lambda: fluq.fractions()(1))