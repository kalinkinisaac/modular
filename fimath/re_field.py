from fractions import Fraction
from .error import UnsupportedTypeError
from .types_support import TypesSupported
import decimal

def types_support(func):

    supported_types = {int, float}

    def wrapped(self, other):
        if type(other) in supported_types:
            other = ReField(a=other)
        return func(other)

    return wrapped

class ReField(object):
    # ReField consist numbers a + b*sqrt(3)
    def __init__(self, a=Fraction(0, 1), b=Fraction(0, 1)):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def approx(self, precision=16):
        decimal.getcontext().prec = precision
        return (decimal.Decimal(self.a.numerator)/decimal.Decimal(self.a.denominator) +
               decimal.Decimal(3).sqrt() * decimal.Decimal(self.b.numerator) / decimal.Decimal(self.b.denominator))

    def sqrt_approx(self, precision=16):
        decimal.getcontext().prec = precision
        return (decimal.Decimal(self.a.numerator) / decimal.Decimal(self.a.denominator) +
               decimal.Decimal(3).sqrt() * decimal.Decimal(self.b.numerator) / decimal.Decimal(self.b.denominator)).sqrt()

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
        return ReField(a=abs(self.a), b=abs(self.b))

    @types_support
    def __eq__(self, other):
        if type(other) == ReField:
            return self.a == other.a  and self.b == other.b
        else:
            raise UnsupportedTypeError(other)
    @types_support
    def __lt__(self, other):
        sign = lambda x: x and (1, -1)[x < 0]
        return sign(self.a - other.a) * (self.a - other.a) ** 2 < 3 * sign(other.b - self.b) * (other.b - self.b) ** 2

    @types_support
    def __le__(self, other):
        return self == other or self < other

    @types_support
    def __gt__(self, other):
        return not self <= other

    @types_support
    def __ge__(self, other):
        return not self < other

    @types_support
    def __neg__(self):
        return ReField(a=-self.a, b=-self.b)

    @types_support
    def __add__(self, other):
        return ReField(
            a=self.a + other.a,
            b=self.b + other.b
        )

    def __float__(self):
        return float(self.approx())

    @types_support
    def __sub__(self, other):
        return self + (-other)

    @types_support
    def __mul__(self, other):
        if type(other) == ReField:
            return ReField(
                a=self.a * other.a + 3 * self.b * other.b,
                b=self.a * other.b + self.b * other.a
            )

        elif type(other) == int or type(other) == float:
            return self * ReField(a=other)

        else:
            raise UnsupportedTypeError(other)

    def __rmul__(self, other):
        return self * other

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

    @types_support
    def __truediv__(self, other):
        return self * other.inv()

    def __repr__(self):
        return f'({self.a}+{self.b}s3)'

    @classmethod
    def one(cls):
        return ReField(a=1, b=0)