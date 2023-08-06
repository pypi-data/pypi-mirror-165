import math
import numpy as np


class GaussianHill:
    def __init__(self, sigma, d, u=np.array([0.0, 0.0])):
        self._d = np.array([[d[0, 0], d[0, 1]], [d[1, 0], d[1, 1]]], dtype=np.float64)
        self._fai_0 = 2 * math.pi * sigma**2
        self._initial_param = -1 / (2 * sigma**2)
        self._sigma = sigma
        self._u = np.array([u[0], u[1]], dtype=np.float64)

    def calc_initial_condition(self, cell_coordinate):
        return math.exp(self._initial_param*np.linalg.norm(cell_coordinate)**2)

    def calc(self, coordinate, time):
        coordinate = np.array([coordinate[0], coordinate[1]], dtype=np.float64)

        sigma_t = self._sigma**2 * np.eye(2) + 2 * time * self._d
        param_0 = self._fai_0 / (2 * math.pi * math.sqrt(abs(np.linalg.det(sigma_t))))

        vector_0 = coordinate - self._u * time
        vector_1 = vector_0.reshape([2, 1])

        matrix_0 = np.multiply(vector_0, vector_1)

        return param_0*math.exp(-0.5*np.vdot(np.linalg.inv(sigma_t), matrix_0))
