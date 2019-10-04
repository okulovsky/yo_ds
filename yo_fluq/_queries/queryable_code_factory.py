from typing import *
from .._common import *
from .helpers import *
import itertools


class QueryableCodeFactory(Generic[TFactory,T]):
    def __init__(self, en, length):
        self.en = en
        self.length = length

    def __iter__(self):
        for e in self.en:
            yield e

    def select(self, selector: Callable[[T], TOut]) -> TFactory:
        return FlupFactory.QueryableFactory(map(selector, self.en), self.length)

    def where(self, filterSelector: Callable[[T], bool]) -> TFactory:
        return FlupFactory.QueryableFactory(filter(filterSelector, self.en))

    def distinct(self, selector: Optional[Callable[[T], TOut]] = None) -> TFactory:
        return FlupFactory.QueryableFactory(distinct(self.en, selector))

    def select_many(self, selector: Callable[[T], Iterable[TOut]]) -> TFactory:
        return FlupFactory.QueryableFactory(itertools.chain.from_iterable(map(selector, self.en)))

    def with_indices(self) -> TFactory:
        return FlupFactory.QueryableFactory(with_indices(self.en), self.length)

    def group_by(self, selector: Callable[[T], TKey]) -> TFactory:
        return FlupFactory.QueryableFactory(group_by(self.en, selector))


    def skip(self, count) -> TFactory:
        return FlupFactory.QueryableFactory(itertools.islice(self.en, count, None))

    def take(self, count) -> TFactory:
        return FlupFactory.QueryableFactory(itertools.islice(self.en, count))

    def skip_while(self, condition) -> TFactory:
        return FlupFactory.QueryableFactory(skip_while(self.en, condition))

    def take_while(self, condition) -> TFactory:
        return FlupFactory.QueryableFactory(take_while(self.en, condition))

    def append(self, *args: T) -> TFactory:
        return FlupFactory.QueryableFactory(append(self.en, args))

    def prepend(self, *args: T) -> TFactory:
        return FlupFactory.QueryableFactory(prepend(self.en, args))

    def intersect(self, en2: Iterable[T]) -> TFactory:
        return FlupFactory.QueryableFactory(intersect(self.en, en2))

    def concat(self, en2: Iterable[T]) -> TFactory:
        return FlupFactory.QueryableFactory(concat(self.en, en2))

    def order_by(self, selector: Callable[[T], Any]) -> TFactory:
        return FlupFactory.QueryableFactory(Orderer(self.en, [(-1, selector)]), self.length)

    def order_by_descending(self, selector: Callable[[T], Any]) -> TFactory:
        return FlupFactory.QueryableFactory(Orderer(self.en, [(1, selector)]), self.length)

    def then_by(self, selector: Callable[[T], Any]) -> TFactory:
        if not isinstance(self.en, Orderer):
            raise ValueError('then_by can only be called directly after order_by or order_by_descending')
        return FlupFactory.QueryableFactory(Orderer(self.en, self.en._funcs + [(-1, selector)]), self.length)

    def then_by_descending(self, selector: Callable[[T], Any]) -> TFactory:
        if not isinstance(self.en, Orderer):
            raise ValueError('then_by can only be called directly after order_by or order_by_descending')
        return FlupFactory.QueryableFactory(Orderer(self.en, self.en._funcs + [(1, selector)]), self.length)

    def foreach(self, action: Callable[[T], None]) -> None:
        foreach(self.en, action)

    def foreach_and_continue(self, action: Callable[[T], None]) -> TFactory:
        return FlupFactory.QueryableFactory(foreach_and_continue(self.en, action), self.length)


    def fork(self, context: ForkContext, pipeline: Callable[[Any, Iterable[T]], Any]):
        return FlupFactory.QueryableFactory(fork(self.en, context, pipeline))

    def fire_and_forget(self, pipeline: Callable[[Iterable[T]], Any]):
        return FlupFactory.QueryableFactory(fork(self.en, ForkContext(None), lambda q, _: pipeline(q)))

    def parallel_select(self, selector, workers_count=None, buffer_size=1):
        return FlupFactory.QueryableFactory(parallel_select(self.en, selector, workers_count, buffer_size), self.length)

    def feed(self, collector: Callable[[Any],T]) -> T:
        return collector(self)

    def aggregate(self, aggregator):
        return aggregate(self.en, aggregator)





