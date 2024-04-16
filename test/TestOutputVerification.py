import unittest
import sys
sys.path.append('../')
from unittest.mock import patch
import numpy as np
from src.OutputVerification import OutputVerification
from src.CoilT import CoilT

class TestOutputVerification(unittest.TestCase):
    def setUp(self):
        self.coils = [CoilT(1, 2, 10, 100), CoilT(1, 2, 10, 100), CoilT(1, 2, 10, 100)]
        self.v_m = [2.0, 3.0, 5.0]
        self.v_f = [1.0, 1.0, 2.0]
        self.v_t = [1.0, 1.0, -1.0]
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

    @patch('src.MagneticCore.MagneticCore.magnetic_force', return_value=np.array([1,1,2]))
    @patch('src.MagneticCore.MagneticCore.magnetic_torque', return_value=np.array([1,1,-1]))
    def test_calculate_similarity_perfect_match(self, mock_force, mock_torque):
        similarity = self.output_verifier.calculate_simularity()
        for sim, expected in zip(similarity, [1.0, 1.0]):
            self.assertAlmostEqual(sim, expected, places=4)

    @patch('src.MagneticCore.MagneticCore.magnetic_force', return_value=np.array([-1, -1, -2]))
    @patch('src.MagneticCore.MagneticCore.magnetic_torque', return_value=np.array([-1, -1, 1]))
    def test_calculate_similarity_opposite_direction(self, mock_force, mock_torque):
        similarity = self.output_verifier.calculate_simularity()
        for sim, expected in zip(similarity, [-1.0, -1.0]):
            self.assertAlmostEqual(sim, expected, places=4)

    @patch('src.MagneticCore.MagneticCore.magnetic_force', return_value=np.array([0, 0, 0]))
    @patch('src.MagneticCore.MagneticCore.magnetic_torque', return_value=np.array([0, 0, 0]))
    def test_calculate_similarity_zero_vectors(self, mock_force, mock_torque):
        similarity = self.output_verifier.calculate_simularity()
        self.assertEqual(similarity, [-1.0, -1.0])
if __name__ == '__main__':
    unittest.main(verbosity=2)
