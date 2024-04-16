from typing import List
from src.CoilT import CoilT
import math
import numpy as np


class MagneticCore:
    def __init__(self, coils: List[CoilT]):
        self.coils = coils
        self.mu_0 = 4 * math.pi * 10 ** (-7)

    def calculate_current_of_target_force(self, v_m, v_force):
        x = 0
        y = 1
        z = 2
        i = [0, 0, 0]
        i[x] = self.calculate_c(x, v_m[x]) * v_force[x]
        i[y] = self.calculate_c(y, v_m[y]) * v_force[y]
        i[z] = self.calculate_c(z, v_m[z]) * v_force[z]
        return i

    def calculate_current_of_target_torque(self, v_m, v_torque):
        x = 0
        y = 1
        z = 2
        a = [self.calculate_a(x), self.calculate_a(y), self.calculate_a(z)]
        i = [0, 0, 0]
        m = np.array(v_m)
        i[x] = (v_torque[y] * v_m[z] - v_torque[z] * v_m[y]) / (np.dot(m, m) * a[x])
        i[y] = (v_torque[z] * v_m[x] - v_torque[x] * v_m[z]) / (np.dot(m, m) * a[y])
        i[z] = (v_torque[x] * v_m[y] - v_torque[y] * v_m[x]) / (np.dot(m, m) * a[z])
        return i

    def calculate_a(self, index):
        c = self.coils[index]
        a = (self.mu_0 * c.n * c.r ** 2) / (c.l ** 2 / 4 + c.r ** 2) ** (3 / 2)
        return a

    def calculate_c(self, index, m):
        c = self.coils[index]
        if (m == 0):
            return 0
        b = -2 * (c.l ** 2 / 4 + c.r ** 2) ** (5 / 2) / (3 * self.mu_0 * c.n * c.r ** 2 * c.l * m)
        return b

    def magnetic_torque(self, v_m, i):
        b = np.empty(3)
        for j in range(len(self.coils)):
            b[j] = self.magnetic_field_helmholtz(self.coils[j], i[j])
        m = np.array(v_m)
        t = np.cross(m, b)

        return t.tolist()

    def magnetic_force(self, v_m, i):
        f = [0, 0, 0]
        for j in range(len(self.coils)):
            f[j] = v_m[j] * self.derivatives_of_magnetic_field_maxwell_at_center(self.coils[j], i[j])
        return f

    def magnetic_field_helmholtz(self, c, i):
        b = (self.mu_0 * c.n * i * c.r ** 2) / ((c.l / 2 + c.r ** 2) ** (3 / 2))
        return b

    def derivatives_of_magnetic_field_maxwell_at_center(self, c, i):
        db = (-3 * self.mu_0 * c.n * i * c.r ** 2 * c.l) / (2 * (c.l ** 2 / 4 + c.r ** 2) ** (5 / 2))
        return db
