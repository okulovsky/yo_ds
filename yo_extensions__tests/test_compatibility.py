from yo_extensions import *
from yo_extensions.misc import *
from yo_extensions import fluq as fluq
from unittest import TestCase

class CompatibilityTestCase(TestCase):
    def test_query(self):
        df = Query.combinatorics.grid(a=[10],b=[20]).to_dataframe()
        pass

    def test_query_feed(self):
        path = IO.relative_to_file(__file__,'sample.txt')
        Query.args(1,2,3).select(str).feed(fluq.to_text_file(path))

    def test_query_inherited_feed(self):
        self.assertListEqual(
            [(1,2),(2,3)],
            Query.args(1,2,3).feed(fluq.pairwise()).to_list()
        )


    def test_df_alg(self):
        s = Query.en(range(10)).to_series().feed(alg.trimmer(drop_before=5))
        self.assertListEqual(
            [6,7,8,9],
            list(s.values)
        )




