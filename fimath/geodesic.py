from .field import Field

# Totally Field/ReField geodesic class
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

        if self.a.real <= self.b.real:
            self._left, self._right = self.a, self.b
        else:
            self._left, self._right = self.b, self.a

        if self.is_vertical():
            self.center = Field.inf()
            self.radius = Field.inf()
        else:
            self.center = 0.5 * (self.a.sq_abs() - self.b.sq_abs()) / (self.a - self.b).real
            self.sq_radius = (self.a - self.center).sq_abs()

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def is_vertical(self):
        return self.a.real == self.b.real or self.has_inf()

    def has_inf(self):
        return self.a.is_inf or self.b.is_inf

    def x(self):
        if(self.a.is_inf):
            return self.b.real
        else:
            return self.a.real

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'<Geodesic from {self.a} to {self.b}>'