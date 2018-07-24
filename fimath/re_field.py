from fractions import Fraction
from .error import UnsupportedTypeError

import decimal

class ReField(object):
    # ReField consist numbers a + b*sqrt(3)
    def __init__(self, a=Fraction(0, 1), b=Fraction(0, 1)):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def approx(self, precision=16):
        decimal.getcontext().prec = precision
        return decimal.Decimal(self.a.numerator)/decimal.Decimal(self.a.denominator) + \
               decimal.Decimal(3).sqrt() * decimal.Decimal(self.b.numerator) / decimal.Decimal(self.b.denominator)

    def inv(s):
        x = s.a ** 2 + 3 * s.b ** 2
        y = 2 * (s.a * s.b)
        den = x ** 2 - 3 * y ** 2

        if den == 0:
            raise ZeroDivisionError()

        a = x * s.a - 3 * y * s.b
        b = x * s.b - y * s.a

        return ReField(
            a=Fraction(a, den),
            b=Fraction(b, den)
        )

    def __abs__(self):
        return abs(float(self))

    def __eq__(self, other):
        return self.a == other.a  and self.b == other.b

    def __lt__(self, other):
        sign = lambda x: x and (1, -1)[x < 0]
        return sign(self.a - other.a) * (self.a - other.a) ** 2 < 3 * sign(other.b - self.b) * (other.b - self.b) ** 2

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __neg__(self):
        return ReField(a=-self.a, b=-self.b)

    def __add__(self, other):
        return ReField(
            a=self.a + other.a,
            b=self.b + other.b
        )
    def __float__(self):
        return float(self.approx())

    def __sub__(self, other):
        return self + (-self)

    def __mul__(self, other):
        if type(other) == ReField:
            return ReField(
                a=self.a * other.a + 3 * self.b * other.b,
                b=self.a * other.b + self.b * other.a
            )
        else:
            pass

    def __pow__(self, power, modulo=None):
        if type(power) == int:
            if power == 0:
                return ReField.one()

            result = ReField.one()
            for _ in range(power):
                result = result * self

            if power > 0:
                return result
            else:
                return result.inv()

        else:
            UnsupportedTypeError(power)

    def __truediv__(self, other):
        return self * other.inv()

    def __repr__(self):
        return f'({self.a}+{self.b}s3)'

    @classmethod
    def one(cls):
        return ReField(a=1, b=0)