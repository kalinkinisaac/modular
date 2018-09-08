import abc
import math
import numbers


class BaseGeodesic(object):
    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    @property
    @abc.abstractmethod
    def begin(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def end(self):
        raise NotImplementedError


class BaseMatrix(object):
    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    @property
    @abc.abstractmethod
    def a(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def b(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def c(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def d(self):
        raise NotImplementedError

    @abc.abstractmethod
    def inv(self):
        raise NotImplementedError

    @staticmethod
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


class BaseReField(object):
    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    @property
    @abc.abstractmethod
    def a(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def b(self):
        raise NotImplementedError

    @abc.abstractmethod
    def inv(self):
        raise NotImplementedError

    def __float__(self):
        return self.a + self.b * math.sqrt(3)


class BaseField(numbers.Complex):

    __slots__ = ()

    @property
    def real(self):
        raise NotImplementedError

    @property
    def imag(self):
        raise NotImplementedError

    @property
    def is_inf(self):
        raise NotImplementedError

    def __complex__(self):
        raise NotImplementedError

    def __add__(self, other):
        """self + other"""
        raise NotImplementedError

    def __radd__(self, other):
        """other + self"""
        raise NotImplementedError

    def __neg__(self):
        """-self"""
        raise NotImplementedError

    def __pos__(self):
        """+self"""
        raise NotImplementedError

    def __sub__(self, other):
        """self - other"""
        return self + -other

    def __rsub__(self, other):
        """other - self"""
        return -self + other

    def __mul__(self, other):
        """self * other"""
        raise NotImplementedError

    def __rmul__(self, other):
        """other * self"""
        raise NotImplementedError

    def __truediv__(self, other):
        """self / other: Should promote to float when necessary."""
        raise NotImplementedError

    def __rtruediv__(self, other):
        """other / self"""
        raise NotImplementedError

    def __pow__(self, exponent):
        """self**exponent; should promote to float or complex when necessary."""
        raise NotImplementedError

    def __rpow__(self, base):
        """base ** self"""
        raise NotImplementedError

    def __abs__(self):
        """Returns the Real distance from 0. Called for abs(self)."""
        raise NotImplementedError

    def conjugate(self):
        """(x+y*i).conjugate() returns (x-y*i)."""
        raise NotImplementedError

    def __eq__(self, other):
        """self == other"""
        raise NotImplementedError
