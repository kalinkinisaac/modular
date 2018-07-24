from .base_gamma import BaseGamma
from .gamma_zero import (GammaBotZero, GammaTopZero)
from .subgroup import subgroup_action
from .algo import gcd, inv_element
from fimath import Mat

class SubGammaZero(BaseGamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        # Generating set of orbit representatives
        # of action $\Gamma_1(N)$ on $\Gamma_0(N)$
        self.reprs = []
        for a in range(1, self.N // 2 + 1):
            if gcd(a, self.N) == 1:
                self.reprs.append(Mat(a, 0, 0, inv_element(a, self.N)))

    # Constructing reduction procedure
    def reduced(self, mat: Mat):
        a, b = mat.a, mat.d
        if a > self.N // 2:
            a = (-a) % self.N
            b = (-b) % self.N
        return Mat(a, 0, 0, b)


class GammaBotOne(BaseGamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs, self.not_cached_reduced = subgroup_action(self.N, SubGammaZero(self.N), GammaBotZero(self.N))

    @staticmethod
    def sort_key(m):
        return [m.c, m.d, m.a, m.b]


class GammaTopOne(BaseGamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs, self.not_cached_reduced = subgroup_action(self.N, SubGammaZero(self.N), GammaTopZero(self.N))

    @staticmethod
    def sort_key(m):
        return [m.a, m.b, m.c, m.d]
