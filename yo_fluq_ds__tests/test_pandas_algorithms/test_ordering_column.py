import unittest
from yo_fluq_ds__tests.common import *

df1 = Query.combinatorics.grid(CatA=['A','B'],CatB=[1,2], CatC=['x','y','z']).to_dataframe()

class OrderingColumnTests(unittest.TestCase):

    def make(self, df, group, order):
        return df.feed(fluq.add_ordering_column(group, order, 'order', 'group')).sort_index()

    def check(self, df, group, order, expected_order, group_order):
        result = self.make(df,group,order)
        self.assertListEqual(expected_order, list(result.order))
        self.assertListEqual(group_order, list(result.group))

    def dcheck(self, df, group, order, _, __): #pragma: no cover
        print(self.make(df,group,order))

    def pcheck(self, *args):#pragma: no cover
        pass

    def test_2_grouping_and_sorting_1(self):
        self.check(df1,
            ['CatB','CatC'],
            'CatA',
            [0,0,0,0,0,0,1,1,1,1,1,1],
            [0,1,2,3,4,5,0,1,2,3,4,5]
        )

    def test_2_grouping_and_sorting_2(self):
        self.check(df1,
            ['CatC','CatA'],
            'CatB',
            [0,0,0,1,1,1,0,0,0,1,1,1],
            [0,2,4,0,2,4,1,3,5,1,3,5]
        )

    def test_2_grouping_and_sorting_3(self):
        self.check(df1,
            ['CatA', 'CatB'],
            'CatC',
            [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2],
            [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
        )

    def test_1_grouping_and_sorting_1(self):
        self.check(df1,
            'CatA',
            'CatC',
            [0, 2, 4, 1, 3, 5, 0, 2, 4, 1, 3, 5],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        )

    def test_1_grouping_and_sorting_2(self):
        self.check(df1,
            'CatB',
            'CatC',
            [0, 2, 4, 0, 2, 4, 1, 3, 5, 1, 3, 5],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
        )


    def test_1_grouping_and_sorting_descending(self):
        self.check(df1,
            'CatB',
            ('CatC',False),
            [4, 2, 0, 4, 2, 0, 5, 3, 1, 5, 3, 1],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
        )


    def test_partial_df(self):
        self.check(df1.iloc[[1,3,4,5,7,8,10,11]],
                    'CatB',
                    'CatA',
                    [0,0,1,2,1,2,3,4],
                    [0,1,1,1,0,0,1,1]
                    )
