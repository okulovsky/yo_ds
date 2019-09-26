from .._common import *

class ToList(PushQueryElement):
    def on_enter(factory,instance):
        instance._list = []

    def on_process(factory, instance, element):
        instance._list.append(element)

    def on_report(factory, instance):
        return instance._list


class ToTuple(PushQueryElement):
    def on_enter(factory, instance):
        instance._list = []

    def on_process(factory, instance, element):
        instance._list.append(element)

    def on_report(factory, instance):
        return tuple(instance._list)


class ToSet(PushQueryElement):
    def on_enter(factory,instance):
        instance._set = set()

    def on_process(factory, instance, element):
        if element in instance._set:
            raise ValueError('Duplicating element {0}'.format(element))
        instance._set.add(element)

    def on_report(factory, instance):
        return instance._set

class ToDictionary(PushQueryElement):
    def __init__(self, key_selector: Optional[Callable] = None, value_selector: Optional[Callable] = None):
        if (key_selector is None) != (value_selector is None):
            raise ValueError('KeySelector and ValueSelector must be defined both or none of them')
        self.key_selector = key_selector
        self.value_selector = value_selector

    def on_enter(factory,instance):
        instance._dict = {}
        instance._first_time = True
        instance._await_key_value_pair = None
        instance.key_selector = factory.key_selector
        instance.value_selector = factory.value_selector

    def on_process(factory, instance, element):
        if instance._first_time:
            if isinstance(element,KeyValuePair):
                instance._await_key_value_pair = True
                if instance.key_selector is None:
                    instance.key_selector = lambda z: z.key
                if instance.value_selector is None:
                    instance.value_selector = lambda z: z.value
            else:
                instance._await_key_value_pair = False
                if instance.key_selector is None or instance.value_selector is None:
                    raise ValueError('KeySelector/ValueSelector are not specified, but sequence does not consist of key/value pairs')
            instance._first_time = False
        else:
            if instance._await_key_value_pair != isinstance(element,KeyValuePair):
                raise ValueError("The sequence is a mixture of KeyValue pair and other types. This is not allowed")

        key = instance.key_selector(element)
        if key in instance._dict:
            raise ValueError('Duplicating value for key {0}'.format(key))
        instance._dict[key]=instance.value_selector(element)

    def on_report(factory, instance):
        return instance._dict

