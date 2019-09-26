from .._common import *
from yo_fluq import *
Queryable = lambda *args, **kwargs: FlupFactory.QueryableFactory(*args, **kwargs)
T = TypeVar('T')
TOut = TypeVar('TOut')
TKey = TypeVar('TKey')
TValue = TypeVar('TValue')
TFactory = TypeVar('TFactory')