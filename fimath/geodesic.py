from .field import Field
from math import degrees
from cmath import phase

class Geodesic(object):

    def __init__(self, a, b):
        if type(a) == int or type(a) == float:
            self.a = Field(a=a)
        else:
            self.a = a

        if type(b) == int or type(b) == float:
            self.b = Field(a=b)
        else:
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
            self.center = 0.5*(abs(self.a)**2 - abs(self.b)**2)/float((self.a - self.b).real)
            self.radius = abs(self.a - self.center)
            self.theta1 = degrees(phase(complex(self.a) - self.center))
            self.theta2 = degrees(phase(complex(self.b) - self.center))

            self.theta1, self.theta2 = min(self.theta1, self.theta2), max(self.theta1, self.theta2)

    def left(self):
        if self.a.real <= self.b.real:
            return self.a
        else:
            return self.b

    def right(self):
        if self.a.real <= self.b.real:
            return self.b
        else:
            return self.a

    def is_vertical(self):
        return self.a.real == self.b.real or self.has_inf()


    # def y_min(self):
    #     if self.has_inf():
    #         if self.a.is_inf:
    #             return float(self.b.imag)
    #         else:
    #             return float(self.a.imag)
    #     else:
    #         return min(float(self.a.imag), float(self.b.imag))

    def has_inf(self):
        return self.a.is_inf or self.b.is_inf

    # def y_max(self):
    #     return max(float(self.a.imag), float(self.b.imag))

    def x(self):
        if(self.a.is_inf):
            return self.b.real
        else:
            return self.a.real

    def __str__(self):
        return f'<Geodesic from: {self.a} to: {self.b}>\n' \
               f'Center: {self.center}, Radius: {self.radius}, Theta1: {self.theta1}, Theta2: {self.theta2}'
    def __repr__(self):
        return f'<Geodesic from {self.a} to {self.b}>'