from .field import Field
from .error import UnsupportedTypeError

class Mat(object):

    def __init__(self, a : int, b : int, c : int, d : int):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __mul__(s, other):
        if type(other) == __class__:
            return Mat(
                a =s.a * other.a + s.b * other.c,
                b =s.a * other.b + s.b * other.d,
                c =s.c * other.a + s.d * other.c,
                d =s.c * other.b + s.d * other.d
            )
        elif type(other) == Field:
            if s.a * s.d == s.b * s.c:
                return Field(a=s.a) / s.c
            else:
                if s.c != 0:
                    if other == -s.d * Field.one() / s.c:
                        return Field.inf()
                    elif other.is_inf:
                        return s.a * Field.one() / s.c

                if other.is_inf:
                    return Field.inf()

            return (s.a * other + s.b) / (s.c * other + s.d)
        else:
            UnsupportedTypeError(other)

    def __rmul__(self, other):
        return self * other

    def __repr__(s):
        return f'[{s.a} {s.b}]\n[{s.c} {s.d}]'

    # Constants
    @classmethod
    def identity(cls):
        return Mat(a=1, b=0, c=0, d=1)
