from .field import Field

# Totally Field/ReField geodesic class
class Geodesic(object):

    def __init__(self, begin, end):
        if type(begin) == int or type(begin) == float:
            self.begin = Field(a=begin)
        else:
            self.begin = begin

        if type(end) == int or type(end) == float:
            self.end = Field(a=end)
        else:
            self.end = end

        if self.begin.real <= self.end.real:
            self._left, self._right = self.begin, self.end
        else:
            self._left, self._right = self.end, self.begin

        if self.is_vertical():
            self.center = Field.inf()
            self.radius = Field.inf()
        else:
            self.center = 0.5 * (self.begin.sq_abs() - self.end.sq_abs()) / (self.begin - self.end).real
            self.sq_radius = (self.begin - self.center).sq_abs()

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def is_vertical(self):
        return self.begin.real == self.end.real or self.has_inf()

    def has_inf(self):
        return self.begin.is_inf or self.end.is_inf

    def x(self):
        if(self.begin.is_inf):
            return self.end.real
        else:
            return self.begin.real

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'<Geodesic from {self.begin} to {self.end}>'