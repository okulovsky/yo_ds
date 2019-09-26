from typing import *
import pandas as pd
import numpy as np

class _SideTrimmer:
    def __init__(self, mode, value, percentile):
        self.mode = mode
        self.value = value
        self.percentile = percentile

    def process(self, series, before):
        value = self.value
        data = np.array(series)
        if self.percentile is not None:
            value = np.percentile(data, self.percentile)
        if before:
            pattern = series > value
        else:
            pattern = series < value
        if self.mode == 'drop':
            return series[pattern]
        else:
            return series.where(pattern, value)


class trimmer(Callable[[pd.Series], pd.Series]):
    def __init__(self,
                 drop_before: Optional[float]=None,
                 drop_before_percentile: Optional[float]=None,
                 unite_before: Optional[float] =None,
                 unite_before_percentile: Optional[float] =None,
                 drop_after: Optional[float] =None,
                 drop_after_percentile: Optional[float] =None,
                 unite_after: Optional[float] =None,
                 unite_after_percentile: Optional[float] =None):
        self.before = None
        self.after = None

        if drop_before is not None:
            self.before = _SideTrimmer('drop', drop_before, None)
        if drop_before_percentile is not None:
            self.before = _SideTrimmer('drop', None, drop_before_percentile)
        if unite_before is not None:
            self.before = _SideTrimmer('unite', unite_before, None)
        if unite_before_percentile is not None:
            self.before = _SideTrimmer('unite', None, unite_before_percentile)

        if drop_after is not None:
            self.after = _SideTrimmer('drop', drop_after, None)
        if drop_after_percentile is not None:
            self.after = _SideTrimmer('drop', None, drop_after_percentile)
        if unite_after is not None:
            self.after = _SideTrimmer('unite', unite_after, None)
        if unite_after_percentile is not None:
            self.after = _SideTrimmer('unite', None, unite_after_percentile)

    def __call__(self, series: pd.Series) ->pd.Series:
        if self.before is not None:
            series = self.before.process(series, True)
        if self.after is not None:
            series = self.after.process(series, False)
        return series
