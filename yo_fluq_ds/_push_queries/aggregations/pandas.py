from .._common import *
import pandas as pd
import numpy as np

class ToDataframe(yo_fluq.agg.PushQueryElement):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def on_enter(factory,instance):
        instance.lst = []

    def on_process(factory, instance, element):
        instance.lst.append(element)

    def on_report(factory, instance):
        return pd.DataFrame(instance.lst,**factory.kwargs)


class ToNDArray(yo_fluq.agg.PushQueryElement):
    def on_enter(factory,instance):
        instance.lst = []

    def on_process(factory, instance, element):
        instance.lst.append(element)

    def on_report(factory, instance):
        return np.array(instance.lst)


class ToSeries(yo_fluq.agg.PushQueryElement):
    def __init__(self, value_selector : Optional[Callable] = None, key_selector : Optional[Callable] = None, **kwargs):
        self.value_selector = value_selector
        self.key_selector = key_selector
        self.kwargs = kwargs

    def on_enter(factory,instance):
        instance.values = []
        instance.keys = []
        instance.first_time = True
        instance.accepts_key_value_pair = None
        instance.key_selector = factory.key_selector
        instance.value_selector = factory.value_selector
        instance.kwargs = factory.kwargs

    def on_process(factory, instance, element):
        if instance.first_time:
            if isinstance(element, yo_fluq.KeyValuePair):
                instance.accepts_key_value_pair = True
                if instance.value_selector is None:
                    instance.value_selector = lambda z: z.value
                if instance.key_selector is None:
                    instance.key_selector = lambda z: z.key
            else:
                instance.accepts_key_value_pair = False
                if instance.value_selector is None:
                    instance.value_selector = lambda z: z
            instance.first_time = False
        else:
            if isinstance(element, yo_fluq.KeyValuePair) != (instance.accepts_key_value_pair):
                raise ValueError('The sequence is the mixture of keyvalue pairs and onther types, which is not allowed')

        instance.values.append(instance.value_selector(element))
        if instance.key_selector is not None:
            instance.keys.append(instance.key_selector(element))

    def on_report(factory, instance):
        if instance.key_selector is None:
            return pd.Series(instance.values,**instance.kwargs)
        else:
            return pd.Series(instance.values, instance.keys, **instance.kwargs)



