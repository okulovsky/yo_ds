from yo_fluq_ds__tests.common import *
from pathlib import Path

class TestInitiators(TestCase):
    def test_grid(self):
        df = Query.combinatorics.grid(A=[1, 2], B=['A', 'B']).to_dataframe()
        self.assertListEqual(['A', 'B'], list(df.columns))
        self.assertListEqual([1, 1, 2, 2], list(df.A))
        self.assertListEqual(['A', 'B', 'A', 'B'], list(df.B))


    def test_cartesian(self):
        lst = Query.combinatorics.cartesian([1, 2], ['A', 'B']).to_list()
        self.assertListEqual([
            (1, 'A'),
            (1, 'B'),
            (2, 'A'),
            (2, 'B')
        ], lst)

    def test_triangle(self):
        lst = Query.combinatorics.triangle([1,2,3],True).to_list()
        self.assertListEqual([(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)],lst)

    def test_trianle_no_diagonal(self):
        lst = Query.combinatorics.triangle([1,2,3,4],False).to_list()
        self.assertListEqual([(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)],lst)


    def test_folder(self):
        lst = Query.folder(path('test_queries','folder')).select(lambda z: z.name).order_by(lambda z: z).to_list()
        self.assertListEqual(['file1', 'file2'], lst)

    def test_folder_as_path(self):
        lst = Query.folder(Path(path('test_queries','folder'))).select(lambda z: z.name).order_by(
            lambda z: z).to_list()
        self.assertListEqual(['file1', 'file2'], lst)

    def test_folder_wrong_arg(self):
        self.assertRaises(ValueError,lambda:Query.folder(123).to_list())

    def test_folder_nonexisting(self):
        self.assertRaises(ValueError,lambda: Query.folder('NON-EXISTING-FOLDER').to_list())


    def test_powerset(self):
        r = Query.combinatorics.powerset([1,2,3]).to_list()
        self.assertListEqual([
            (),
            (1,),
            (2,),
            (3,),
            (1,2),
            (1,3),
            (2,3),
            (1,2,3)
        ],r)

    def test_powerset_2(self):
        r = Query.combinatorics.powerset(range(20)).distinct().count()
        self.assertEqual(2**20,r)


    def test_series(self):
        dct = Query.series(pd.Series([1,2,3],['a','b','c'])).to_dictionary()
        self.assertDictEqual(dict(a=1,b=2,c=3),dct)

    def test_df(self):
        df = pd.DataFrame()
        df['testA']=[1,2]
        df['testB']=['1','2']
        result = Query.df(df).to_list()
        self.assertDictEqual(dict(testA=1,testB='1'),result[0])
        self.assertDictEqual(dict(testA=2, testB='2'), result[1])
