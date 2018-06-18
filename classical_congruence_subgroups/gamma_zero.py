from .isomorphism import (one2many, many2one)
from .algo import (factor, get_xy, gcd, inv_element)
from math import log
import numpy as np
import itertools


class GammaZero(object):

    def __init__(self, N):
        self.N = N

        self._fact = factor(self.N)
        self.fact = list(zip(self._fact.keys(), self._fact.values()))

        self.representatives = []
        self.gen_reprs()
        self.L = []


    def gen_reprs(self):
        t_repr = []
        for (p_i, m_i) in self.fact:
            t_repr.append(self._gen_reprs_prime(p_i, m_i))
        for combination in list(itertools.product(*t_repr)):
            self.representatives.append(many2one(list(combination)))

    def _gen_reprs_prime(self, p, m):
        representatives = []
        representatives.append([0, 1, [p, m]])
        representatives.extend([[1, i, [p, m]] for i in range(p ** m)])
        for i in range(1, m):
            bs = list(filter(lambda x: x % p != 0, range(1, p ** (m - i))))
            representatives.extend([[p ** i, b, [p, m]] for b in bs])
        return representatives

    def pair_reduction_procedure(self, a, b):
        many = one2many([a, b, self.N], fact=self._fact)
        reduced = []
        for one in many:
            reduced.append(self._pair_reduction_procedure(one))
        return many2one(reduced)

    def _pair_reduction_procedure(self, one):
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
        self.reduce_cache = dict()
        self.gen_l()

    def gen_l(self):
        self.L = []
        for a, b, N in self.representatives:
            self.L.append(self.reduce(np.matrix([[0, 0], [a, b]])))

    def reduce(self, matrix):
        a, b = matrix.item(1,0), matrix.item(1,1)
        if (a, b) in self.reduce_cache:
            return self.reduce_cache[(a, b)]
        else:
            self.reduce_cache[(a, b)] = self._reduce(a, b)
            return self.reduce_cache[(a, b)]

    def _reduce(self, a, b):
        a, b = self.pair_reduction_procedure(a, b)[0:2]
        d, c = list(map(lambda x : x % self.N, get_xy(a, b, self.N)))
        return np.matrix([[c, (-d)], [a, b]]) % self.N

    @staticmethod
    def sort_key(m):
        return [m.item(1, 0), m.item(1, 1), m.item(0, 0), m.item(0, 1)]


class GammaTopZero(GammaZero):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reduce_cache = dict()
        self.gen_l()

    def gen_l(self):
        self.L = []
        for a, b, N in self.representatives:
            self.L.append(self.reduce(np.matrix([[a, b],[0,0]])))

    def reduce(self, matrix):
        a, b = matrix.item(0,0), matrix.item(0,1)
        if (a, b) in self.reduce_cache:
            return self.reduce_cache[(a, b)]
        else:
            self.reduce_cache[(a, b)] = self._reduce(a, b)
            return self.reduce_cache[(a, b)]

    def _reduce(self, a, b):
        a, b = self.pair_reduction_procedure(a, b)[0:2]
        d, c = list(map(lambda x : x % self.N, get_xy(a, b, self.N)))
        return np.matrix([[a, b],[(-c), d]]) % self.N

    @staticmethod
    def sort_key(m):
        return [ m.item(0, 0), m.item(0, 1), m.item(1, 0), m.item(1, 1)]