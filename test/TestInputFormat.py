import unittest
import sys
sys.path.append('../')
from unittest.mock import patch, mock_open
from src.InputFormat import InputFormat
from src.CoilT import CoilT
import json


class TestInputFormat(unittest.TestCase):
    def setUp(self):
        self.input_format = InputFormat()
        self.valid_json_data = '{"coil_x": {"r": 1, "n": 10, "l": 2, "max_i": 100}, "coil_y": {"r": 1, "n": 10, "l": 2, "max_i": 100}, "coil_z": {"r": 1, "n": 10, "l": 2, "max_i": 100}}'

    @patch('builtins.open', new_callable=mock_open, read_data='{"coil_x": {"r": 1, "n": 10, "l": 2, "max_i": 100}, "coil_y": {"r": 1, "n": 10, "l": 2, "max_i": 100}, "coil_z": {"r": 1, "n": 10, "l": 2, "max_i": 100}}')
    def test_load_coils_valid(self, mock_file):
        coils = self.input_format.load_coils('dummy_path.json')
        self.assertEqual(len(coils), 3)
        self.assertIsInstance(coils[0], CoilT)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_coils_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            self.input_format.load_coils('nonexistent_path.json')

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0))
    def test_load_coils_invalid_json(self, mock_json, mock_file):
        with self.assertRaises(ValueError):
            self.input_format.load_coils('dummy_path.json')

    def test_create_coil_from_data_valid(self):
        coil_data = {"r": 1, "n": 10, "l": 2, "max_i": 100}
        coil = self.input_format.create_coil_from_data(coil_data)
        self.assertIsInstance(coil, CoilT)
        self.assertEqual(coil.r, 1)
        self.assertEqual(coil.n, 10)
        self.assertEqual(coil.l, 2)
        self.assertEqual(coil.max_i, 100)

    @patch('builtins.input', side_effect=['1 2 4', '2 1 -1', '7 8 9'])
    def test_load_params_valid_input(self, mock_input):
        result = self.input_format.load_params()
        self.assertEqual(result['magnetic_moment_vector'], [1.0, 2.0, 4.0])
        self.assertEqual(result['target_magnetic_torque'], [2.0, 1.0, -1.0])
        self.assertEqual(result['target_magnetic_force'], [7.0, 8.0, 9.0])

    @patch('builtins.input', side_effect=['1 2', '4 5 6', '7 8 9'])
    def test_load_params_invalid_magnetic_moment(self, mock_input):
        with self.assertRaises(ValueError) as context:
            self.input_format.load_params()
        self.assertIn('Error: Exactly 3 values must enter for the magnetic moment vector', str(context.exception))

    @patch('builtins.input', side_effect=['1 2 3', '4 5', '7 8 9'])
    def test_load_params_invalid_magnetic_torque(self, mock_input):
        with self.assertRaises(ValueError) as context:
            self.input_format.load_params()
        self.assertIn('Error: Exactly 3 values must enter for the target magnetic torque', str(context.exception))

    @patch('builtins.input', side_effect=['1 2 3', '4 5 6', '7 8'])
    def test_load_params_invalid_magnetic_force(self, mock_input):
        with self.assertRaises(ValueError) as context:
            self.input_format.load_params()
        self.assertIn('Error: Please enter exactly 3 values for the target magnetic force', str(context.exception))

    @patch('builtins.input', side_effect=['1 0 0', '1 0 0', '1 0 0'])
    def test_load_params_invalid_combination(self, mock_input):
        with self.assertRaises(ValueError) as context:
            self.input_format.load_params()
            self.assertIn('Error: Regarding the magnetic moment, the target magnetic torque or force is not achievable', str(context.exception))


if __name__ == '__main__':
    unittest.main(verbosity=2)
