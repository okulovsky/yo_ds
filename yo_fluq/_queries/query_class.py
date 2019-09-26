from .queryable import Queryable
from .._push_queries import PushQuery
from typing import *
from collections import Sized
from .._common import *
from .helpers import loop_maker

class QueryClass:
    def en(self, en: Iterable) -> Queryable:
        length = None
        if isinstance(en,Sized):
            length = len(en)
        return FlupFactory.QueryableFactory(en,length)

    def args(self, *args)  -> Queryable:
        return FlupFactory.QueryableFactory(args,len(args))


    def dict(self, dictionary: Dict)  -> Queryable:
        return FlupFactory.QueryableFactory(dictionary.items(),len(dictionary)).select(lambda z: KeyValuePair(z[0],z[1]))

    def push(self) -> PushQuery:
        return PushQuery()

    def loop(self, begin: Any, delta: Any, end: Any = None, endtype=LoopEndType.NotEqual):
        lp = loop_maker(begin,delta,end,endtype)
        return Queryable(lp.make())

