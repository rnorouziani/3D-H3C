import numpy as np
from src.MagneticCore import MagneticCore


class OutputVerification:
    def __init__(self, coils, v_m, v_f, v_t, i_f, i_t):
        self.coils = coils
        self.v_m = v_m
        self.v_f = v_f
        self.v_t = v_t
        self.i_f = i_f
        self.i_t = i_t
        self.target_simularity = 0.98

    def is_currents_within_range(self):
        for i in range(len(self.coils)):
            if self.i_f[i] > self.coils[i].max_i or self.i_t[i] > self.coils[i].max_i:
                return False
        return True

    def is_accurate_enough(self):
        a = self.calculate_simularity()
        if a[0] >= self.target_simularity and a[1] >= self.target_simularity:
            return True
        return False

    def calculate_simularity(self):
        magneticCore = MagneticCore(self.coils)
        e_f = magneticCore.magnetic_force(self.v_m, self.i_f)
        e_t = magneticCore.magnetic_torque(self.v_m, self.i_t)

        n_f = np.linalg.norm(self.v_f)
        n_t = np.linalg.norm(self.v_t)
        n_e_f = np.linalg.norm(e_f)
        n_e_t = np.linalg.norm(e_t)

        if n_f == 0 or n_e_f == 0:
            if n_f == n_e_f:
                similarity_f = 1.0
            else:
                similarity_f = -1.0
        else :
            similarity_f = np.dot(self.v_f, e_f) / (n_f * n_e_f)
        if n_t == 0 or n_e_t == 0:
            if n_f == n_e_f:
                similarity_t = 1.0
            else:
                similarity_t = -1
        else:
            similarity_t = np.dot(self.v_t, e_t) / (n_t * n_e_t)

        return [similarity_f, similarity_t]
