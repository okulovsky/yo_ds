from yo_ds import *
from unittest import TestCase


def path(*args):
    folder = FileIO.find_root_folder('yo.root')
    return os.path.abspath(os.path.join(folder, 'tests', 'extensions', 'test_plots_extensions', *args))