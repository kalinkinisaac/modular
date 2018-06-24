from .gamma import Gamma
from .gamma_zero import (GammaBotZero, GammaTopZero)
from .subgroup import subgroup_action
from .algo import gcd, inv_element
import numpy as np

class SubGammaOne(Gamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        # Generating set of orbit representatives
        # of action $\Gamma_1(N)$ on $\Gamma_0(N)$
        self.reprs = []
        for a in range(1, self.N // 2 + 1):
            if gcd(a, self.N) == 1:
                self.reprs.append(np.matrix([[a, 0], [0, inv_element(a, self.N)]]))

    # Constructing reduction procedure
    def reduced(self, mat: np.matrix):
        a, b = mat.item(0, 0), mat.item(1, 1)
        return np.matrix([[a, 0], [0, b]])


class GammaBotOne(Gamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs, self.not_cached_reduced = subgroup_action(self.N, SubGammaOne(self.N), GammaBotZero(self.N))

    @staticmethod
    def sort_key(m):
        return [m.item(1, 0), m.item(1, 1), m.item(0, 0), m.item(0, 1)]


class GammaTopOne(Gamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs, self.not_cached_reduced = subgroup_action(self.N, SubGammaOne(self.N), GammaTopZero(self.N))

    @staticmethod
    def sort_key(m):
        return [m.item(0, 0), m.item(0, 1), m.item(1, 0), m.item(1, 1)]
