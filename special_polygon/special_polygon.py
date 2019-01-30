from graph import BCGraph
from .star_type import StarType
from fimath.geodesic import Geodesic
from fimath.constants import *

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', filename='log.log', level=logging.DEBUG)


class SpecialPolygon(object):

    def __init__(self, graph=BCGraph()):
        self._graph = graph
        self._edges = []
        self._involutions = []
        self._tree = []
        self._white_vertices = []
        self._black_vertices = []
        self._cut_vertices = []

        self._L0 = []
        self._L1 = []
        self._G = []
        self._visited = [False] * len(self._graph.V0)
        self._removed = [False] * len(self._graph.V0)
        self._I = [-1] * len(self._graph.V0)

    @property
    def edges(self):
        return self._edges

    @property
    def involutions(self):
        return self._involutions

    @property
    def tree(self):
        return self._tree

    @property
    def white_vertices(self):
        return self._white_vertices

    @property
    def black_vertices(self):
        return self._black_vertices

    @property
    def cut_vertices(self):
        return self._cut_vertices

    def construct_polygon(self):
        logging.debug('graph constructing procedure started')

        neighbors = self._graph.v1_nei(self._graph.v1)
        star_v1 = StarType.from_nei(neighbors)

        self._tree.append(Geodesic(V0, V1))

        if star_v1 == StarType.Segment:
            logging.debug('case 0.1: Start V1 is a segment.')

            self._L0.append(self._graph.v0)
            self._L1.append(self._graph.v1)
            self._G.append(IDM)
            self._I.append(0)

            s1 = Geodesic(V1, INF)
            s2 = Geodesic(V1, ZERO)

            self._edges.extend([s1, s2])
            self._involutions.append([s1, s2, G1])
            self._white_vertices.append(V1)

            logging.debug(f'added edges:\ns1: {s1}\ns2: {s2}')

        else:
            self._tree.extend([G1.moe(Geodesic(V0, V1)), G1_2.moe(Geodesic(V0, V1))])

            if star_v1 == StarType.SlingShot:
                logging.debug('case 0.2: Star V1 is a sling shot.')

                v_ = BCGraph.cyc_next(self._graph.v0, neighbors)
                v__ = BCGraph.cyc_next(v_, neighbors)

                self._L0.extend([self._graph.v0, v_, v__])
                self._L1.extend([self._graph.v1] * 3)
                self._G.extend([IDM, G1, G1_2])

                self._I[self._graph.v0] = 0
                self._I[v_] = 1
                self._I[v__] = 2

                self._visited[self._graph.v0] = True
                self._visited[v_] = True
                self._visited[v__] = True

            else:
                logging.debug('case 0.3: Star V1 is a racket')

                v = SpecialPolygon.unique(neighbors)
                j = self._graph.dist_j

                self._L0.append(v)
                self._L1.append(self._graph.v1)
                self._G.append(G1 ** j)
                self._I[v] = 0

                s = [Geodesic(ZERO, INF), Geodesic(ZERO, ONE), Geodesic(ONE, INF)]
                v = [V0, Field(0.5+0.5j), Field(1+1j)]
                s1 = s[(j + 1) % 3]
                s2 = s[(j + 2) % 3]
                g = (G1 ** (j - 1) * G_ * G1 ** (1 - j))

                self._edges.extend([s1, s2])
                self._involutions.append([s1, s2, g])
                self.cut_vertices.extend([v[(j + 1) % 3], v[(j + 2) % 3]])
                logging.debug(f'added edges:\ns1 = {s1}\ns2 = {s2}')

        logging.debug('initial prepararion finished')

        while self._L0:
            self._induction()
            logging.debug('end of induction')

        return self._edges, self._tree, self._involutions

    def _induction(self):
        logging.debug(f'new induction\nL0 = {self._L0}\nL1 = {self._L1}\nG =\n{self._G}')

        v = self._L0.pop()
        v_ = self._L1.pop()
        g = self._G.pop()

        logging.debug(f'popped:\nV = {v},\nV\' = {v_},\ng =\n{g}')

        if self._removed[v]:
            logging.debug('V was marked \"to be removed\"\nend of induction')
            return

        if self._graph.is_v0_uni(v):
            self._case_1(g)

        else:
            v__ = (set(self._graph.v0_nei(v)) - {v_}).pop()
            star_v__ = StarType.from_nei(self._graph.v1_nei(v__))

            logging.debug(f'case 2: V has valency 2\tV\'\' = {v__}')

            if star_v__ == StarType.Segment:
                self._case_2a(g)

            else:
                self._tree.extend([(g * G0).moe(Geodesic(V0, V1)),
                                   (g * G_).moe(Geodesic(V0, V1)),
                                   (g * G__).moe(Geodesic(V0, V1))
                                   ])

                if star_v__ == StarType.SlingShot:
                    self._case_2b(v, g, v__, star_v__)

                elif star_v__ == StarType.Racket:
                    self._case_2c(g)

                else:
                    # nearly impossible
                    raise Exception('There is not such case')

    def _case_1(self, g):
        s1_ = Geodesic(V0, ZERO)
        s2_ = Geodesic(V0, INF)

        s1 = g.moe(s1_)
        s2 = g.moe(s2_)

        self._edges.extend([s1, s2])
        self._involutions.append([s1, s2, g * G0 * g.inv()])
        self._black_vertices.append(g.moe(V0))

        logging.debug(f'case 1: V is univalent\nadded edges:\ns1 = {s1},\ns2 = {s2}')

    def _case_2a(self, g):
        s1_ = Geodesic(V1, ZERO)
        s2_ = Geodesic(V1, INF)

        g_g0 = g * G0

        s1 = g_g0.moe(s1_)
        s2 = g_g0.moe(s2_)

        self._edges.extend([s1, s2])
        self._tree.append(g_g0.moe(Geodesic(V0, V1)))
        self._involutions.append([s1, s2, g_g0 * G1_2 * g_g0.inv()])
        self._white_vertices.append(g_g0.moe(V1))

        logging.debug(f'case 2a: Star V\'\' is a segment\nadded edges:\ns1 = {s1},\ns2 = {s2}')

    def _case_2b(self, v, g, v__, star_v__):
        self._tree.extend([(g * G0).moe(Geodesic(V0, V1)),
                           (g * G_).moe(Geodesic(V0, V1)),
                           (g * G__).moe(Geodesic(V0, V1))
                           ])

        if star_v__ == StarType.SlingShot:
            v1 = self._graph.cyc_next(v, self._graph.v1_nei(v__))
            v2 = self._graph.cyc_next(v1, self._graph.v1_nei(v__))

            logging.debug(f'case 2b: Star V\'\' is a sling shot,\nV1 = {v1},\nV2 = {v2}')

            for w in [v1, v2]:
                if self._visited[w]:
                    self._case_2b__(g, w, v1)
                else:
                    self._case_2b_(g, v__, w, v1)

    def _case_2b_(self, g, v__, w, v1):
        self._I[w] = len(self._L0)
        self._L0.append(w)
        self._L1.append(v__)

        if w == v1:
            self._G.append(g * G_)
        else:
            self._G.append(g * G__)

        self._visited[w] = True
        logging.debug(f'case 2b\': W({w}) marked as \"unvisited\"')

    def _case_2b__(self, g, w, v1):
        l_ = self._I[w]
        g_ = self._G[l_]

        if w == v1:
            e = G_
        else:
            e = G__

        s0 = Geodesic(ZERO, INF)
        s1 = (g * e).moe(s0)
        s2 = g_.moe(s0)

        self._edges.extend([s1, s2])
        self._involutions.append([s1, s2, g_ * G0 * (g * e).inv()])
        self._cut_vertices.extend([(g * e).moe(V0), g_.moe(V0)])

        self._removed[self._L0[l_]] = True
        logging.debug(f'case 2b\'\': W({w}) marked as \"visited\"\nadded edges:\ns1: {s1},\ns2 : {s2}')

    def _case_2c(self, g):
        s0 = Geodesic(ZERO, INF)
        g1 = g * G_
        g2 = g * G__
        s1 = g1.moe(s0)
        s2 = g2.moe(s0)
        self._edges.extend([s1, s2])
        self._involutions.append([s1, s2, g2 * (g1 * G0).inv()])
        self._cut_vertices.extend([g1.moe(V0), g2.moe(V0)])

        logging.debug(f'case 2c: Star V__ is a racket\nadded edges:\ns1 : {s1},\ns2 : {s2}')

    @staticmethod
    def unique(triple):
        for x in triple:
            if triple.count(x) == 1:
                return x
