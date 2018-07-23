from mmath import Field
from math import degrees
from cmath import phase

class Geodesic(object):

    DELTA = 1e-14
    def __init__(self, a : Field, b : Field):
        self.a = a
        self.b = b
        self.center = 0
        self.radius = 0
        self.theta1 = 0
        self.theta2 = 0

        self.set_parameters()

    def set_parameters(self):
        if self.is_vertical():
            self.center = Field.inf()
            self.radius = Field.inf()
        else:
            self.center = 0.5*(abs(complex(self.a))**2 - abs(complex(self.b))**2)/complex(self.a - self.b).real
            self.radius = abs(complex(self.a) - self.center)
            self.theta1 = degrees(phase(complex(self.a) - self.center))
            self.theta2 = degrees(phase(complex(self.b) - self.center))

            self.theta1, self.theta2 = min(self.theta1, self.theta2), max(self.theta1, self.theta2)

    def is_vertical(self):
        return (abs(complex(self.a - self.b).real) <= Geodesic.DELTA) or self.has_inf()

    def y_min(self):
        if self.has_inf():
            if self.a.is_inf:
                return complex(self.b).imag
            else:
                return complex(self.a).imag
        else:
            return min(complex(self.a).imag, complex(self.b).imag)

    def has_inf(self):
        return self.a.is_inf or self.b.is_inf

    def y_max(self):
        return max(abs(complex(self.a).imag), abs(complex(self.b).imag))

    def x(self):
        if(self.a.is_inf):
            return complex(self.b).real
        else:
            return complex(self.a).real

    def __repr__(self):
        return "Geodesic from: {} to: {}.\n" \
               "Center: {}, Radius: {}, Theta1: {}, Theta2: {}".format(self.a,
                                                                      self.b,
                                                                      self.center,
                                                                      self.radius,
                                                                      self.theta1,
                                                                      self.theta2)