import math

class Theis:
    def __init__(self, T=None, S=None, H=None, Q=None):
        """
        Set basic parameters.
        * Give the reference value.
        :param T: Coefficient of conductivity. (1) | float. | 4e-13.
        :param S: Coefficient of storage. (1) | float. | 1e-6.
        :param H: Initial head. (m) | float. | 2000.
        :param Q: Extract flow rate. (m^3/h) | float. | 36.
        """
        self.T = T
        self.S = S
        self.H = H
        self.Q = Q
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

    def calculate(self, r, t):
        """

        :param r: unit (m)
        :param t: unit (s)
        :return:
        """
        u = r**2*self.S/(4*self.T*t)
        return self.H - self.Q*self.__series_num(u)/(4*3.1415926*self.T)

    def set_T(self, K, rho, g, mu, thick):
        """
        Calculate T by other parameters.
        :param K: Permeability.
        :param rho: Density of water.
        :param g: Gravity.
        :param mu: Viscoust.
        :param thick: Thickness.
        :return: None
        """
        self.T = K*rho*g*thick/mu

