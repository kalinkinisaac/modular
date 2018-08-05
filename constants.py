from fimath import (Mat, Field, ReField, inf)
from fractions import Fraction

IDM = Mat(1, 0, 0, 1)
G0 = Mat(0, -1, 1, 0)
G1 = Mat(0, 1, -1, 1)
G1_2 = G1 ** 2

G0_ = Mat(0, 1, -1, 0)
G1_ = Mat(1, 1, -1, 0)
G1_2_ = G1_ ** 2

G_ = Mat(1, -1, 0, 1)
G__ = Mat(1, 0, -1, 1)

ZERO = Field(0)
ONE = Field(1)
INF = inf

V0 = Field(1j)
V1 = Field(ReField(1/2), ReField(b=1/2))

