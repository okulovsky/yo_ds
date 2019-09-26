from yo_ds__tests.common import *

class TestOtherPlots(TestCase):
    def test_pie(self):
        series = Query.en(range(1,5)).to_series()
        pie_plot(series)

    def test_roc_auc(self):
        true = [0,0,0,0,0,1,1,1]
        pred = [0.1,0.3,0.5,0.7,0.4,0.6,0.8, 0.8]
        return roc_plot(true,pred)