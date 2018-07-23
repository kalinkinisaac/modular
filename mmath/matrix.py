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
                    if other.is_inf:
                        return s.a * Field.one() / s.c
                    elif other == -s.d * Field.one() / s.c:
                        return Field.inf()


                if other.is_inf:
                    return Field.inf()

            return (s.a * other + s.b) / (s.c * other + s.d)
        elif type(other) == int:
            return Mat(
                s.a * other,
                s.b * other,
                s.c * other,
                s.d * other
            )
        else:
            UnsupportedTypeError(other)

    def __mod__(self, other):
        if type(other) == int:
            return Mat(
                self.a % other,
                self.b % other,
                self.c % other,
                self.d % other
            )

    def __neg__(self):
        return Mat(
            -self.a,
            -self.b,
            -self.c,
            -self.d
        )

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d

    def __pow__(self, power : int, modulo=None):
        if power == 0:
            return Mat.identity()

        if power > 0:
            result = Mat.identity()
            for _ in range(power):
                result = result * self
            return result

        if power < 0:
            result = Mat.identity()
            for _ in range(power):
                result = result * self
            return result.inv()

    def dot(self, other):
        return self * other

    def inv(self):
        if self.a * self.d - self.b * self.c == 0:
            print(self)
            raise ZeroDivisionError()

        return Mat(self.d, -self.b, -self.c, self.a) * (self.a * self.d - self.b * self.c)


    def __rmul__(self, other):
        return self * other

    def __repr__(s):
        return f'[{s.a} {s.b}]\n[{s.c} {s.d}]'

    # Constants
    @classmethod
    def identity(cls):
        return Mat(a=1, b=0, c=0, d=1)
