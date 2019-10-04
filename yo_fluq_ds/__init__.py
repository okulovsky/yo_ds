from yo_fluq import PushQueryElement
from ._push_queries import aggregations as agg
from . import _fluq as fluq
from ._misc import *
from ._queries import QueryClass,Queryable



FlupFactory.QueryableFactory = Queryable
FlupFactory.QueryFactory = QueryClass

Query = QueryClass()


import pandas as pd
from typing import *

T = TypeVar('T')
TOut = TypeVar('TOut')

def _feed(object: T, method: Callable[[T],TOut])->TOut:
    return method(object)




pd.Series.feed = _feed
pd.DataFrame.feed = _feed
pd.core.groupby.DataFrameGroupBy.feed = _feed
pd.core.groupby.SeriesGroupBy.feed = _feed

    