'''Classes which support the Queryable interface.'''

# Copyright (c) 2011-2016 Sixty North.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from typing import *
from functools import total_ordering as totally_ordered
import heapq


class Orderer:
    '''A Queryable representing an ordered iterable.

    The sorting implemented by this class is an incremental partial sort so
    you don't pay for sorting results which are never enumerated.'''

    def __init__(self, iterable, orderers: List[Tuple[int,Callable]]):
        '''Create an OrderedIterable.

            Args:
                iterable: The iterable sequence to be ordered.
                order: +1 for ascending, -1 for descending.
                func: The function to select the sorting key.
        '''
        self._iterable = iterable
        self._funcs = orderers


    def __iter__(self):
        '''Support for the iterator protocol.

        Returns:
            An iterator object over the sorted elements.
        '''

        # Determine which sorting algorithms to use
        directions = [direction for direction, _ in self._funcs]
        direction_total = sum(directions)
        if direction_total == -len(self._funcs):
            # Uniform ascending sort - do nothing
            MultiKey = tuple

        elif direction_total == len(self._funcs):
            # Uniform descending sort - invert sense of operators
            @totally_ordered
            class MultiKey(object):
                def __init__(self, t):
                    self.t = tuple(t)

                def __lt__(lhs, rhs):
                    # Uniform descending sort - swap the comparison operators
                    return lhs.t > rhs.t

                def __eq__(lhs, rhs):
                    return lhs.t == rhs.t
        else:
            # Mixed ascending/descending sort - override all operators
            @totally_ordered
            class MultiKey(object):
                def __init__(self, t):
                    self.t = tuple(t)

                # TODO: [asq 1.1] We could use some runtime code generation here to compile a custom comparison operator
                def __lt__(lhs, rhs):
                    for direction, lhs_element, rhs_element in zip(directions, lhs.t, rhs.t):
                        cmp = (lhs_element > rhs_element) - (rhs_element > lhs_element)
                        if cmp == direction:
                            return True
                        if cmp == -direction:
                            return False
                    return False # pragma: no cover

                def __eq__(lhs, rhs):
                    return lhs.t == rhs.t

        # Uniform ascending sort - decorate, sort, undecorate using tuple element
        def create_key(index, item):
            return MultiKey(func(item) for _, func in self._funcs)

        lst = [(create_key(index, item), index, item) for index, item in enumerate(self._iterable)]
        heapq.heapify(lst)
        while lst:
            key, index, item = heapq.heappop(lst)
            yield item
