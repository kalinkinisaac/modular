from graph import BCGraph
from fimath.constants import *
from .error import ReprNotFoundError


class GraphConstructor(object):

    def __init__(self, l, n, reduced, sort_key):
        self.L = l
        self.N = n
        self.reduced = reduced
        self.sort_key = sort_key
        self.V0 = []
        self.V1 = []

    def construct(self):
        self.V0 = []
        self.V1 = []

        for mat in self.L:
            orb = self.g0_orb(mat)
            if mat == self.minimum(orb):
                self.V0.append(mat)

            orb = self.g1_orb(mat)
            if mat == self.minimum(orb):
                self.V1.append(mat)

        self.V0.sort(key=self.sort_key)
        self.V1.sort(key=self.sort_key)

        _v02n = dict({(self.V0[i], i) for i in range(len(self.V0))})
        _v12n = dict({(self.V1[i], i) for i in range(len(self.V1))})

        def v02n(_v0):
            if _v0 not in _v02n.keys():
                raise ReprNotFoundError(_v0)
            else:
                return _v02n[_v0]

        def v12n(_v1):
            if _v1 not in _v12n.keys():
                raise ReprNotFoundError(_v1)
            else:
                return _v12n[_v1]

        v0_g = [list(map(v12n, self.g0_nei(v))) for v in self.V0]
        v1_g = [list(map(v02n, self.g1_nei(v))) for v in self.V1]

        v0 = self.minimum(self.g0_orb(IDM))
        v1 = self.minimum(self.g1_orb(IDM))

        # Finding distinguished edge
        orb = self.g1_orb(v1)
        neighbors = self.g1_nei(v1)

        j_0 = orb.index(IDM)
        j = 0

        if neighbors.count(v0) > 1:
            if v0 == neighbors[(j_0 - 1) % 3]:
                j = 1
            else:
                j = 2

        return BCGraph(
            v0=v0_g,
            v1=v1_g,
            dist_edge=[v02n(v0), v12n(v1), j]
        )

    def acted(self, element, g):
        n_matrix = g % self.N
        return self.reduced((element * n_matrix) % self.N)

    def minimum(self, orb):
        orb.sort(key=self.sort_key)
        return orb[0]

    # Returns orbit of matrix
    def g0_orb(self, mat: Matrix):
        mat = mat % self.N
        acted = self.acted(mat, G0)

        if mat == acted:
            return [mat]
        else:
            return [mat, acted]

    def g1_orb(self, mat: Matrix):
        mat = mat % self.N
        acted = self.acted(mat, G1)

        if mat == acted:
            return [mat]
        else:
            return [mat, acted, self.acted(mat, G1_2)]

    # Returns neighbors of vertex
    def g0_nei(self, mat: Matrix):
        orbit = self.g0_orb(mat)
        return [self.minimum(self.g1_orb(m)) for m in orbit]

    def g1_nei(self, mat: Matrix):
        orbit = self.g1_orb(mat)
        return [self.minimum(self.g0_orb(m)) for m in orbit]
