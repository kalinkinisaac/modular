from .base_gamma import BaseGamma
from .gamma_one import GammaBotOne
from .subgroup import subgroup_action
from mmath import Mat

class SubGammaOne(BaseGamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    # Trivial representatives
    def gen_reprs(self):
        for a in range(self.N):
            self.reprs.append(Mat(1, a, 0, 1))

    # Identity transformation
    def reduced(self, mat: Mat):
        a = mat.a

        if a > self.N // 2:
            mat = (-mat) % self.N

        return mat


class Gamma(BaseGamma):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs, self.not_cached_reduced = subgroup_action(self.N, SubGammaOne(self.N), GammaBotOne(self.N))

    @staticmethod
    def sort_key(m):
        return [m.c, m.d, m.a, m.b]