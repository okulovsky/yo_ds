from ..._common import *

def with_indices(en):
    for index,item in enumerate(en):
        yield ItemWithIndex(index,item)


def foreach(en, action):
    for element in en:
        if action is not None:
            action(element)

def foreach_and_continue(en,action):
    for element in en:
        action(element)
        yield element

def append(en,array):
    for e in en:
        yield e
    for e in array:
        yield e

def prepend(en, array):
    for e in array:
        yield e
    for e in en:
        yield e


