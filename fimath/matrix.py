from .bases import BaseMatrix
from .field import Field
from .re_field import ReField
from .geodesic import Geodesic
import operator

class Matrix(BaseMatrix):

    __slots__ = ('_a', '_b', '_c', '_d')

    def __new__(cls, a=1, b=0, c=0, d=1):
        self = super(Matrix, cls).__new__(cls)

        if isinstance(a, BaseMatrix):
            self._a = a.a
            self._b = a.b
            self._c = a.c
            self._d = a.d
            return self

        elif type(a) is int is type(b) is type(c) is type(d):
            self._a = a
            self._b = b
            self._c = c
            self._d = d
            return self
        else:
            raise TypeError('all arguments should be int type')

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    @property
    def d(self):
        return self._d

    def __repr__(s):
        return f'{s.__class__.__name__}([{s._a} {s._b}]\n\t[{s._c} {s._d}]'

    def __str__(s):
        return f'[{s._a} {s._b}]\n[{s._c} {s._d}]'


    def _operator_fallbacks(monomorphic_operator, fallback_operator):

        def forward(a, b):
            if isinstance(b, (BaseMatrix, int)):
                return monomorphic_operator(a, b)
            else:
                return NotImplemented

        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, BaseMatrix):
                return monomorphic_operator(a, b)
            else:
                return NotImplemented

        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse


    def moe(self, other):
        if type(other) == list:
            return [self._single_moe(f) for f in other]

        elif isinstance(other, (Field, ReField)):
            return self._single_moe(other)

        elif type(other) == Geodesic:
            return Geodesic(self._single_moe(other.begin), self._single_moe(other.end))
        else:
            return NotImplemented

    def dot(self, other):
        return self * other

    def det(self):
        return self._a * self._d - self._b * self._c

    def inv(self):
        if self._a * self._d - self._b * self._c == 0:
            raise ZeroDivisionError()

        return Matrix(self._d, -self._b, -self._c, self._a) * self.det()

    def _mul(l, r):
        if isinstance(r, BaseMatrix):
            return Matrix(
                l._a * r.a + l._b * r.c,
                l._a * r.b + l._b * r.d,
                l._c * r.a + l._d * r.c,
                l._c * r.b + l._d * r.d
            )
        elif type(r) == int:
            return Matrix(
                l._a * r,
                l._b * r,
                l._c * r,
                l._d * r
            )

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)


    def __mod__(self, other):
        if type(other) == int:
            return Matrix(
                self._a % other,
                self._b % other,
                self._c % other,
                self._d % other
            )
        else:
            return NotImplemented

    def __neg__(self):
        return Matrix(
            -self._a,
            -self._b,
            -self._c,
            -self._d
        )

    def __eq__(self, other):
        return self._a == other.a and self._b == other.b and self._c == other.c and self._d == other.d

    def __pow__(self, power : int, modulo=None):
        if type(power) == int:
            if power == 0:
                return Matrix()

            if power > 0:
                result = Matrix()
                for _ in range(power):
                    result = result * self
                return result

            if power < 0:
                result = Matrix()
                for _ in range(power):
                    result = result * self
                return result.inv()
        else:
            return NotImplemented

    def _single_moe(s, other):
        if type(other) == Field:
            if s._a * s._d == s._b * s._c:
                return Field(s._a) / s._c

            else:
                if s._c != 0:
                    if other.is_inf:
                        return s._a * Field(1) / s._c
                    elif other == -s._d * Field(1) / s._c:
                        return Field(is_inf=True)

                if other.is_inf:
                    return Field(is_inf=True)

            return (s._a * other + s._b) / (s._c * other + s._d)

        else:
            return NotImplemented

    # Constants
    @classmethod
    def identity(cls):
        return Matrix(a=1, b=0, c=0, d=1)
