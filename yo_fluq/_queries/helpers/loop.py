from ..._common import LoopEndType

class loop_maker:
    def __init__(self, begin, delta, end, endType: LoopEndType):
        self.begin = begin
        self.delta = delta
        self.end = end
        self.endType = endType
        self.less_comparison = None

    def _cmp_less_like(self, left, right):
        if self.less_comparison is None: #pragma: no cover
            raise ValueError('loop_maker error: cmp is requested, but less_comparison was not set')
        if self.less_comparison:
            return left<right
        else:
            return left>right

    def make(self):
        value = self.begin

        if self.end is not None:
            if value==self.end:
                if self.endType != LoopEndType.NotEqual:
                    yield value
                return

        yield value

        value = value + self.delta
        if value > self.begin:
            self.less_comparison = True
        else:
            self.less_comparison = False

        if self.end is not None and not self._cmp_less_like(self.begin,self.end):
            raise ValueError('`end` and `delta` parameters are contradictory. ')

        while True:
            if self.end is None:
                yield value
                value+=self.delta
                continue

            if value == self.end:
                if self.endType != LoopEndType.NotEqual:
                    yield value
                break

            elif self._cmp_less_like(value,self.end):
                yield value
                value+=self.delta
                continue

            else:
                if self.endType == LoopEndType.Force:
                    yield self.end
                break