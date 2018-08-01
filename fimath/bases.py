import abc
import math
import numbers

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
    def _inv(self):
        raise NotImplementedError

    def __float__(self):
        return self.a + self.b * math.sqrt(3)

class BaseField(numbers.Complex):
    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    @property
    @abc.abstractmethod
    def is_inf(self):
        raise NotImplementedError

    def __complex__(self):
        if self.is_inf:
            return complex('inf')
        else:
            return complex(
                self.a + self.b * math.sqrt(3),
                self.c + self.d * math.sqrt(3)
            )