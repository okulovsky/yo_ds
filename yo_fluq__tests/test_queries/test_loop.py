from yo_fluq import *
from unittest import TestCase

class TestLoop(TestCase):
    def test_loop_inc_endless(self):
        self.assertEqual(
            [1,3,5,7,9],
            Query.loop(1,2).take_while(lambda z: z<10).to_list()
        )

    def test_loop_dec_endless(self):
        self.assertEqual(
            [1,-1,-3],
            Query.loop(1,-2).take_while(lambda z: z>-5).to_list()
        )

    def test_loop_inc_notequal(self):
        self.assertEqual(
            [1,4,7],
            Query.loop(1,3,10).to_list()
        )

    def test_loop_inc_equal(self):
        self.assertEqual(
            [1,4,7,10],
            Query.loop(1,3,10,LoopEndType.Equal).to_list()
        )

    def test_loop_inc_force(self):
        self.assertEqual(
            [1,4,7,9],
            Query.loop(1,3,9,LoopEndType.Force).to_list()
        )


    def test_loop_dec_notequal(self):
        self.assertEqual(
            [1,-2,-5],
            Query.loop(1,-3,-6).to_list()
        )

    def test_loop_dec_equal(self):
        self.assertEqual(
            [1,-2,-5, -8],
            Query.loop(1,-3,-8,LoopEndType.Equal).to_list()
        )

    def test_loop_dec_force(self):
        self.assertEqual(
            [1,-2, -5, -7],
            Query.loop(1,-3,-7,LoopEndType.Force).to_list()
        )

    def test_loop_inc_empty(self):
        self.assertEqual(
            [],
            Query.loop(1,1,1).to_list()
        )

    def test_loop_inc_emptyend(self):
        self.assertEqual(
            [1],
            Query.loop(1, 1, 1, LoopEndType.Equal).to_list()
        )

    def test_loop_inc_emptyendforce(self):
        self.assertEqual(
            [1],
            Query.loop(1, 1, 1, LoopEndType.Force).to_list()
        )

    def test_loop_dec_empty(self):
        self.assertEqual(
            [],
            Query.loop(1,-1,1).to_list()
        )

    def test_loop_dec_emptyend(self):
        self.assertEqual(
            [1],
            Query.loop(1, -1, 1, LoopEndType.Equal).to_list()
        )

    def test_loop_dec_emptyendforce(self):
        self.assertEqual(
            [1],
            Query.loop(1, -1, 1, LoopEndType.Force).to_list()
        )

    def test_loop_inc_contradictory_raise(self):
        self.assertRaises(ValueError,lambda: Query.loop(1,-1,10).to_list())

    def test_loop_dec_contradictory_raise(self):
        self.assertRaises(ValueError,lambda: Query.loop(1,1,-10).to_list())


