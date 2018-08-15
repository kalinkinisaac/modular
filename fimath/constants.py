from .field import Field
from .re_field import ReField
from .matrix import Matrix

inf = Field(is_inf=True)

IDM = Matrix(1, 0, 0, 1)
G0 = Matrix(0, -1, 1, 0)
G1 = Matrix(0, 1, -1, 1)
G1_2 = G1 ** 2

G0_ = Matrix(0, 1, -1, 0)
G1_ = Matrix(1, 1, -1, 0)
G1_2_ = G1_ ** 2

G_ = Matrix(1, -1, 0, 1)
G__ = Matrix(1, 0, -1, 1)

ZERO = Field(0)
ONE = Field(1)
INF = inf

V0 = Field(1j)
V1 = Field(ReField(1/2), ReField(b=1/2))

