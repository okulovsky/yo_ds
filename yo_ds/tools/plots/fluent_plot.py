from typing import *
import pandas as pd
from matplotlib.axes import Axes
from matplotlib import pyplot as plt

class FluentPlot:
    def __init__(self):
        super(FluentPlot, self).__init__()

        self._default_ax = None  # type: Optional[Axes]
        self._default_fig_size = None  # type: Optional[Tuple[float,float]]
        self._post_processing = []  # type: List[Callable[[Axes],Any]]

        self._title = None  # type: Optional[str]
        self._xlabel = None  # type: Optional[str]
        self._ylabel = None  # type: Optional[str]
        self._with_legend = False  # type: bool

        self._method = None
        self._iterate = False
        self._iterate_df_columns = False


    def __call__(self, obj: Any) -> Axes:
        if self._default_ax is not None:
            ax = self._default_ax
        elif self._default_fig_size is not None:
            _, ax = plt.subplots(1, 1, figsize=self._default_fig_size)
        else:
            _, ax = plt.subplots(1, 1, figsize=(12, 6))

        self._draw(obj, ax)

        if self._title is not None:
            ax.set_title(self._title)
        if self._xlabel is not None:
            ax.set_xlabel(self._xlabel)
        if self._ylabel is not None:
            ax.set_ylabel(self._ylabel)
        if self._with_legend:
            ax.legend()

        for post_proc in self._post_processing:
            post_proc(ax)

        return ax


    def _draw(self, obj, ax):
        if self._iterate:
            for item in obj:
                self._method(item, ax)
        elif self._iterate_df_columns:
            if not isinstance(obj,pd.DataFrame):
                raise ValueError('Value expect to be pd.Dataframe to do iterate over its columns')
            for c in obj.columns:
                item = obj[c]
                self._method(item, ax)
        else:
            self._method(obj, ax)


    def on(self, ax: Axes) -> 'FluentPlot':
        if ax is not None:
            self._default_ax = ax
        return self


    def size(self, width, height):
        self._default_fig_size = (width, height)
        return self


    def labels(self, title: Optional[str] = None, xlabel: Optional[str] = None,
               ylabel: Optional[str] = None) -> 'FluentPlot':
        self._title = title
        self._xlabel = xlabel
        self._ylabel = ylabel
        return self


    def with_legend(self) -> 'FluentPlot':
        self._with_legend = True
        return self


    def tune(self, method: Callable[[Axes], Any]) -> 'FluentPlot':
        self._post_processing.append(method)
        return self


    def call(self, method: Callable[[Any,Axes],Any]) -> 'FluentPlot':
        self._method = method
        return self

    def iterate(self, iterate=True) -> 'FluentPlot':
        self._iterate = iterate
        return self
    

    def iterate_df_columns(self, iterate_df_columns=True) -> 'FluentPlot':
        self._iterate_df_columns = iterate_df_columns
        return self

