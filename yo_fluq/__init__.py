from ._queries import QueryClass, Queryable
from ._push_queries import aggregation as agg, PushQueryElement
from ._misc import *

FlupFactory.QueryableFactory = Queryable
FlupFactory.QueryFactory = QueryClass
Query = QueryClass()

