from .._common import *
from collections import OrderedDict
import numpy as np

def strjoin(separator: str):
    return lambda en: separator.join(Query.en(en).select(str))


class pairwise:
    def __init__(self):
        pass

    def _make(self, en):
        old = None
        firstTime = True
        for e in en:
            if not firstTime:
                yield (old, e)
            old = e
            if firstTime:
                firstTime = False

    def __call__(self, en):
        return Queryable(self._make(en))


class count_by:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, en):
        result = OrderedDict()
        for e in en:
            gr = self.selector(e)
            if gr not in result:
                result[gr] = 0
            result[gr] += 1
        return Query.dict(result)


class shuffle:
    def __init__(self, random_state: Union[np.random.RandomState,int,None,bool]):
        if random_state is None:
            self.random_state = None
        elif isinstance(random_state,bool):
            if random_state:
                self.random_state = np.random.RandomState(np.random.randint(0,1000000))
            else:
                self.random_state = None
        elif isinstance(random_state,int):
            self.random_state = np.random.RandomState(random_state)
        elif isinstance(random_state,np.random.RandomState):
            self.random_state = random_state
        else:
            raise TypeError('random_state must be None, int, bool or RandomState, but was {0}'.format(type(random_state)))

    def _call_iter(self, lst):
        permutation = self.random_state.permutation(len(lst))
        for p in permutation:
            yield lst[p]

    def __call__(self, en):
        if self.random_state is None:
            return en
        lst = np.array(list(en))
        return Queryable(self._call_iter(lst),length=len(lst))
