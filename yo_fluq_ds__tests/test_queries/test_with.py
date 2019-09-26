from yo_fluq_ds__tests.common import *

from tqdm import tqdm
from matplotlib.axes import Axes

class YoWithTests(TestCase):
    def test_progress_bar_0(self):
        en = Query.args(1,2,3).feed(fluq.with_progress_bar(console=True)).en
        self.assertTrue(isinstance(en,tqdm))
        self.assertEqual(3,en.total)

    def test_progress_bar_1(self):
        en = Query.args(1,2,3).where(lambda z: True).feed(fluq.with_progress_bar(console=True)).en
        self.assertTrue(isinstance(en,tqdm))
        self.assertEqual(None,en.total)

    def test_plots_0(self):
        result = Query.args("1","2","3").feed(fluq.with_plots(2)).to_list()
        axes = result[0]._all_axes
        self.assertEqual((2,2),axes.shape)
        self.assertEqual('1', axes[0, 0].title.get_text())
        self.assertEqual('2', axes[0, 1].title.get_text())
        self.assertEqual('3', axes[1, 0].title.get_text())
        self.assertEqual('1',result[0].item)


    def test_plots_1(self):
        result = Query.args('1').feed(fluq.with_plots(1)).to_list()
        axes = result[0]._all_axes
        self.assertTrue(isinstance(axes,Axes))


