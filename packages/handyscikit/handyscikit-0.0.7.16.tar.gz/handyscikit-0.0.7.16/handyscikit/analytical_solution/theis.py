import math
import numpy as np

class Theis:
    def __init__(self, t=None, s=None, h=None, q=None):
        """
        Set basic parameters.
        * Give the reference value.
        :param t: Coefficient of conductivity. (1) | float. | 4e-13.
        :param s: Coefficient of storage. (1) | float. | 1e-6.
        :param h: Initial head. (m) | float. | 2000.
        :param q: Extract flow rate. (m^3/h) | float. | 36.
        """
        self.t = t
        self.s = s
        self.h = h
        self.q = q
        self.__a = [-0.57721566, 0.99999193, -0.24991055, 0.05519968, -0.00976004, 0.00107857]
        self.__b = [0.2677737343, 8.6347608925, 18.059016973, 8.5733287401]
        self.__c = [3.9584969228, 21.0996530827, 25.6329561486, 9.5733223454]

    def __series_num(self, u):
        if u<1:
            tmp = self.__a[0]+u*(self.__a[1]+u*(self.__a[2]+u*(self.__a[3]+u*(self.__a[4]+u*self.__a[5]))))
            return -1*math.log(u) + tmp
        else:
            tmp1 = 1/(u*(math.e**u))
            tmp2 = self.__b[0]+u*(self.__b[1]+u*(self.__b[2]+u*(self.__b[3]+u)))
            tmp3 = self.__c[0]+u*(self.__c[1]+u*(self.__c[2]+u*(self.__c[3]+u)))
            return tmp1*tmp2/tmp3

    def calc(self, coordinate, t):
        """
        :param coordinate: unit (m)
        :param t: unit (s)
        :return:
        """
        radius = np.linalg.norm(coordinate)
        u = radius**2*self.s/(4*self.t*t)
        return self.h - self.q*self.__series_num(u)/(4*3.1415926*self.t)

    def set_conductivity_by_permeability(self, k, rho, g, mu, thick):
        """
        Calculate T by other parameters.
        :param k: Permeability.
        :param rho: Density of water.
        :param g: Gravity.
        :param mu: Viscoust.
        :param thick: Thickness.
        :return: None
        """
        self.t = k*rho*g*thick/mu
