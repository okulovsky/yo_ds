from .._common import *
import copy

class _NoSpecialCase:
    pass

class AbstractPushQueryElement:
    def instance(self): #pragma: no cover
        raise NotImplementedError()

    def subscribe(self, pqe, name):
        raise ValueError('This Element is not subscribable')

    def __call__(self, enumerable: Iterable):
        with self.instance() as agg:
            for element in enumerable:
                process_result = agg.process(element)
                if isinstance(process_result,StopIteration):
                    break
            return agg.report()


class AbstractPushQueryElementInstance:
    def __enter__(self): #pragma: no cover
        raise NotImplementedError()

    def process(self, element): #pragma: no cover
        pass

    def report(self): #pragma: no cover
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class _ArithmeticPQEI(AbstractPushQueryElementInstance):
    def __init__(self,
                 enter_lambda,
                 process_lambda,
                 report_lambda,
                 throw_if_empty,
                 value_if_empty,
                 rettype,
                 stop_iteration_lambda
                 ):
        self._enter_lambda = enter_lambda
        self._process_lambda = process_lambda
        self._report_lambda = report_lambda
        self._throw_if_empty = throw_if_empty
        self._value_if_empty = value_if_empty
        self._rettype = rettype
        self._stop_iteration_lambda = stop_iteration_lambda

    def __enter__(self):
        self._count = 0
        self._state = self._enter_lambda()
        return self

    def process(self, element):
        self._count+=1
        self._state = self._process_lambda(self._state, element)
        ret_status = self._stop_iteration_lambda(self._state)
        return ret_status

    def report(self):
        if self._count == 0:
            if self._throw_if_empty:
                raise ValueError('The sequence was empty')
            elif not isinstance(self._value_if_empty,_NoSpecialCase):
                result = self._value_if_empty
            else:
                result = self._report_lambda(self._state)
        else:
            result = self._report_lambda(self._state)
        if self._rettype is not None:
            result = self._rettype(result)
        return result



class ArithmeticPQE(AbstractPushQueryElement):
    def __init__(self,
                 enter_lambda,
                 process_lambda,
                 report_lambda,
                 throw_if_empty,
                 value_if_empty = _NoSpecialCase(),
                 stop_iterations_lambda = lambda z: None):
        self._enter_lambda = enter_lambda
        self._process_lambda = process_lambda
        self._report_lambda = report_lambda
        self._throw_if_empty = throw_if_empty
        self._rettype = None
        self._value_if_empty = value_if_empty
        self._stop_iterations_lambda = stop_iterations_lambda

    def instance(self):
        return _ArithmeticPQEI(
            self._enter_lambda,
            self._process_lambda,
            self._report_lambda,
            self._throw_if_empty,
            self._value_if_empty,
            self._rettype,
            self._stop_iterations_lambda
        )

    def throw_if_empty(self):
        result = copy.deepcopy(self)
        result._throw_if_empty = True
        return result

    def default_if_empty(self, default_value = None):
        result = copy.deepcopy(self)
        result._throw_if_empty = False
        result._value_if_empty = default_value
        return result

    def astype(self, rettype):
        result = copy.deepcopy(self)
        result._rettype = rettype
        return result


class _PushQueryElementInstance(AbstractPushQueryElementInstance):
    def __init__(self, enter_function, process_function, report_function, exit_function):
        self.enter_function = enter_function
        self.process_function = process_function
        self.report_function = report_function
        self.exit_function = exit_function

    def __enter__(self):
        self.enter_function(self)
        return self

    def process(self, element):
        return self.process_function(self, element)

    def report(self):
        return self.report_function(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.exit_function(self,exc_type, exc_val, exc_tb)


class PushQueryElement(AbstractPushQueryElement):
    def instance(self):
        return _PushQueryElementInstance(
            self.on_enter,
            self.on_process,
            self.on_report,
            self.on_exit
        )

    def on_enter(factory,instance): #pragma: no cover
        raise NotImplementedError()

    def on_process(factory, instance, element): #pragma: no cover
        raise NotImplementedError()

    def on_report(factory, instance): #pragma: no cover
        raise NotImplementedError()

    def on_exit(factory, instance,exc_type, exc_val, exc_tb):
        pass



