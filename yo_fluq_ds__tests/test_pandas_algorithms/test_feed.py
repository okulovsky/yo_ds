from yo_fluq_ds__tests.common import *

class FractionsTests(TestCase):
    def test_groupby(self):
        df = pd.DataFrame({'a':[1,1,2,2,2]})
        series = df.groupby('a').feed(fluq.fractions(), Query.series).to_dictionary()
        self.assertDictEqual({1:0.4,2:0.6},series)