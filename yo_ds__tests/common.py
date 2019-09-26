from  unittest import TestCase
import os
from yo_ds import *


def path(*args):
    folder = FileIO.find_root_folder('yo.root')
    temp = os.path.join(folder, 'yo_ds__tests', *args)
    os.makedirs(os.path.dirname(temp), exist_ok=True)
    return temp

