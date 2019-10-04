from typing import *
import pandas as pd

class fractions(Callable[[Union[pd.core.groupby.DataFrameGroupBy,pd.Series]],pd.Series]):
    def __init__(self):
        pass

    def __call__(self,
                 data: Union[pd.core.groupby.DataFrameGroupBy,pd.Series]) -> pd.Series:
        if isinstance(data,pd.core.groupby.DataFrameGroupBy):
            size = data.size()
            return size/size.sum()
        elif isinstance(data,pd.Series):
            return data/data.sum()
        else:
            raise TypeError('Only Series, DataFrameGroupBy are supported')

