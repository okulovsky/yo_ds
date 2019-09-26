from .._common import *
from .._push_queries import AggregationCodeFactory, agg
from yo_fluq._queries.queryable_code_factory import QueryableCodeFactory
from yo_fluq._common import *

class Queryable(Generic[T],AggregationCodeFactory,QueryableCodeFactory['Queryable',T]):
    def __init__(self,en,length=None):
        AggregationCodeFactory.__init__(self,self._aggregate_with)
        QueryableCodeFactory.__init__(self,en,length)

    def _aggregate_with(self, aggregator: agg.PushQueryElement):
        return aggregator(self.en)


