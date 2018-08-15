from .field import Field
from .re_field import ReField
from .bases import BaseGeodesic

# Totally Field geodesic class
class Geodesic(BaseGeodesic):

    __slots__ = ('_begin', '_end', '_left', '_right', '_top', '_bot', '_is_vertical', '_vertical_x', '_has_inf',
                 '_center', '_sq_radius')

    def __new__(cls, begin, end):

        self = super(Geodesic, cls).__new__(cls)
        self._begin = Field(begin)
        self._end = Field(end)
        self._is_vertical = False
        self._has_inf = False

        if self._begin == self._end:
            raise ValueError('geodesic begin can not be equal to end')

        if self._begin.is_inf:
            self._is_vertical = True
            self._has_inf = True
            self._vertical_x = self._end.real

            self._left = self._end
            self._right = self._begin
            self._top = self._begin
            self._bot = self._end


        elif self._end.is_inf:
            self._is_vertical = True
            self._has_inf = True
            self._vertical_x = self._begin.real

            self._left = self._begin
            self._right = self._end
            self._top = self._end
            self._bot = self._begin

        else:
            if self._begin.real == self._end.real:
                self._is_vertical = True
                self._vertical_x = self._begin.real

            if self._begin.real < self._end.real:
                self._left = self._begin
                self._right = self._end
            else:
                self._left = self._end
                self._right = self._begin

            if self._begin.imag < self._end.imag:
                self._top = self._end
                self._bot = self._begin
            else:
                self._top = self._begin
                self._bot = self._end

        if self._bot.imag < 0:
            raise ValueError('geodesic should not have point below real axis')

        if not self._is_vertical:
            self._center = ReField(0.5) * (self._begin.sq_abs() - self._end.sq_abs()) / (self._begin - self._end).real
            self._sq_radius = (self._begin - self._center).sq_abs()

        return self

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def top(self):
        return self._top

    @property
    def bot(self):
        return self._bot

    @property
    def is_vertical(self):
        return self._is_vertical

    @property
    def has_inf(self):
        return self._has_inf

    @property
    def vertical_x(self):
        if not self._is_vertical:
            raise NotImplementedError('geodesic is not vertical')

        return self._vertical_x

    @property
    def center(self):
        if self._is_vertical:
            raise NotImplementedError('geodesic is vertical')

        return self._center

    @property
    def sq_radius(self):
        if self._is_vertical:
            raise NotImplementedError('geodesic is vertical')

        return self._sq_radius

    def __repr__(self):
        return f'{self.__class__.__name__}(from: {self._begin} to: {self._end})'

    def __str__(self):
        return f'Geodesic from {self.begin} to {self.end}>'

    def __hash__(self):
        return hash(repr(self))


    def __eq__(self, other):
        if type(other) == Geodesic:
            return self.begin == other.begin and self.end == other.end
        else:
            return NotImplemented



def reversed(geo : Geodesic):
    return Geodesic(geo.end, geo.begin)

def unoriented_eq(l : Geodesic, r : Geodesic):
    return l == r or l == reversed(r)

__all__ = ['Geodesic', 'reversed', 'unoriented_eq']