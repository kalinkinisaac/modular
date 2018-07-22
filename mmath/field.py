from fractions import Fraction
from .error import (UnsupportedTypeError, NanError)

class Field(object):

    # Field consist numbers a + b*sqrt(3) + c*i + d*i*sqrt(3)
    def __init__(self, a=Fraction(0, 1), b=Fraction(0, 1), c=Fraction(0, 1), d=Fraction(0, 1), is_inf=False):
        self.a = Fraction(a)
        self.b = Fraction(b)
        self.c = Fraction(c)
        self.d = Fraction(d)

        self._is_inf = is_inf

    # Inverse of number, self^-1
    def inv(s):
        if s.is_inf:
            return Field.zero()
        if s.is_zero:
            return Field.inf()

        x = s.a ** 2 + s.c ** 2 + 3 * (s.b ** 2 + s.d ** 2)
        y = 2 * (s.a * s.b + s.c * s.d)
        den = x ** 2 - 3 * y ** 2

        if den == 0:
            raise ZeroDivisionError()

        a = x * s.a - 3 * y * s.b
        b = x * s.b - y * s.a
        c = -x * s.c + 3 * y * s.d
        d = -x * s.d + y * s.c

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
        return not self.is_inf and not(self.a or self.b or self.c or self.d)

    def __neg__(self):
        return self * -1

    def __mul__(self, other):
        if type(other) == Field:
            if (self.is_inf and not other.is_zero) or (other.is_inf and not self.is_zero):
                return Field.inf()
            elif (self.is_inf and other.is_zero) or (other.is_inf and self.is_zero):
                raise NanError()
            else:
                return Field(
                    a=self.a * other.a + 3 * self.b * other.b - self.c * other.c - 3 * self.d * other.d,
                    b=self.a * other.b + self.b * other.a - self.c * other.d - self.d * other.c,
                    c=self.a * other.c + self.c * other.a + 3 * self.b * other.d + 3 * self.d * other.b,
                    d=self.a * other.d + self.d * other.a + self.b * other.c + self.c * other.b
                )

        if type(other) == int or type(other) == Fraction:
            if self.is_inf and other != 0:
                return Field.inf()
            elif self.is_inf and other == 0:
                raise NanError()
            return self * Field(a=other)

        raise UnsupportedTypeError(other)

    def __rmul__(self, other):
        if type(other) == Mat:
            return other.__mul__(self)

        if type(other) == Field:
            return other * self
        elif type(other) == int or type(other) == Fraction:
            return Field(a=other) * self
        else:
            raise UnsupportedTypeError(other)

    def __truediv__(self, other):
        if type(other) == Field:
            if self.is_inf and not other.is_inf:
                return Field.inf()
            elif self.is_inf and other.is_inf:
                raise NanError()
            else:
                return self * other.inv()
        elif type(other) == int or type(other) == Fraction:
            return self * Field(a=Fraction(1, other))
        else:
            raise UnsupportedTypeError(other)

    def __rtruediv__(self, other):
        if type(other) == Field:
            return other * self.inv()
        elif type(other) == int or type(other) == Fraction:
            return Field(a=other) / self
        else:
            raise UnsupportedTypeError(other)


    def __add__(self, other):
        if type(other) == Field:
            if self.is_inf or other.is_inf:
                return Field.inf()

            return Field(
                a=self.a + other.a,
                b=self.b + other.b,
                c=self.c + other.c,
                d=self.d + other.d
            )
        elif type(other) == int or type(other) == Fraction:
            return self + Field(a=other)
        else:
            raise UnsupportedTypeError(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __eq__(self, other):
        return (self.is_inf and other.is_inf) or \
               (self.a == other.a and
                self.b == other.b and
                self.c == other.c and
                self.d == other.d)

    def __str__(self):
        if self.is_inf:
            return 'inf'

        res = []

        if self.a:
            res.append(f'{self.a}')
        if self.b:
            res.append(f'{self.b}s3')
        if self.c:
            res.append(f'{self.c}j')
        if self.d:
            res.append(f'{self.d}js3')

        return '({})'.format('+'.join(res))

    def __repr__(self):
        if self.is_inf:
            return 'inf'
        else:
            return f'({self.a}+{self.b}s3+{self.c}j+{self.d}js3)'

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
