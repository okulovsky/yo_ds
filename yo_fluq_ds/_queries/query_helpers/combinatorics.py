from ..._common import *
from ..queryable import Queryable
import itertools

def _grid_iter(keys,lists):
    for config in itertools.product(*lists):
        yield Obj(**{key: value for key, value in zip(keys, config)})


def _grid_dict(dict):
    keys = list(dict)
    lists = [dict[key] for key in keys]
    length = 1
    for l in lists:
        length *= len(l)
    return Queryable(_grid_iter(keys, lists), length)



def _grid_args(args):
    length = 1
    for l in args:
        length*=len(l)
    return Queryable(itertools.product(*args),length)



def _triangle_iter(items,with_diagonal):
    for index1,item1 in enumerate(items):
        begin = index1
        if not with_diagonal:
            begin+=1
        for index2 in range(begin,len(items)):
            item2=items[index2]
            yield (item1,item2)

T = TypeVar('T')

from itertools import combinations

def _powerset_iter(iterable):
    xs = list(iterable)
    for i in range(len(xs)+1):
        for p in combinations(xs,i):
            yield p


class CombinatoricsQuery:
    def grid(self, **kwargs)->Queryable[Obj]:
        return _grid_dict(kwargs)

    def grid_dict(self, dict) -> Queryable[Obj]:
        return _grid_dict(dict)

    def cartesian(self,*args)->Queryable[Tuple]:
        return _grid_args(args)

    def triangle(self, items: T, with_diagonal=True) -> Queryable[Tuple[T, T]]:
        return Queryable(_triangle_iter(items, with_diagonal), (len(items) * (len(items) - 1)) // 2)

    def powerset(self, iterable: Iterable[T]) -> Queryable[Tuple]:
        return Queryable(_powerset_iter(iterable))













