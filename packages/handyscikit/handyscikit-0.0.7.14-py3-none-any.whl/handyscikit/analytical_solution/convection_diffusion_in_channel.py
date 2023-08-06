import cmath as cm
import numpy as np

"""
Analytical solution of 3.1_convectin_diffusion_in_the_channel.
* It seems that change size (not width=1 and height=1) will leads to analytical solution incorrect.
"""
class ConvectionDiffusionInChannel:
    def __init__(self, width, height, d, u):
        """
        Initialize analytical solution.
        :param width: float | Width of solving field.
        :param height: float | Height of solving field.
        :param d: 2D np.ndarray | Diffusion coefficient.
        :param u: float | Horizontal velocity.
        """
        self.__height = height

        self.__k = 2 * np.pi / width
        self.__lambda = cm.sqrt(complex((self.__k**2) * d[0] / d[1], self.__k * u / d[1]))
        self.__c1 = (1 - cm.exp(self.__lambda)) / (cm.exp(-1 * self.__lambda) - cm.exp(self.__lambda))
        self.__c2 = (cm.exp(-1 * self.__lambda) - 1) / (cm.exp(-1 * self.__lambda) - cm.exp(self.__lambda))

    def calc(self, coordinate):
        """
        Give coordinate and calculate the solution.
        :param x: float | x-coordinate.
        :param y: float | y-coordinate.
        :return: soluiton value.
        """

        temp = cm.exp(complex(0, self.__k*coordinate[0]))
        temp_1 = self.__lambda*coordinate[1]/self.__height
        return (temp*(self.__c1*cm.exp(-1*temp_1) + self.__c2*cm.exp(temp_1))).real