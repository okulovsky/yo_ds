from yo_ds import *
from unittest import TestCase
from IPython.display import HTML

class TestYoMisc(TestCase):
    def test_notebook_true(self):
        self.assertIsInstance(
            notebook_printable_version(True),
            HTML
        )

    def test_notebook_false(self):
        self.assertIsNone(
            notebook_printable_version(False)
        )

    def test_diff_set(self):
        s = diffset({1,2,3},{2,3,4})
        self.assertListEqual([3,3,1,1,2,False,False,False],list(s.values))
