import copy
from ..._common import *
from collections import OrderedDict


def intersect(en1, en2):
    en2=set(en2)
    for e in en1:
        if e in en2:
            yield e

def concat(en1, en2):
    for e in en1:
        yield e
    for e in en2:
        yield e


def skip_while(en, condition):
    make_yield = False
    for e in en:
        if not make_yield and not condition(e):
            make_yield = True
        if make_yield:
            yield e

def take_while(en, condition):
    for e in en:
        if not condition(e):
            break
        yield e


class Group(KeyValuePair[TKey,List[TValue]]):
    def __init__(self, key: TKey, values: List[TValue]):
        super(Group, self).__init__(key,values)

    def __iter__(self):
        for e in self.value:
            yield e

    def __len__(self):
        return len(self.value)


def group_by(en,selector):
    groups = OrderedDict()
    for e in en:
        key = selector(e)
        if key not in groups:
            groups[key]=[e]
        else:
            groups[key].append(e)

    for key, value in groups.items():
        yield Group(key,value)



def aggregate(en, aggregator):
    value = None
    firstTime = True
    for e in en:
        if firstTime:
            firstTime=False
            value = e
        else:
            value = aggregator(value,e)
    return value


def distinct(en, selector):
    seen = set()
    for e in en:
        key = e
        if selector is not None:
            key = selector(e)
        if key in seen:
            continue
        seen.add(key)
        yield e
