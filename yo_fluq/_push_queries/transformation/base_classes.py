from .._common import PushQueryElement, PushQueryElement
from collections import OrderedDict
from typing import *


class ObservableBase(PushQueryElement):
    def on_exit(factory, instance, exc_type, exc_val, exc_tb):
        for key, value in instance.subscribers.items():
            value.__exit__(exc_type, exc_val, exc_tb)


class SplitPipelines(ObservableBase):
    def __init__(self, *args: PushQueryElement, **kwargs: PushQueryElement):
        key_values = []
        for e in args:
            key = type(e).__name__.lower()
            key_values.append((key,e))
        for key, value in kwargs.items():
            key_values.append((key,value))
        self.pipelines = OrderedDict()
        for key, value in key_values:
            final_key = key
            for i in range(0,100):
                final_key = key+('' if i==0 else '_'+str(i))
                if final_key not in self.pipelines:
                    break
            self.pipelines[final_key]=value


    def on_enter(factory,instance):
        instance.subscribers = OrderedDict()
        for key, value in factory.pipelines.items():
            inst = value.instance()
            inst.__enter__()
            instance.subscribers[key] = inst

    def on_process(factory, instance, element):
        for value in instance.subscribers.values():
            value.process(element)

    def on_report(factory, instance):
        return {key: value.report() for key, value in instance.subscribers.items()}


class ObservableAbstract(ObservableBase):
    def __init__(self):
        self.subscribers = OrderedDict()  # type: Dict[Any,PushQueryElement]

    def subscribe(self, pqe: PushQueryElement, name):
        self.subscribers[name] = pqe

    def on_enter(factory, instance):
        instance.subscribers = OrderedDict()
        for key, value in factory.subscribers.items():
            inst = value.instance()
            inst.__enter__()
            instance.subscribers[key] = inst

    def push_element(factory, instance, element):
        for value in instance.subscribers.values():
            value.process(element)



class SelectPQE(ObservableAbstract):
    def __init__(self, selector: Callable):
        super(SelectPQE, self).__init__()
        self.selector = selector

    def on_process(factory, instance, element):
        factory.push_element(instance, factory.selector(element))

    def on_report(factory, instance):
        for value in instance.subscribers.values():
            return value.report()



class SelectManyPQE(ObservableAbstract):
    def __init__(self, selector: Callable):
        super(SelectManyPQE, self).__init__()
        self.selector = selector

    def on_process(factory, instance, element):
        for smaller_element in factory.selector(element):
            factory.push_element(instance, smaller_element)

    def on_report(factory, instance):
        for value in instance.subscribers.values():
            return value.report()



class WherePQE(ObservableAbstract):
    def __init__(self, filter: Callable):
        super(WherePQE, self).__init__()
        self.filter = filter

    def on_process(factory, instance, element):
        if factory.filter(element):
            factory.push_element(instance, element)

    def on_report(factory, instance):
        for value in instance.subscribers.values():
            return value.report()



class Dispatch(ObservableBase):
    def __init__(self):
        self.continuation = None  # type: Optional[PushQueryElement]

    def subscribe(self, pqe, name):
        if self.continuation is None:
            self.continuation = pqe
        else: #pragma: no cover
            raise ValueError('There is already one subscriber, and Dispatch does not accept more')


    def on_enter(factory, instance):
        instance.subscribers = OrderedDict()

    def push_to_bucket(factory, instance, element, bucket):
        if factory.continuation is None: #pragma: no cover
            raise ValueError('Cannot route: the continuation is not set')
        if bucket not in instance.subscribers:
            instance.subscribers[bucket] = factory.continuation.instance()
            instance.subscribers[bucket].__enter__()
        instance.subscribers[bucket].process(element)


    def on_report(factory, instance):
        return {key: value.report() for key, value in instance.subscribers.items()}



class SplitByGroup(Dispatch):
    def __init__(self, group_selector, with_total=None):
        super(SplitByGroup, self).__init__()
        self.group_selector = group_selector
        self.with_total = with_total

    def on_process(factory, instance, element):
        bucket = factory.group_selector(element)
        factory.push_to_bucket(instance, element, bucket)
        if factory.with_total is not None:
            factory.push_to_bucket(instance, element, factory.with_total)


class SplitByDictionary(Dispatch):
    def __init__(self):
        super(SplitByDictionary, self).__init__()

    def on_process(factory, instance, element):
        if not isinstance(element, dict):
            raise ValueError('SplitByDictionary expects disctionaries!')
        for key, value in element.items():
            factory.push_to_bucket(instance, value, key)
