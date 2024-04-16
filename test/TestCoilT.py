import unittest
import sys
sys.path.append('../')
from src.CoilT import CoilT

class TestCoilT(unittest.TestCase):
    def test_init_valid(self):
        coil = CoilT(r=1, l=2, n=10, max_i=100)
        self.assertEqual(coil.r, 1)
        self.assertEqual(coil.l, 2)
        self.assertEqual(coil.n, 10)
        self.assertEqual(coil.max_i, 100)

    def test_init_invalid_radius(self):
        with self.assertRaises(ValueError):
            CoilT(r=0, l=2, n=10, max_i=100)

    def test_init_invalid_distance(self):
        with self.assertRaises(ValueError):
            CoilT(r=1, l=0, n=10, max_i=100)

    def test_init_invalid_turns(self):
        with self.assertRaises(ValueError):
            CoilT(r=1, l=2, n=0, max_i=100)

    def test_init_invalid_current(self):
        with self.assertRaises(ValueError):
            CoilT(r=1, l=2, n=10, max_i=0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
