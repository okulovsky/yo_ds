from yo_fluq_ds__tests.common import *
import numpy as np

class MiscMethodsTests(TestCase):
    def test_pairwise(self):
        result = Query.args(1,2,3).feed(fluq.pairwise()).to_list()
        self.assertListEqual([(1,2),(2,3)],result)

    def test_strjoin(self):
        result = Query.args(1,2,3).feed(fluq.strjoin(','))
        self.assertEqual("1,2,3",result)

    def test_countby(self):
        result = Query.args(1,1,1,2,2,3).feed(fluq.count_by(lambda z: z)).to_series()
        self.assertListEqual([1,2,3],list(result.index))
        self.assertListEqual([3,2,1],list(result))

    def test_shuffle(self):
        arg = Query.en(range(5)).feed(fluq.shuffle(1)).to_list()
        self.assertListEqual([2,1,4,0,3],arg)

    def test_shuffle_rstate(self):
        arg = Query.en(range(5)).feed(fluq.shuffle(np.random.RandomState(1))).to_list()
        self.assertListEqual([2,1,4,0,3],arg)

    def test_shuffle_true(self):
        arg = Query.en(range(5)).feed(fluq.shuffle(True)).to_set()
        self.assertSetEqual({0,1,2,3,4}, arg)
        self.assertEqual(5,len(arg))

    def test_shuffle_false(self):
        res = Query.en(range(5)).feed(fluq.shuffle(False)).to_list()
        self.assertListEqual([0,1,2,3,4],res)

    def test_shuffle_none(self):
        res = Query.en(range(5)).feed(fluq.shuffle(None)).to_list()
        self.assertListEqual([0,1,2,3,4],res)

    def test_shuffle_raises(self):
        self.assertRaises(
            TypeError,
            lambda: Query.en(range(5)).feed(fluq.shuffle('a')).to_list()
        )

