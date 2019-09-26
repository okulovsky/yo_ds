from typing import *
import pandas as pd
from matplotlib.axes import Axes
from matplotlib import pyplot as plt


class _method_wrap(Callable):
    def __init__(self, method, ax_argument_name='ax'):
        self.method = method
        self.ax_argument_name = ax_argument_name

    def __call__(self, obj, ax, *args, **kwargs):
        kwargs[self.ax_argument_name] = ax
        self.method(*args,**kwargs)


class _obj_method_wrap(Callable):
    def __init__(self, method_selector, ax_argument_name='ax'):
        self.method_selector = method_selector
        self.ax_argument_name = ax_argument_name

    def __call__(self, obj, ax, *args, **kwargs):
        kwargs[self.ax_argument_name] = ax
        method = self.method_selector(obj)
        method(*args,**kwargs)




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
        self._args = None
        self._kwargs = None
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


    def _make_args(self, obj):
        args = [a(obj) if callable(a) else a for a in self._args]
        return args


    def _make_kwargs(self, obj):
        kwargs = {key: (value(obj) if callable(value) else value) for key, value in self._kwargs.items()}
        return kwargs


    def _draw(self, obj, ax):
        if self._iterate:
            for item in obj:
                self._method(item, ax, *self._make_args(item), **self._make_kwargs(item))
        elif self._iterate_df_columns:
            if not isinstance(obj,pd.DataFrame):
                raise ValueError('Value expect to be pd.Dataframe to do iterate over its columns')
            for c in obj.columns:
                item = obj[c]
                self._method(item, ax, *self._make_args(item), **self._make_kwargs(item))
        else:
            self._method(obj, ax, *self._make_args(obj), **self._make_kwargs(obj))


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


    def call_ax(self, ax_selector: Callable[[Axes],Callable]) -> 'FluentPlot':
        self._method = lambda obj, ax, *args, **kwargs: ax_selector(ax)(*args,**kwargs)
        return self

    def call_obj(self, obj_method_selector, ax_argument_name='ax') -> 'FluentPlot':
        self._method = _obj_method_wrap(obj_method_selector, ax_argument_name)
        return self

    def call(self, method, ax_argument_name='ax') -> 'FluentPlot':
        self._method = _method_wrap(method, ax_argument_name)
        return self


    def args(self, *args, **kwargs) -> 'FluentPlot':
        self._args = args
        self._kwargs = kwargs
        return self


    def iterate(self, iterate=True) -> 'FluentPlot':
        self._iterate = iterate
        return self
    

    def iterate_df_columns(self, iterate_df_columns=True) -> 'FluentPlot':
        self._iterate_df_columns = iterate_df_columns
        return self

