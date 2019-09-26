from yo_fluq_ds import *
from unittest import TestCase
import os
import pandas as pd
import numpy as np


def path(*args):
    folder = FileIO.find_root_folder('yo.root')
    dir = os.path.join(folder, 'yo_fluq_ds__tests', *args)
    return dir