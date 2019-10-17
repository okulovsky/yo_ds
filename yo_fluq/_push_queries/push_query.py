from .._common import *
from .transformation import *
from .aggregation_code_factory import AggregationCodeFactory

class PushQuery(PushQueryElement, AggregationCodeFactory):
    def __init__(self):
        self.head = None  # type: Optional[PushQueryElement]
        self.tail = None  # type: Optional[PushQueryElement]
        AggregationCodeFactory.__init__(self,self.append)


    def append(self, pqe: PushQueryElement):
        if self.head is None:
            self.head = pqe
            self.tail = pqe
        else:
            self.tail.subscribe(pqe, None)
            self.tail = pqe
        return self

    def instance(self):
        if self.head is None:
            raise ValueError('PQEBuilder was not completed, HEAD is not set!')
        return self.head.instance()

    def select(self, selector: Callable) -> 'PushQuery':
        return self.append(SelectPQE(selector))

    def where(self, filter: Callable) ->'PushQuery':
        return self.append(WherePQE(filter))

    def select_many(self, selector: Callable) -> 'PushQuery':
        return self.append(SelectManyPQE(selector))

    def split_pipelines(self, **kwargs:PushQueryElement):
        pqe = SplitPipelines(**kwargs)
        return self.append(pqe)

    def split_by_group(self, group_selector, with_total = None):
        return self.append(SplitByGroup(group_selector, with_total))

    def split_dictionary(self):
        return self.append(SplitByDictionary())




