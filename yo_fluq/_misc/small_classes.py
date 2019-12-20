from typing import *
from enum import Enum

T = TypeVar('T')
TOut = TypeVar('TOut')
TKey = TypeVar('TKey')
TValue = TypeVar('TValue')
TFactory = TypeVar('TFactory')

class KeyValuePair(Generic[TKey,TValue]):
    def __init__(self, key: TKey, value: TValue):
        self.key = key
        self.value = value

    def __repr__(self):
        return dict(key=self.key,value=self.value).__repr__()

    def __str__(self):
        return dict(key=self.key, value=self.value).__str__()

class ItemWithIndex(KeyValuePair):
    def __init__(self, key, value):
        super(ItemWithIndex, self).__init__(key,value)
        self.index = key
        self.item = value

class ForkContext:
    def __init__(self, data_to_send):
        self.sent = data_to_send
        self.received = None
        self.result = None

class FlupFactory:
    QueryableFactory = None
    QueryFactory = None


class LoopEndType(Enum):
    NotEqual = 0
    Equal = 1
    Force = 2