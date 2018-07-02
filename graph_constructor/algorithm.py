from constants import (IDM, G0, G1, G1_2)
import numpy as np
from graph import BCGraph
from numpy_helpers import *
from .error import ReprNotFoundError

def construct_g_0_graph(gamma):
    gc = GraphConstructor(
        L=gamma.reprs,
        reduced=gamma.reduced,
        sort_key=gamma.sort_key,
        N=gamma.N)


    return gc.construct_graph()

def construct_g_1_graph(gamma):
    gc = GraphConstructor(
        L=gamma.reprs,
        reduced=gamma.reduced,
        sort_key=gamma.sort_key,
        N=gamma.N)

    return gc.construct_graph()

class GraphConstructor(object):

    def __init__(self, L, N, reduced, sort_key):
        self.L = L
        self.reduced = reduced
        self.N = N
        self.sort_key = sort_key

    def construct_graph(self):
        L = list(map(np.matrix, self.L))
        self.V0 = []
        self.V1 = []

        for mat in L:
            orb = self.g0_orb(mat)
            if np.array_equal(mat, self.minimum(orb)):
                self.V0.append(mat)

            orb = self.g1_orb(mat)
            if np.array_equal(mat, self.minimum(orb)):
                self.V1.append(mat)

        self.V0.sort(key=self.sort_key)
        self.V1.sort(key=self.sort_key)

        self._v02n = dict({(self.V0[i].tobytes(), i) for i in range(len(self.V0))})
        self._v12n = dict({(self.V1[i].tobytes(), i) for i in range(len(self.V1))})

        def v02n(v0):
            b_hash = v0.tobytes()
            if b_hash not in self._v02n.keys():
                raise ReprNotFoundError(v0)
            else:
                return self._v02n[b_hash]

        def v12n(v1):
            b_hash = v1.tobytes()
            if b_hash not in self._v12n.keys():
                raise ReprNotFoundError(v1)
            else:
                return self._v12n[b_hash]

        V0G = [list(map(v12n, self.g0_nei(v))) for v in self.V0]
        V1G = [list(map(v02n, self.g1_nei(v))) for v in self.V1]

        v0 = self.minimum(self.g0_orb(IDM))
        v1 = self.minimum(self.g1_orb(IDM))

        # Calculating distinguished edge
        orb = self.g1_orb(v1)
        neighbors = self.g1_nei(v1)

        j_0 = np_index(IDM, orb)
        j = 0

        if np_count(v0, neighbors) > 1:
            if np.array_equal(v0, neighbors[(j_0 - 1) % 3]):
                j = 1
            else:
                j = 2



        return BCGraph(
            V0=V0G,
            V1=V1G,
            dist_edge=[v02n(v0), v12n(v1), j],
            sort_key=self.sort_key)

    def acted(self, element, g):
        n_matrix = g % self.N
        return self.reduced(element.dot(n_matrix) % self.N)

    def minimum(self, orb):
        orb.sort(key=self.sort_key)
        return orb[0]

    # Returns orbit of matrix
    def g0_orb(self, mat):
        mat = mat % self.N
        acted = self.acted(mat, G0)

        if np.array_equal(mat, acted):
            return [mat]
        else:
            return [mat, acted]

    def g1_orb(self, mat):
        mat = mat % self.N
        acted = self.acted(mat, G1)

        if np.array_equal(mat, acted):
            return [mat]
        else:
            return [mat, acted, self.acted(mat, G1_2)]

    # Returns neighbors of vertex
    def g0_nei(self, mat):
        orbit = self.g0_orb(mat)
        return [self.minimum(self.g1_orb(m)) for m in orbit]

    def g1_nei(self, mat):
        orbit = self.g1_orb(mat)
        return [self.minimum(self.g0_orb(m)) for m in orbit]
