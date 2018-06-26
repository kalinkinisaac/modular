from .base_gamma import BaseGamma
from .gamma_one import GammaBotOne
from .subgroup import subgroup_action
import numpy as np
from constants import IDM

class SubGamma(BaseGamma):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    # Trivial representatives
    def gen_reprs(self):
        self.reprs = [IDM]

    # Identity transformation
    def reduced(self, mat: np.matrix):
        return IDM


class Gamma(BaseGamma):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs, self.not_cached_reduced = subgroup_action(self.N, SubGamma(self.N), GammaBotOne(self.N))

    @staticmethod
    def sort_key(m):
        return [m.item(1, 0), m.item(1, 1), m.item(0, 0), m.item(0, 1)]