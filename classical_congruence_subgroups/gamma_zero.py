from .gamma import Gamma
from .isomorphism import (one2many, many2one)
from .algo import (factor, get_xy, gcd, inv_element)
from math import log
import numpy as np
import itertools


class GammaZero(Gamma):

    def __init__(self, *args, **kwargs):

        self._fact = None
        self.fact = None

        super(__class__, self).__init__(*args, **kwargs)

    def gen_reprs(self):
        self._fact = factor(self.N)
        self.fact = list(zip(self._fact.keys(), self._fact.values()))

        t_repr = []
        for (p_i, m_i) in self.fact:
            t_repr.append(self._gen_reprs_prime(p_i, m_i))
        for combination in list(itertools.product(*t_repr)):
            self.reprs.append(many2one(list(combination)))

    def _gen_reprs_prime(self, p, m):
        reprs = []
        reprs.append([0, 1, [p, m]])
        reprs.extend([[1, i, [p, m]] for i in range(p ** m)])
        for i in range(1, m):
            bs = list(filter(lambda x: x % p != 0, range(1, p ** (m - i))))
            reprs.extend([[p ** i, b, [p, m]] for b in bs])
        return reprs

    def pair_reduction(self, a, b):
        many = one2many([a, b, self.N], fact=self._fact)
        reduced = []
        for one in many:
            reduced.append(self._pair_reduction(one))
        return many2one(reduced)

    def _pair_reduction(self, one):
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


class GammaBottomZero(GammaZero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gen_l()

    def gen_l(self):
        self.L = []
        for a, b, N in self.reprs:
            self.L.append(self.reduced(np.matrix([[0, 0], [a, b]])))

    def not_cached_reduced(self, matrix):
        a, b = matrix.item(1, 0), matrix.item(1, 1)
        return self._reduced(a, b)

    def _reduced(self, a, b):
        a, b = self.pair_reduction(a, b)[0:2]
        d, c = list(map(lambda x : x % self.N, get_xy(a, b, self.N)))
        return np.matrix([[c, (-d)], [a, b]]) % self.N

    @staticmethod
    def sort_key(m):
        return [m.item(1, 0), m.item(1, 1), m.item(0, 0), m.item(0, 1)]


class GammaTopZero(GammaZero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gen_l()

    def gen_l(self):
        for a, b, N in self.reprs:
            self.L.append(self.reduced(np.matrix([[a, b],[0,0]])))

    def not_cached_reduced(self, matrix):
        a, b = matrix.item(0, 0), matrix.item(0, 1)
        return self._reduced(a, b)

    def _reduced(self, a, b):
        a, b = self.pair_reduction(a, b)[0:2]
        d, c = list(map(lambda x : x % self.N, get_xy(a, b, self.N)))
        return np.matrix([[a, b],[(-c), d]]) % self.N

    @staticmethod
    def sort_key(m):
        return [m.item(0, 0), m.item(0, 1), m.item(1, 0), m.item(1, 1)]