from yo_fluq_ds__tests.common import *
import numpy as np

df = Query.en(['A']*30+['B'] * 60+['C'] * 10).to_dataframe(columns=['Group']).reset_index()

class StratifyColumnTests(TestCase):

    def chech(self,res):
        self.assertListEqual(list(range(100)), list(res.index.sort_values()))
        due = Query.series(df.groupby('Group').feed(fluq.fractions())).to_dictionary()
        width = 15
        for i in range(df.shape[0] - width):
            windowed = res.iloc[i:i + width].groupby('Group').feed(fluq.fractions())
            for key, value in due.items():
                self.assertLess(abs(value - windowed[key]), 0.1)

    def test_1(self):
        res = df.feed(fluq.stratify('Group','stratify'))
        self.chech(res)

    def test_2(self):
        res = df.feed(fluq.stratify('Group','stratify',random_state=42))
        self.chech(res)

    def test_3(self):
        res = df.feed(fluq.stratify('Group','stratify',random_state=np.random.RandomState(45)))
        self.chech(res)

