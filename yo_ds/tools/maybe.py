
class mb_call:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._with_try_catch = False

    def try_catch(self):
        self._with_try_catch = True
        return self

    def _invoke(self, value):
        if not self._with_try_catch:
            return (value(*self.args, **self.kwargs), False)
        else:
            try:
                return (value(*self.args, **self.kwargs), False)
            except:
                return (None,True)



def maybe(value, *args, default = None):

    for action in args:

        if value is None:
            break

        elif callable(action):
            value = action(value)

        elif isinstance(action,str):
            try:
                value = getattr(value,action)
            except:
                value = None

        elif isinstance(action,mb_call):
            inv_result = action._invoke(value)
            value = inv_result[0]

        elif isinstance(action,list):

            if len(action)<1 or len(action)>3:
                raise ValueError("Only 1-, 2- and 3-dimentional indexing is supported") #pragma: no cover
            try:
                if len(action)==1:
                    value = value[action[0]]
                elif len(action)==2:
                    value = value[action[0],action[1]] #No star-expression for indexing,
                elif len(action)==3:
                    value = value[action[0], action[1],action[2]]
                else:
                    pass
            except:
                value = None

    if value is None:
        return default

    return value

