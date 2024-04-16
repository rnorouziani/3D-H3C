import json
import numpy as np
from src.CoilT import CoilT


class InputFormat:

    def load_coils(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            coils = [None, None, None]
            coils[0] = self.create_coil_from_data(data['coil_x'])
            coils[1] = self.create_coil_from_data(data['coil_y'])
            coils[2] = self.create_coil_from_data(data['coil_z'])
            return coils
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} could not be found.")
        except KeyError as e:
            raise ValueError(f"The file format is incorrect. Missing key: {e}")
        except json.JSONDecodeError:
            raise ValueError(f"The file at {file_path} is not a valid JSON file.")

    def create_coil_from_data(self, coil_data):
        return CoilT(coil_data['r'], coil_data['l'], coil_data['n'], coil_data['max_i'])

    def load_params(self):
        try:
            magnetic_moment_input = input("Enter the magnetic moment vector (3 values separated by space): ")
            magnetic_moment_vector = [float(x) for x in magnetic_moment_input.split()]

            if len(magnetic_moment_vector) != 3:
                raise ValueError("Error: Exactly 3 values must enter for the magnetic moment vector.")

            target_torque_input = input("Enter the target magnetic torque (3 values separated by space): ")
            target_magnetic_torque = [float(x) for x in target_torque_input.split()]

            if len(target_magnetic_torque) != 3:
                raise ValueError("Error: Exactly 3 values must enter for the target magnetic torque.")

            target_force_input = input("Enter the target magnetic force (3 values separated by space): ")
            target_magnetic_force = [float(x) for x in target_force_input.split()]

            if len(target_magnetic_force) != 3:
                raise ValueError("Error: Please enter exactly 3 values for the target magnetic force.")
            if not self.is_input_valid(magnetic_moment_vector, target_magnetic_torque, target_magnetic_force):
                raise ValueError("Error: Regarding the magnetic moment, the target magnetic torque or force is not "
                                 "achievable!")
        except ValueError as e:
            print(e)
            raise

        return {
            "magnetic_moment_vector": magnetic_moment_vector,
            "target_magnetic_torque": target_magnetic_torque,
            "target_magnetic_force": target_magnetic_force
        }

    def is_input_valid(self, m, t, f):
        for i in range(0, 3):
            if m[i] == 0 and f[i] != 0:
                return False
        v_m = np.array(m)
        v_t = np.array(t)
        if not np.dot(v_m, v_t) == 0:
            return False
        return True
