from enum import Enum

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        raise NotImplementedError()

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        raise NotImplementedError()

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        raise NotImplementedError()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        raise NotImplementedError()