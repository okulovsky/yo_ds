from .._common import *


class partition_by_count:
    def __init__(self, count: int):
        self.count = count

    def _make(self, query):
        buffer = []
        for e in query:
            buffer.append(e)
            if len(buffer) == self.count:
                yield buffer
                buffer = []
        if len(buffer) > 0:
            yield buffer

    def __call__(self, query):
        return Queryable(self._make(query))



class partition_by_selector:
    def __init__(self, selector: Callable[[T],Any]):
        self.selector = selector

    def _make(self, query):
        buffer = []
        first_time = True
        old_field = None
        for e in query:
            if first_time:
                old_field = self.selector(e)
                buffer.append(e)
                first_time = False
                continue
            new_field = self.selector(e)
            if new_field!=old_field:
                yield buffer
                buffer = []
            buffer.append(e)
            old_field=new_field
        if len(buffer)>0:
            yield buffer

    def __call__(self, query):
        return Queryable(self._make(query))

