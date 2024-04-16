import unittest
import sys
sys.path.append('../')
from src.OutputVerification import OutputVerification
from src.CoilT import CoilT

class TestOutputVerification(unittest.TestCase):
    def setUp(self):
        self.coils = [CoilT(1, 2, 10, 100), CoilT(1, 2, 10, 100), CoilT(1, 2, 10, 100)]
        self.v_m = [1, 1, 1]
        self.v_f = [1, 1, 1]
        self.v_t = [1, 1, 1]
        self.i_f = [50, 50, 50]
        self.i_t = [50, 50, 50]
        self.output_verifier = OutputVerification(self.coils, self.v_m, self.v_f, self.v_t, self.i_f, self.i_t)

    def test_is_currents_within_range_valid(self):
        self.assertTrue(self.output_verifier.is_currents_within_range())

    def test_is_currents_within_range_invalid(self):
        self.output_verifier.i_f[1] = 200
        self.assertFalse(self.output_verifier.is_currents_within_range())

    def test_is_accurate_enough_valid(self):
        self.output_verifier.calculate_simularity = lambda: (0.99, 0.99)
        self.assertTrue(self.output_verifier.is_accurate_enough())

    def test_is_accurate_enough_force_invalid(self):
        self.output_verifier.calculate_simularity = lambda: (0.5, 0.9)
        self.assertFalse(self.output_verifier.is_accurate_enough())

    def test_is_accurate_enough_torque_invalid(self):
        self.output_verifier.calculate_simularity = lambda: (0.9, 0.5)
        self.assertFalse(self.output_verifier.is_accurate_enough())

if __name__ == '__main__':
    unittest.main()
