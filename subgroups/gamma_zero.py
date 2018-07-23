from .base_gamma import BaseGamma
from .isomorphism import (one2many, many2one)
from .algo import (factor, get_xy, gcd, inv_element)
from math import log
from mmath import Mat
import itertools


class GammaZero(BaseGamma):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.pair_reprs = []
        self.fact = factor(self.N)
        self.gen_pair_reprs()

    def gen_pair_reprs(self):
        tmp_pair_reprs = []
        for (p_i, m_i) in self.fact:
            tmp_pair_reprs += [self._gen_pair_reprs_prime(p_i, m_i)]


        for combination in list(itertools.product(*tmp_pair_reprs)):
            self.pair_reprs.append(many2one(list(combination)))

    def _gen_pair_reprs_prime(self, p, m):
        reprs = []
        reprs.append([0, 1, [p, m]])
        reprs.extend([[1, i, [p, m]] for i in range(p ** m)])
        for i in range(1, m):
            bs = list(filter(lambda x: x % p != 0, range(1, p ** (m - i))))
            reprs.extend([[p ** i, b, [p, m]] for b in bs])
        return reprs

    def pair_reduced(self, a, b):
        many = one2many([a, b, self.N], fact=self.fact)
        reduced = []
        for one in many:
            reduced.append(self._pair_reduced(one))
        return many2one(reduced)

    def _pair_reduced(self, one):
        a, b, [p, m] = one
        N = p ** m

        if a % N == 0:
            return [0, 1, [p, m]]

        _gcd = gcd(a, N)
        c = a // _gcd
        i = int(log(_gcd, p))
        bc = (b * inv_element(c, N)) % N
        if i == 0:
            return [1, bc % N, [p, m]]
        else:
            return [p ** i, (bc % p ** (m - i)) % N, [p, m]]


class GammaBotZero(GammaZero):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        self.reprs = []
        for a, b, N in self.pair_reprs:
            self.reprs.append(self.reduced(Mat(0, 0, a, b)))

    def not_cached_reduced(self, mat):
        a, b = mat.c, mat.d
        a, b = self.pair_reduced(a, b)[0:2]
        d, c = list(map(lambda x: x % self.N, get_xy(a, b, self.N)))
        return Mat(c, -d, a, b) % self.N

    @staticmethod
    def sort_key(m):
        return [m.c, m.d, m.a, m.b]


class GammaTopZero(GammaZero):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.gen_reprs()

    def gen_reprs(self):
        for a, b, N in self.pair_reprs:
            self.reprs.append(self.reduced(Mat(a, b, 0, 0)))

    def not_cached_reduced(self, mat):
        a, b = mat.a, mat.b
        a, b = self.pair_reduced(a, b)[0:2]
        d, c = list(map(lambda x : x % self.N, get_xy(a, b, self.N)))
        return Mat(a, b,-c, d) % self.N


    @staticmethod
    def sort_key(m):
        return [m.a, m.b, m.c, m.d]