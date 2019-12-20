from unittest import TestCase
from yo_fluq import KeyValuePair

class MiscTestCase(TestCase):
    def test_kv_pair_repr(self):
        kvp = KeyValuePair((2,3),[dict(a=2)])
        self.assertEqual("{'key': (2, 3), 'value': [{'a': 2}]}", kvp.__repr__())
        self.assertEqual("{'key': (2, 3), 'value': [{'a': 2}]}", kvp.__str__())
