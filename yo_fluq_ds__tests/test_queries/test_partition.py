from yo_fluq_ds__tests.common import *

class ExtendedMethodsTests(TestCase):
    def test_count_partition(self):
        lsts = Query.args(1,2,3,4,5).feed(fluq.partition_by_count(2)).to_list()
        self.assertEqual(3,len(lsts))
        self.assertListEqual([1,2],lsts[0])
        self.assertListEqual([3,4],lsts[1])
        self.assertListEqual([5],lsts[2])

    def test_count_empty_partition(self):
        lsts = Query.args().feed(fluq.partition_by_count(2)).to_list()
        self.assertEqual(0,len(lsts))

    def test_selector_partition(self):
        lsts = (Query
                .args( ('a',1), ('a',2), ('b',3), ('c',4), ('c', 5))
                .feed(fluq.partition_by_selector(lambda z: z[0]))
                .select(lambda z: [x[1] for x in z])
                .to_list()
                )
        self.assertEqual(3,len(lsts))
        self.assertListEqual([1,2],lsts[0])
        self.assertListEqual([3], lsts[1])
        self.assertListEqual([4,5],lsts[2])