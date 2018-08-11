from fractions import Fraction
from math import sqrt, degrees, isinf
import math
from cmath import phase
from .re_field import ReField
from decimal import Decimal
import numbers
from .bases import BaseField
import operator


class Field(BaseField):

    __slots__ = ('_real', '_imag', '_is_inf')

    def __new__(cls, real=0, imag=None, *, is_inf = False):

        self = super(Field, cls).__new__(cls)
        self._is_inf = False

        if is_inf:
            self._is_inf = True
            self._real = ReField()
            self._imag = ReField()
            return self

        elif imag is None:
            if isinstance(real, Field):
                return real

            elif isinstance(real, ReField):
                self._real = real
                self._imag = ReField()
                return self

            elif isinstance(real, (int, Fraction)):
                self._real = ReField(real)
                self._imag = ReField()
                return self

            elif isinstance(real, numbers.Complex):
                self._real = ReField(real.real)
                self._imag = ReField(real.imag)
                return self

            elif isinstance(real, (float, Decimal)):
                self._real = ReField(real)
                self._imag = ReField()
                return self

            else:
                raise TypeError('argument should be int, float, Fraction, BaseReField or BaseField instance')

        else:
            if type(real) is ReField is type(imag):
                self._real = real
                self._imag = imag
                return self
            elif isinstance(real, (int, float, numbers.Rational)) and isinstance(imag, (int, float, numbers.Rational)):
                self._real = ReField(real)
                self._imag = ReField(imag)
                return self

            else:
                raise TypeError('both argument should be int, float, Fraction or ReField instances')

    @property
    def real(self):
        if self.is_inf:
            raise NotImplementedError('Infinity has not real')

        return self._real

    @property
    def imag(self):
        if self.is_inf:
            raise NotImplementedError('Infinity has not imag')

        return self._imag

    def __repr__(self):
        if self.is_inf:
            return 'inf'
        else:
            #return f'({self.real}+1j{self.imag})'
            return repr(self.__complex__())

    def __str__(self):
        return self.__repr__()



    def abs(self):
        return abs(complex(self))

    def sq_abs(self):
        return self.real ** 2 + self.imag ** 2

    def __complex__(self):
        return complex(float(self.real), float(self.imag))

    def conjugate(self):
        return Field(real=self.real, imag=-self.imag)

    def _operator_fallbacks(monomorphic_operator, fallback_operator):

        def forward(a, b):
            if isinstance(b, BaseField):
                return monomorphic_operator(a, b)
            elif isinstance(b, (int, float, numbers.Complex, ReField)):
                return fallback_operator(a, Field(b))
            else:
                return NotImplemented

        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, BaseField):
                return monomorphic_operator(a, b)
            elif isinstance(a, (int, float, numbers.Complex, ReField)):
                return fallback_operator(Field(a), b)
            else:
                return NotImplemented

        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse

    def _add(l, r):
        if l.is_inf or r.is_inf:
            return Field(is_inf=True)
        else:
            return Field(real=l.real + r.real, imag=l.imag + r.imag)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)


    def _sub(l, r):
        if l.is_inf or r.is_inf:
            return Field(is_inf=True)
        else:
            return Field(real=l.real - r.real, imag=l.imag - r.imag)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)


    def _mul(l, r):
        if l.is_inf or r.is_inf:
            if l == 0 or r == 0:
                raise ZeroDivisionError('Nan')
            else:
                return Field(is_inf=True)
        else:
            return Field(real=l.real * r.real - l.imag * r.imag, imag=l.real * r.imag + l.imag * r.real)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)


    def _div(l, r):
        return l * r.inv()

    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)


    def angle(self):
        return degrees(phase(compile(self)))

    def inv(self):
        if self.sq_abs() == 0:
            return Field(is_inf=True)
        else:
            return Field(
                real=self.real / self.sq_abs(),
                imag=-self.imag / self.sq_abs()
            )

    @property
    def is_inf(self):
        return self._is_inf

    @property
    def is_zero(self):
        return not self.is_inf and not(self.real or self.imag)

    def __neg__(self):
        return Field(real=-self.real, imag=-self.imag)


    def __abs__(self):
        return sqrt(float(self.real) ** 2 + float(self.imag) ** 2)


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

    def __rpow__(self, other):
        pass

    def __pos__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, BaseField):
            if self.is_inf or other.is_inf:
                return self.is_inf and other.is_inf
            else:
                return (self.real == other.real and
                        self.imag == other.imag)
        elif isinstance(other, (int, float, Decimal)):
            if self.is_inf:
                return math.isinf(other)
            else:
                return self.real == other

        elif isinstance(other, numbers.Complex):
            return (self.is_inf and other.imag == float('inf')) or \
                   (self.real == other.real and
                    self.imag == other.imag)


    def __hash__(self):
        return hash(repr(self))



    @classmethod
    def sort_key(cls, fi):
        return [fi.imag.sign(), fi.imag.sign() * fi.imag / fi.real]

# TODO: remove from there
    # Constants
    @classmethod
    def zero(cls):
        return Field()

    @classmethod
    def one(cls):
        return Field(1)

    @classmethod
    def inf(cls):
        return Field(is_inf=True)
