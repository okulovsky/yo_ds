from . import aggregation as agg
from .transformation import SplitPipelines
from typing import *

class _NoDefault:
    pass

class AggregationCodeFactory:
    def __init__(self, method_concatenator: Callable):
        self.method_concatenator = method_concatenator

    def first(self):
        return self.method_concatenator(agg.First())

    def first_or_default(self, default=None):
        return self.method_concatenator(agg.First().default_if_empty(default))

    def last(self):
        return self.method_concatenator(agg.Last())

    def last_or_default(self, default=None):
        return self.method_concatenator(agg.Last().default_if_empty(default))

    def single(self):
        return self.method_concatenator(agg.Single())

    def single_or_default(self, default=None):
        return self.method_concatenator(agg.Single().default_if_empty(default))

    def min(self, selector : Callable = lambda z: z, default = _NoDefault()):
        a = agg.Min(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self.method_concatenator(a)

    def max(self, selector: Callable = lambda z: z, default = _NoDefault()):
        a = agg.Max(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self.method_concatenator(a)

    def argmin(self, selector: Callable = lambda z: z, default = _NoDefault()):
        a = agg.ArgMin(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self.method_concatenator(a)

    def argmax(self, selector: Callable = lambda z: z, default = _NoDefault()):
        a = agg.ArgMax(selector)
        if not isinstance(default, _NoDefault):
            a = a.default_if_empty(default)
        return self.method_concatenator(a)

    def sum(self):
        return self.method_concatenator(agg.Sum())

    def mean(self):
        return self.method_concatenator(agg.Mean())

    def count(self):
        return self.method_concatenator(agg.Count())

    def any(self, selector: Optional[Callable] = None):
        return self.method_concatenator(agg.Any(selector))

    def all(self, selector: Optional[Callable] = None):
        return self.method_concatenator(agg.All(selector))

    def to_list(self):
        return self.method_concatenator(agg.ToList())

    def to_dictionary(self, key_selector: Optional[Callable] = None, value_selector: Optional[Callable] = None):
        return self.method_concatenator(agg.ToDictionary(key_selector, value_selector))

    def to_set(self):
        return self.method_concatenator(agg.ToSet())

    def to_tuple(self):
        return self.method_concatenator(agg.ToTuple())

    def aggregate_with(self, *args: agg.PushQueryElement):
        if len(args)==1:
            return self.method_concatenator(args[0])
        else:
            return self.method_concatenator(SplitPipelines(*args))
