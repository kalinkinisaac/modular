from constants import (IDM, G0, G1, G1_2)
import numpy as np
from graph import BCGraph
from numpy_helpers import *

def construct_g_0_graph(gamma):
    gc = GraphConstructor(
        L=gamma.L,
        reduce=gamma.reduce,
        sort_key=gamma.sort_key,
        N=gamma.N)

    return gc.construct_graph()

class GraphConstructor(object):

    def __init__(self, L, N, reduce, sort_key):
        self.L = L
        self.reduce = reduce
        self.N = N
        self.sort_key = sort_key

    def construct_graph(self):
        L = list(map(np.matrix, self.L))
        self.V0 = []
        self.V1 = []

        for matrix in L:
            orbit = self.g_0_orbit(matrix)
            if np.array_equal(matrix, self.minimum(orbit)):
                self.V0.append(matrix)

            orbit = self.g_1_orbit(matrix)
            if np.array_equal(matrix, self.minimum(orbit)):
                self.V1.append(matrix)

        self.V0.sort(key=self.sort_key)
        self.V1.sort(key=self.sort_key)

        self.v02n = dict({(self.V0[i].tobytes(), i) for i in range(len(self.V0))})
        self.v12n = dict({(self.V1[i].tobytes(), i) for i in range(len(self.V1))})

        V0G = [list(map(lambda x: self.v12n[x.tobytes()], self.g_0_neighbors(v))) for v in self.V0]
        V1G = [list(map(lambda x: self.v02n[x.tobytes()], self.g_1_neighbors(v))) for v in self.V1]

        v0 = self.minimum(self.g_0_orbit(IDM))
        v1 = self.minimum(self.g_1_orbit(IDM))

        # Distinguished edge
        orbit = self.g_1_orbit(v1)
        neighbors = self.g_1_neighbors(v1)

        j_0 = np_index(IDM, orbit)
        j = 0

        if np_count(v0, neighbors) > 1:
            if np.array_equal(v0, neighbors[(j_0 - 1) % 3]):
                j = 1
            else:
                j = 2



        return BCGraph(
            V0=V0G,
            V1=V1G,
            dist_edge=[self.v02n[v0.tobytes()], self.v12n[v1.tobytes()], j],
            sort_key=self.sort_key)



    def action(self, element, g):
        n_matrix = g % self.N
        return self.reduce(element.dot(n_matrix))

    def minimum(self, orbit):
        orbit.sort(key=self.sort_key)
        return  orbit[0]

    def g_0_orbit(self, matrix):
        matrix = matrix % self.N
        acted = self.action(matrix, G0)

        if np.array_equal(matrix, acted):
            return [matrix]
        else:
            return [matrix, acted]

    def g_1_orbit(self, matrix):
        matrix = matrix % self.N
        acted = self.action(matrix, G1)

        if np.array_equal(matrix, acted):
            return [matrix]
        else:
            return [matrix, acted, self.action(matrix, G1_2)]

    def g_0_neighbors(self, matrix):
        orbit = self.g_0_orbit(matrix)
        return [self.minimum(self.g_1_orbit(m)) for m in orbit]

    def g_1_neighbors(self, matrix):
        orbit = self.g_1_orbit(matrix)
        return [self.minimum(self.g_0_orbit(m)) for m in orbit]
