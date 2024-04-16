import unittest
import sys
sys.path.append('../')
from src.MagneticCore import MagneticCore
from src.CoilT import CoilT
import numpy as np

class TestMagneticCore(unittest.TestCase):
    def setUp(self):
        self.coils = [CoilT(1, 2, 10, 100), CoilT(1, 2, 10, 100), CoilT(1, 2, 10, 100)]
        self.magnetic_core = MagneticCore(self.coils)

    def test_initialization(self):
        self.assertEqual(len(self.magnetic_core.coils), 3)

    def test_calculate_current_of_target_force(self):
        v_m = [1, 0, 1]
        v_force = [10, 0, 0]
        calculated_currents = self.magnetic_core.calculate_current_of_target_force(v_m, v_force)
        expected_currents = [-1500527.193595177, 0, 0]

        np.testing.assert_array_almost_equal(calculated_currents, expected_currents)

    def test_calculate_current_of_target_torque(self):
        v_m = [1, 0, 1]
        v_torque = [2, 0, -2]
        expected_currents = [0, -450158.15807855304, 0]
        calculated_currents = self.magnetic_core.calculate_current_of_target_torque(v_m, v_torque)
        np.testing.assert_array_almost_equal(calculated_currents, expected_currents)
    def test_magnetic_torque(self):
        v_m = [1, 0, 1]
        i = [0, -450158.15807855304, 0]
        torque = self.magnetic_core.magnetic_torque(v_m, i)
        expected_torque = [2, 0, -2]
        np.testing.assert_array_almost_equal(torque, expected_torque)

    def test_magnetic_force(self):
        v_m = [1, 0, 1]
        i = [-1500527.193595177, 0, 0]
        force = self.magnetic_core.magnetic_force(v_m, i)
        expected_force = [10, 0, 0]
        np.testing.assert_array_almost_equal(force, expected_force)

    def test_magnetic_field_helmholtz(self):
        coil = self.coils[0]
        b = self.magnetic_core.magnetic_field_helmholtz(coil, 10)
        expected_b = 4.4428829381583664e-05
        self.assertAlmostEqual(b, expected_b)

    def test_derivatives_of_magnetic_field_maxwell_at_center(self):
        coil = self.coils[0]
        db = self.magnetic_core.derivatives_of_magnetic_field_maxwell_at_center(coil, 10)
        expected_db = -6.664324407237549e-05
        self.assertAlmostEqual(db, expected_db)

if __name__ == '__main__':
    unittest.main()
