import math
from matplotlib import pyplot as plt
import tqdm
from typing import *
from matplotlib.axes import Axes
from .._common import *



class ItemWithPlot(Generic[T]):
    def __init__(self, item: T, ax: Axes, all_axes = Any):
        self.item = item
        self.ax = ax
        self._all_axes = all_axes


class with_plots:
    def __init__(self,columns: int, figsize: Tuple[int,int] = (5,3), name_selector : Callable[[Any],str] = lambda x: str(x)):
        self.columns = columns
        self.figsize = figsize
        self.name_selector = name_selector

    def _make(self, q):
        q = q.to_list()
        count = len(q)
        rows = int(math.ceil(count / self.columns))
        fig, axes = plt.subplots(rows, self.columns, figsize=(self.figsize[0] * self.columns, self.figsize[1] * rows))

        r_ax = [axes]
        if isinstance(axes,Collection):
            if isinstance(axes[0],Collection):
                r_ax = Query.en(axes).select_many(lambda z: z).to_list()
            else:
                r_ax = list(axes)

        for ax, element in zip(r_ax,q):
            if self.name_selector is not None:
                ax.set_title(self.name_selector(element))
            yield ItemWithPlot(element, ax, axes)

    def __call__(self, q):
        return Queryable(self._make(q),q.length)


def _isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


class with_progress_bar:
    def __init__(self, hide=False, console=None, **kwargs):
        if console is None:
            console = not _isnotebook()
        self.console = console
        self.hide = hide
        self.kwargs = kwargs

    def __call__(self, q):
        if self.hide:
            return q
        try:
            length = q.length
            if length is not None:
                self.kwargs['total'] = length
        except:
            pass
        if not self.console:
            return Queryable(tqdm.tqdm_notebook(q, **self.kwargs),q.length)
        else:
            return Queryable(tqdm.tqdm(q, **self.kwargs),q.length)

