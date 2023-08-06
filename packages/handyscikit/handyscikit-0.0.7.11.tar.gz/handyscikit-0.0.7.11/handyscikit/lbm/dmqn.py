import numpy as np


class AbstractDmQn:
    def __init__(self):
        self.m = None  # Dimension of DmQn.
        self.n = None  # Discrete velocity number of DmQn.
        self.cs = None  # Sound speed.
        self.omega = None  # Omega.
        self.e = None  # Velocity.


class D2Q5(AbstractDmQn):
    def __init__(self, float_dtype=np.float64):
        AbstractDmQn.__init__(self)

        self.m = 2
        self.n = 5
        self.cs = 3
        self.omega = np.array([1/3, 1/6, 1/6, 1/6, 1/6], dtype=float_dtype)
        self.e = np.array([[0, 0, 0],
                           [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]], dtype=float_dtype)


class D2Q9(AbstractDmQn):
    def __init__(self, float_dtype=np.float64):
        AbstractDmQn.__init__(self)

        self.m = 2
        self.n = 9
        self.cs = 3
        self.omega = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36], dtype=float_dtype)
        self.e = np.array([[0, 0, 0],
                           [1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0],
                           [1, 1, 0], [-1, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype=float_dtype)


class D3Q7(AbstractDmQn):
    def __init__(self, float_dtype=np.float64):
        AbstractDmQn.__init__(self)

        self.m = 3
        self.n = 7
        self.cs = 4
        self.omega = np.array([1/4, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8], dtype=float_dtype)
        self.e = np.array([[0, 0, 0],
                           [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=float_dtype)


class D3Q15(AbstractDmQn):
    def __init__(self, float_dtype=np.float64):
        AbstractDmQn.__init__(self)

        self.m = 3
        self.n = 15
        self.cs = 3
        self.omega = np.array([2/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9,
                               1/72, 1/72, 1/72, 1/72, 1/72, 1/72, 1/72, 1/72], dtype=float_dtype)
        self.e = np.array([[0, 0, 0],
                           [1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1],
                           [1, 1, 1], [1, 1, -1], [1, -1, -1], [1, -1, 1], [-1, 1, -1], [-1, 1, 1],
                           [-1, -1, 1], [-1, -1, -1]], dtype=float_dtype)


if __name__ == "__main__":
    dmqn = D2Q5()
    print(dmqn.e)