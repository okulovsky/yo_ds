from yo_fluq_ds import *
from unittest import TestCase

class BackwardsTest(TestCase):
    def test_simple(self):
        self.assertEqual(
            3,
            Query.args(1,2,3).select(lambda z: z*3).min()
        )