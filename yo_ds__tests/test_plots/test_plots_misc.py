from yo_ds__tests.test_plots.common import *

class TestPlotsMisc(TestCase):
    def test_fluentplot_iterate_df_columns_raises(self):
        df = pd.Series([1,2,3])
        self.assertRaises(
            ValueError,
            lambda: df.feed(FluentPlot().call(lambda z, ax: z.plot(ax=ax)).iterate_df_columns())
        )