from fractions import Fraction
from .error import (UnsupportedTypeError, NanError)
from math import sqrt, degrees
from cmath import phase
from .re_field import ReField
from decimal import Decimal
from numbers import Rational
from .bases import BaseField

def re_field_support(func):
    def wrapped(obj, other):
        if type(other) == ReField:
            other = Field(a=other.a, b=other.b)
        return func(obj, other)
    return wrapped



class Field(BaseField):

    __slots__ = ('_real', '_imag')

    def __new__(cls, real=0, *, imag=None):

        self = super(Field, cls).__new__(cls)
        if imag is None:
            if isinstance(real, (int, Fraction)):
                self._real = ReField(real)
                self._imag = ReField()
                return self

            elif isinstance(real, BaseField):
                self._real = real.real
                self._imag = real.imag
                return self

            elif type(real) is int:
                self._real = ReField(real)
                self._imag = ReField()
                return self

            elif isinstance(real, (float, Decimal)):
                self._real = ReField(real)
                self._imag = ReField()
                return self

            else:
                raise TypeError('argument should be int, float, Fraction, BaseReField or BaseField instance')





    # Field consist numbers a + b*sqrt(3) + c*i + d*i*sqrt(3)
    def __init__(self, a=Fraction(0, 1), b=Fraction(0, 1), c=Fraction(0, 1), d=Fraction(0, 1), is_inf=False):
        self._a = Fraction(a)
        self._b = Fraction(b)
        self._c = Fraction(c)
        self._d = Fraction(d)

        self._is_inf = is_inf

    @classmethod
    def from_complex(cls, c : complex):
        return Field(a=c.real, c=c.imag)

    def abs(self):
        return abs(complex(self))

    def sq_abs(self):
        return self.real ** 2 + self.imag ** 2

    def __complex__(self):
        return self._a + sqrt(3) * self._b + 1j * (self._c + sqrt(3) * self._d)

    @property
    def real(self):
        return ReField(a=self._a, b=self._b)

    @property
    def imag(self):
        return ReField(a=self._c, b=self._d)

    def angle(self):
        return degrees(phase(compile(self)))

    # def approx(self, precision=16):
    #     decimal.getcontext().prec = precision
    #     return decimal.Decimal(self.a.numerator)/decimal.Decimal(self.a.denominator) + \
    #            decimal.Decimal(3).sqrt() * decimal.Decimal(self.b.numerator) / decimal.Decimal(self.b.denominator)

    # Inverse of number, self^-1
    def inv(s):
        if s.is_inf:
            return Field.zero()
        if s.is_zero:
            return Field.inf()

        x = s._a ** 2 + s._c ** 2 + 3 * (s._b ** 2 + s._d ** 2)
        y = 2 * (s._a * s._b + s._c * s._d)
        den = x ** 2 - 3 * y ** 2

        if den == 0:
            raise ZeroDivisionError()

        a = x * s._a - 3 * y * s._b
        b = x * s._b - y * s._a
        c = -x * s._c + 3 * y * s._d
        d = -x * s._d + y * s._c

        return Field(
            a=Fraction(a, den),
            b=Fraction(b, den),
            c=Fraction(c, den),
            d=Fraction(d, den)
        )

    @property
    def is_inf(self):
        return self._is_inf

    @property
    def is_zero(self):
        return not self.is_inf and not(self._a or self._b or self._c or self._d)

    def __neg__(self):
        return self * -1

    @re_field_support
    def __mul__(self, other):
        if type(other) == Field:
            if (self.is_inf and not other.is_zero) or (other.is_inf and not self.is_zero):
                return Field.inf()
            elif (self.is_inf and other.is_zero) or (other.is_inf and self.is_zero):
                raise NanError()
            else:
                return Field(
                    a=self._a * other.a + 3 * self._b * other.b - self._c * other.c - 3 * self._d * other.d,
                    b=self._a * other.b + self._b * other.a - self._c * other.d - self._d * other.c,
                    c=self._a * other.c + self._c * other.a + 3 * self._b * other.d + 3 * self._d * other.b,
                    d=self._a * other.d + self._d * other.a + self._b * other.c + self._c * other.b
                )

        if type(other) == int or type(other) == Fraction:
            if self.is_inf and other != 0:
                return Field.inf()
            elif self.is_inf and other == 0:
                raise NanError()
            return self * Field(a=other)

        return NotImplemented

    def __abs__(self):
        return sqrt(float(self.real) ** 2 + float(self.imag) ** 2)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        if type(power) == int:
            if power == 0:
                return Field.one()

            result = Field.one()
            for _ in range(power):
                result = result * self

            if power > 0:
                return result
            else:
                return result.inv()

        else:
            return NotImplemented

    @re_field_support
    def __truediv__(self, other):
        if type(other) == Field:
            if self.is_inf and not other.is_inf:
                return Field.inf()
            elif self.is_inf and other.is_inf:
                raise NanError()
            else:
                return self * other._inv()

        elif type(other) == int or type(other) == Fraction:
            return self * Field(a=Fraction(1, other))

        else:
            return NotImplemented

    @re_field_support
    def __rtruediv__(self, other):
        if type(other) == Field:
            return other * self.inv()

        elif type(other) == ReField:
            return Field(a=other.a, b=other.b) / self

        elif type(other) == int or type(other) == Fraction:
            return Field(a=other) / self

        else:
            return NotImplemented

    @re_field_support
    def __add__(self, other):
        if type(other) == Field:
            if self.is_inf or other.is_inf:
                return Field.inf()

            return Field(
                a=self._a + other.a,
                b=self._b + other.b,
                c=self._c + other.c,
                d=self._d + other.d
            )

        elif type(other) == int or type(other) == float or type(other) == Fraction:
            return self + Field(a=other)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    @re_field_support
    def __eq__(self, other):
        return (self.is_inf and other.is_inf) or \
               (self._a == other.a and
                self._b == other.b and
                self._c == other.c and
                self._d == other.d)

    def __hash__(self):
        return hash(repr(self))

    def __str__(self):
        if self.is_inf:
            return 'inf'

        if self.is_zero:
            return '0'

        res = []

        if self._a:
            res.append(f'{self._a}')
        if self._b:
            res.append(f'{self._b}s3')
        if self._c:
            res.append(f'{self._c}j')
        if self._d:
            res.append(f'{self._d}js3')

        return '({})'.format('+'.join(res))

    def __repr__(self):
        if self.is_inf:
            return 'inf'
        else:
            return f'({self._a}+{self._b}s3+{self._c}j+{self._d}js3)'

    @classmethod
    def sort_key(cls, fi):
        return [fi.imag.sign(), fi.imag.sign() * fi.imag / fi.real]

    # Constants
    @classmethod
    def zero(cls):
        return Field(a=0, b=0, c=0, d=0)

    @classmethod
    def one(cls):
        return Field(a=1, b=0, c=0, d=0)

    @classmethod
    def inf(cls):
        return Field(is_inf=True)
