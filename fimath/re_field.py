from fractions import Fraction
from .error import UnsupportedTypeError
from .types_support import TypesSupported
from decimal import Decimal, getcontext
from .bases import BaseReField
import operator
import numbers
import math

# TODO: remake with +-inf
def types_support(func):

    supported_types = {int, float}

    def wrapped(self, other):
        if type(other) in supported_types:
            other = ReField(a=other)
        return func(self, other)

    return wrapped

class ReField(BaseReField):

    __slots__ = ('_a', '_b')

    def __new__(cls, a=0, *, b=None):

        self = super(ReField, cls).__new__(cls)

        if b is None:

            if type(a) is int:
                self._a = Fraction(a)
                self._b = Fraction(0)
                return self

            elif type(a) is Fraction:
                self._a = a
                self._b = Fraction(0)
                return self

            elif isinstance(a, BaseReField):
                self._a = a.a
                self._b = a.b

            elif isinstance(a, (float, Decimal)):
                self._a = Fraction(a)
                self._b = Fraction(0)
                return self

            else:
                raise TypeError('argument should be int, float, Fraction or BaseReField instance')

        else:

            if type(a) is Fraction is type(b):
                self._a = a
                self._b = b
                return self

            elif isinstance(a, (int, float, Decimal)) and isinstance(b, (int, float, Decimal)):
                self._a = Fraction(a)
                self._b = Fraction(b)
                return self

            else:
                raise TypeError('both argument should be int, float or Fraction instances')

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def __repr__(self):
        return f'{self.__class__.__name__}({self.a}+{self.b}s3)'

    def __str__(self):
        return f'({self.a}+{self.b}s3)'

    def _operator_fallbacks(monomorphic_operator, fallback_operator):

        def forward(a, b):
            if isinstance(b, BaseReField):
                return monomorphic_operator(a, b)
            elif type(b) is int:
                return fallback_operator(a, ReField(b))
            elif type(b) is float:
                return fallback_operator(float(a), b)
            else:
                return NotImplemented

        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, BaseReField):
                # Includes ints.
                return monomorphic_operator(a, b)
            elif type(a) is float:
                return fallback_operator(a, float(b))
            else:
                return NotImplemented

        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse


    def _inv(s):
        x = s.a ** 2 + 3 * s.b ** 2
        y = 2 * (s.a * s.b)
        den = x ** 2 - 3 * y ** 2

        if den == 0:
            raise ZeroDivisionError

        a = x * s.a - 3 * y * s.b
        b = x * s.b - y * s.a

        return ReField(
            a=Fraction(a, den),
            b=Fraction(b, den)
        )

    def sign(self):

        if self > ReField.zero():
            return 1
        elif self < ReField.zero():
            return -1
        else:
            return 0

    def __abs__(self):
        return ReField(a=abs(self.a), b=abs(self.b))

    def _add(l, r):
        return ReField(a=l.a + r.a, b=l.b + r.b)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(l, r):
        return ReField(a=l.a - r.a, b=l.b - r.b)

    __sub__, __rsub = _operator_fallbacks(_sub, operator.sub)

    def _mul(l, r):
        return ReField(
            a=l.a * r.a + 3 * l.b * r.b,
            b=l.a * r.b + l.b * r.a
        )

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def __eq__(self, other):
        if type(other) == ReField:
            return self.a == other.a  and self.b == other.b
        elif isinstance(other, (int, float)):
            return self.a == other
        else:
            return NotImplemented

    def _richcmp(self, other, op):
        if isinstance(other, BaseReField):
            return op(math.copysign(1, self.a - other.a) * (self.a - other.a) ** 2,
                   3 * math.copysign(1, other.b - self.b) * (other.b - self.b) ** 2)
        if type(other) is int:
            return op(math.copysign(1, self.a - other) * (self.a - other) ** 2,
                      3 * math.copysign(1, -self.b) * (self.b) ** 2)
        elif isinstance(other, float):
            if math.isnan(other) or math.isinf(other):
                return op(0.0, other)
            else:
                return op(self, ReField(other))
        else:
            return NotImplemented


    def __lt__(l, r):
        return l._richcmp(r, operator.lt)

    def __le__(l, r):
        return l._richcmp(r, operator.le)

    def __gt__(l, r):
        return l._richcmp(r, operator.gt)

    def __ge__(l, r):
        return l._richcmp(r, operator.ge)

    def __neg__(self):
        return ReField(a=-self.a, b=-self.b)

    def __bool__(self):
        return self.a or self.b

    def __pow__(self, power, modulo=None):
        if type(power) is int:
            if power is 0:
                return ReField.one()

            result = ReField.one()
            for _ in range(power):
                result = result * self

            if power > 0:
                return result
            else:
                return result._inv()

        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return self * ReField(other)._inv()
        elif isinstance(other, BaseReField):
            return self * other._inv()
        else:
            return NotImplemented

    # This is disgusting. TODO: replace with better solution
    def __hash__(self):
        return hash(repr(self))

    def approx(self, precision=16):
        getcontext().prec = precision
        return (Decimal(self.a.numerator) / Decimal(self.a.denominator) +
               Decimal(3).sqrt() * Decimal(self.b.numerator) / Decimal(self.b.denominator))

    def sqrt_approx(self, precision=16):
        getcontext().prec = precision
        return (Decimal(self.a.numerator) / Decimal(self.a.denominator) +
               Decimal(3).sqrt() * Decimal(self.b.numerator) / Decimal(self.b.denominator)).sqrt()


    @classmethod
    def one(cls):
        return ReField(a=1, b=0)

    @classmethod
    def zero(cls):
        return ReField(a=0, b=0)