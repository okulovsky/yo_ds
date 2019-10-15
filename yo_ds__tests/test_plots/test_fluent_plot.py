from yo_ds__tests.common import *
import seaborn
import math

class TestFluentPlot(TestCase):
    def test_1_simple(self):
        df = Query.en(range(10)).select(lambda z: Obj(x=z,y=z*z)).to_dataframe()
        return df.feed(FluentPlot().call(lambda item,ax: ax.plot(item.x,item.y)).labels('Simplest fluent plot'))

    def test_2_3rdparty(self):
        df = Query.combinatorics.grid(x=range(5),y=range(5)).select(lambda z: z.update(z=z.x+z.y)).to_dataframe().pivot_table(columns='x',index='y',values='z')
        return df.feed(FluentPlot().call(lambda item, ax: seaborn.heatmap(data=item,ax=ax)).labels('Fluent plot over 3rd party member from seaborn'))

    def test_3_tuning(self):
        df = Query.en(range(10)).select(lambda z: Obj(x=z, y=z * z)).to_dataframe()
        return df.feed(FluentPlot()
                       .call(lambda item,ax: ax.plot(item.x,item.y,label='label'))
                       .labels('Plot with cosmetic tuning','X axis','Y axis')
                       .with_legend()
                       .tune(lambda ax: ax.tick_params(axis='x', rotation=45))
                       )


    def test_4_groupby_plot(self):
        df = Query.combinatorics.grid(a=range(5),x=range(10)).select(lambda z: z.update(y=z.x*z.a)).to_dataframe()
        return df.groupby('a').feed(FluentPlot()
                                    .call(lambda gr, ax: ax.plot(gr[1].x, gr[1].y, label = gr[0]))
                                    .labels('Plot built for groupby')
                                    .iterate()
                                    .with_legend())


    def test_5_df_columns_plot(self):
        df = Query.combinatorics.grid(x=range(5), y=range(5)).select(lambda z: z.update(z=z.x + z.y)).to_dataframe().pivot_table(columns='x', index='y', values='z')
        return df.feed(FluentPlot()
                       .call(lambda item,ax: ax.plot(item.index, item, label = item.name))
                       .iterate_df_columns()
                       .labels('Plot build for dataframe columns')
                       .with_legend())


    def test_6_plots_on_different_axes(self):
        df = Query.en(range(10)).select(lambda z: Obj(x=z, pow=z*z, sqrt=math.sqrt(z))).to_dataframe().set_index('x')
        (Query
         .en(df.columns)
         .feed(fluq.with_plots(columns=2))
         .foreach(lambda p: df[p.item].feed(FluentPlot()
                                            .call(lambda item,ax: ax.plot(item.index, item))
                                            .on(p.ax)
                                            )))

    def test_7_plot_from_series(self):
        series = pd.Series([5,4,3,2,1])
        series.feed(FluentPlot().call(lambda item, ax: item.plot(ax=ax)).size(20,10))


    def test_8_plot_from_df(self):
        df = Query.en(range(10)).select(lambda z: Obj(x=z, pow=z * z, sqrt=math.sqrt(z))).to_dataframe().set_index('x')
        df.feed(FluentPlot().call(lambda item,ax: item.plot(ax=ax)).iterate_df_columns())