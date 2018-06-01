import numpy as np
class Geodesic(object):
    DELTA = 1e-14
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.center = 0
        self.radius = 0
        self.theta1 = 0
        self.theta2 = 0

        self.set_parameters()

    def set_parameters(self):
        if self.is_vertical():
            self.center = np.inf
            self.radius = np.inf
        else:
            self.center = 0.5*(np.abs(self.a)**2 - np.abs(self.b)**2)/(np.real(self.a) - np.real(self.b))
            self.radius = np.abs(self.a - self.center)
            self.theta1 = np.angle(self.a - self.center, deg=True)
            self.theta2 = np.angle(self.b - self.center, deg=True)

            self.theta1, self.theta2 = min(self.theta1, self.theta2), max(self.theta1, self.theta2)

    def is_vertical(self):
        return (np.abs(np.real(self.a - self.b)) <= Geodesic.DELTA) or self.has_inf()

    def y_min(self):
        return min(np.imag(self.a), np.imag(self.b))

    def has_inf(self):
        return (np.imag(self.a) == np.inf) or (np.imag(self.b) == np.inf)

    def y_max(self):
        return max(np.imag(self.a), np.imag(self.b))

    def x(self):
        if(np.isinf(self.a)):
            return np.real(self.b)
        else:
            return np.real(self.a)

    def __repr__(self):
        return "Geodesic from: {} to: {}.\n" \
               "Center: {}, Radius: {}, Theta1: {}, Theta2: {}".format(self.a,
                                                                      self.b,
                                                                      self.center,
                                                                      self.radius,
                                                                      self.theta1,
                                                                      self.theta2)