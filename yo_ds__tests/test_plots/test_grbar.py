from yo_ds__tests.common import *

def _get_df():
    df = Query.combinatorics.grid(x=range(5), a=range(5)).select(lambda z: z.update(y=z.x + z.a, err=z.a/2)).to_dataframe()
    return df

class TestGrBar(TestCase):
    def test_1_simple(self):
        df = _get_df()
        grbar_plot(df,'y','a','x')

    def test_2_error(self): # TODO: does not work
        df = _get_df()
        grbar_plot(df,'y','a','x','err')


    def test_3_value_caption(self):
        df = _get_df()
        grbar_plot(df,'y','a','x','err',value_format='{0:.2f}±{1:.2f}')

    def test_4_custom_caption(self):
        df = _get_df()
        df = df.assign(caption=df.y)
        grbar_plot(df,'y','a','x',None,'caption')


    def test_5_witout_groups(self):
        df= _get_df()
        df = df.loc[df.a==1]
        grbar_plot(df,'y','x',None)

    def test_6_without_colors(self):
        df = _get_df()
        df = df.loc[df.a==1]
        grbar_plot(df,'y',None,'x')

    def test_7_orient_h(self):
        df = _get_df()
        grbar_plot(df,'y','a','x',orient='h')

    def test_8_confints(self):
        df = _get_df()
        df = df.assign(confint=df.apply(lambda z: pd.Interval(z.y-z.err,z.y+z.err),axis=1))
        grbar_plot(df,'confint','a','x')