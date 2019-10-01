from ._common import *

def pie_plot(series: pd.Series, explode: float = 0.1, with_abs_values: bool = False, ax: Axes = None):
    def pcnt(p, total):
        cnt = round(p * total / 100)
        return "{0:.0f} ({1:.2f}%)".format(cnt, p)

    values = series.name or 'values'
    ind = series.index.name or 'index'
    dt = series.to_frame(values).reset_index().assign(explode=explode)


    total = dt[values].sum()
    pcnter = '%1.2f%%'
    if with_abs_values:
        pcnter = lambda p: pcnt(p, total)

    ax = default_ax(ax)

    ax.pie(
        dt[values],
        labels=dt[ind],
        explode=dt['explode'],
        shadow=True,
        startangle=90,
        autopct=pcnter
    )