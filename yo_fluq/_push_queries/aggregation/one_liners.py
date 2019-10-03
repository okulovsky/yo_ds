from .._common import *
import math

class Sum(ArithmeticPQE):
    def __init__(self):
        super(Sum, self).__init__(
            lambda: 0,
            lambda state,element: state+element,
            lambda state: state,
            True,
            None
        )

class Count(ArithmeticPQE):
    def __init__(self):
        super(Count, self).__init__(
            lambda: 0,
            lambda state,element: state+1,
            lambda state:state,
            False
        )

class Mean(ArithmeticPQE):
    def __init__(self):
        super(Mean, self).__init__(
            lambda: (0,0),
            lambda state,element: (state[0]+element,state[1]+1),
            lambda state: state[0]/state[1],
            False,
            None
        )

class Std(ArithmeticPQE):
    @staticmethod
    def _process(state, element):
        mean, count, M2 = state
        count+=1
        delta = element - mean
        mean += delta / count
        delta2 = element - mean
        M2 += delta * delta2
        return (mean,count,M2)

    @staticmethod
    def _exit(state):
        mean, count, M2= state
        if count < 2:
            return None
        return math.sqrt(M2 / count)

    def __init__(self):
        super(Std, self).__init__(
            lambda: (0,0,0),
            Std._process,
            Std._exit,
            False
        )

class First(ArithmeticPQE):
    def __init__(self):
        super(First, self).__init__(
            lambda: (True, None),
            lambda state, element: (False,element) if state[0] else (False,state[1]),
            lambda state: state[1],
            True,
            None,
            lambda state: StopIteration() if not state[0] else None
        )

class Last(ArithmeticPQE):
    def __init__(self):
        super(Last, self).__init__(
            lambda: None,
            lambda state, element: element,
            lambda state: state,
            True
        )

class Single(ArithmeticPQE):
    @staticmethod
    def _process(state,element):
        if not state[0]:
            raise ValueError('Sequence contains more than one element')
        return (False,element)

    def __init__(self):
        super(Single, self).__init__(
            lambda: (True,None),
            Single._process,
            lambda state: state[1],
            True)


class Max(ArithmeticPQE):
    def __init__(self, value_selector = lambda z:z):
        super(Max, self).__init__(
            lambda: (True,None),
            lambda state, element: (False,value_selector(element)) if state[0] else (False,max(state[1],value_selector(element))),
            lambda state: state[1],
            True
        )

class Min(ArithmeticPQE):
    def __init__(self, value_selector = lambda z:z):
        super(Min, self).__init__(
            lambda: (True,None),
            lambda state, element: (False,value_selector(element)) if state[0] else (False,min(state[1],value_selector(element))),
            lambda state: state[1],
            True
        )

class _ProcessorArgMinMax:
    def __init__(self,value_selector,is_argmin):
        self.is_argmin = is_argmin
        self.value_selector = value_selector

    def _process(self, state,element):
        first_time, cur_value, cur_element = state
        value = self.value_selector(element)
        if first_time:
            return (False, value, element)
        elif (value < cur_value and self.is_argmin) or (value > cur_value and not self.is_argmin):
            return (False, value, element)
        else:
            return (False, cur_value, cur_element)


class ArgMin(ArithmeticPQE):
    def __init__(self, value_selector=lambda z: z):
        pr = _ProcessorArgMinMax(value_selector,True)
        super(ArgMin, self).__init__(
            lambda: (True, None, None),
            pr._process,
            lambda state: state[2],
            True
        )


class ArgMax(ArithmeticPQE):
    def __init__(self, value_selector=lambda z: z):
        pr = _ProcessorArgMinMax(value_selector,False)
        super(ArgMax, self).__init__(
            lambda: (True, None, None),
            pr._process,
            lambda state: state[2],
            True
        )

def _all_any_value_selectors(value):
    if isinstance(value,bool):
        return value
    return True

class All(ArithmeticPQE):
    def __init__(self, value_selector=None):
        if value_selector is None:
            value_selector = _all_any_value_selectors
        super(All, self).__init__(
            lambda: True,
            lambda state, element: state and value_selector(element),
            lambda state: state,
            False
        )

class Any(ArithmeticPQE):
    def __init__(self, value_selector=None):
        if value_selector is None:
            value_selector = _all_any_value_selectors
        super(Any, self).__init__(
            lambda: False,
            lambda state, element: state or value_selector(element),
            lambda state: state,
            False
        )


