from graph import BCGraph
from .star_type import StarType
from fimath.geodesic import Geodesic, unoriented_eq
from fimath.constants import *

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', filename='log.log',level=logging.DEBUG)


class SpecialPolygon(object):

    def __init__(self, graph=BCGraph()):
        self.graph = graph

    def construct_polygon(self):
        logging.debug('graph constructing procedure started')
        self.L0 = []
        self.L1 = []
        self.G = []
        self.E = []
        self.T = []
        self.generators = []
        self.involutions = []
        self.visited = [False] * len(self.graph.V0)
        self.removed = [False] * len(self.graph.V0)
        self.I = [-1] * len(self.graph.V0)
        self.v0 = self.graph.v0
        self.v1 = self.graph.v1

        neighbors = self.graph.v1_nei(self.v1)
        star_v1 = StarType.star_type(neighbors)

        self.T.append(Geodesic(V0, V1))

        if star_v1 == StarType.Segment:
            logging.debug('case 0.1: Start V1 is a segment.')

            self.L0.append(self.v0)
            self.L1.append(self.v1)
            self.G.append(IDM)
            self.I.append(0)
            s1 = Geodesic(V1, INF)
            s2 = Geodesic(V1, ZERO)
            self.E.extend([s1, s2])
            self.involutions.append([s1, s2, G1])

            logging.debug(f'added edges:\ns1: {s1}\ns2: {s2}')

        else:
            self.T.extend([G1.moe(Geodesic(V0, V1)), (G1_2).moe(Geodesic(V0, V1))])
            self.generators.extend([G1, G1_2])

            if star_v1 == StarType.SlingShot:
                logging.debug('case 0.2: Star V1 is a sling shot.')

                v_ = BCGraph.cyc_next(self.v0, neighbors)
                v__ = BCGraph.cyc_next(v_, neighbors)

                self.L0.extend([self.v0, v_, v__])
                self.L1.extend([self.v1] * 3)
                self.G.extend([IDM, G1, G1_2])

                self.I[self.v0] = 0
                self.I[v_] = 1
                self.I[v__] = 2

                self.visited[self.v0] = True
                self.visited[v_] = True
                self.visited[v__] = True

            else:
                logging.debug('case 0.3: Star V1 is a racket')

                v = self.unique(neighbors)
                j = self.graph.dist_j

                self.L0.append(v)
                self.L1.append(self.v1)
                self.G.append(G1 ** j)
                self.I[v] = 0

                s = [Geodesic(ZERO, INF), Geodesic(ZERO, ONE), Geodesic(ONE, INF)]
                s1 = s[(j + 1) % 3]
                s2 = s[(j + 2) % 3]
                g = (G1 ** (j - 1) * G_ * G1 ** (1 - j))

                self.E.extend([s1, s2])
                self.involutions.append([s1, s2, g])
                logging.debug(f'added edges:\ns1 = {s1}\ns2 = {s2}')


        logging.debug('initial prepararion finished')

        while(self.L0):
            self.induction()
            logging.debug('end of induction')

        return self.E, self.T, self.involutions



    def induction(self):
        logging.debug(f'new induction\nL0 = {self.L0}\nL1 = {self.L1}\nG =\n{self.G}')

        v = self.L0.pop()
        v_ = self.L1.pop()
        g = self.G.pop()

        logging.debug(f'popped:\nV = {v},\nV\' = {v_},\ng =\n{g}')

        if self.removed[v]:
            logging.debug('V was marked \"to be removed\"\nend of induction')
            return

        if self.graph.is_v0_uni(v):
            self._case_1(g)

        else:
            v__ = (set(self.graph.v0_nei(v)) - {v_}).pop()
            star_v__ = StarType.star_type(self.graph.v1_nei(v__))

            logging.debug(f'case 2: V has valency 2\tV\'\' = {v__}')

            if star_v__ == StarType.Segment:
                self._case_2a(g)

            else:
                self.T.extend([(g * G0).moe(Geodesic(V0, V1)),
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

        self.E.extend([s1, s2])
        self.involutions.append([s1, s2, g * G0 * g.inv()])

        logging.debug(f'case 1: V is univalent\nadded edges:\ns1 = {s1},\ns2 = {s2}')


    def _case_2a(self, g):
        s1_ = Geodesic(V1, ZERO)
        s2_ = Geodesic(V1, INF)

        gG0 = g * G0

        s1 = gG0.moe(s1_)
        s2 = gG0.moe(s2_)

        self.E.extend([s1, s2])
        self.T.append(gG0.moe(Geodesic(V0, V1)))
        self.involutions.append([s1, s2, gG0 * G1_2 * gG0.inv()])

        logging.debug(f'case 2a: Star V\'\' is a segment\nadded edges:\ns1 = {s1},\ns2 = {s2}')


    def _case_2b(self, v, g, v__, star_v__):
        self.T.extend([(g * G0).moe(Geodesic(V0, V1)),
                       (g * G_).moe(Geodesic(V0, V1)),
                       (g * G__).moe(Geodesic(V0, V1))
        ])

        if star_v__ == StarType.SlingShot:
            v1 = self.graph.cyc_next(v, self.graph.v1_nei(v__))
            v2 = self.graph.cyc_next(v1, self.graph.v1_nei(v__))

            logging.debug(f'case 2b: Star V\'\' is a sling shot,\nV1 = {v1},\nV2 = {v2}')

            for w in [v1, v2]:
                if self.visited[w]:
                    self._case_2b__(g, v__, w, v1)
                else:
                    self._case_2b_(g, v__, w, v1)


    def _case_2b_(self, g, v__, w, v1):
        self.I[w] = len(self.L0)
        self.L0.append(w)
        self.L1.append(v__)

        if w == v1:
            self.G.append(g * G_)
        else:
            self.G.append(g * G__)

        self.visited[w] = True
        logging.debug(f'case 2b\': W({w}) marked as \"unvisited\"')


    def _case_2b__(self, g, v__, w, v1):
        l = self.I[w]
        g_ = self.G[l]

        if w == v1:
            e = G_
        else:
            e = G__


        s0 = Geodesic(ZERO, INF)
        s1 = (g * e).moe(s0)
        s2 = g_.moe(s0)
        self.E.extend([s1, s2])
        self.involutions.append([s1, s2, g_ * G0 * (g*e).inv()])
        self.removed[self.L0[l]] = True
        logging.debug(f'case 2b\'\': W({w}) marked as \"visited\"\nadded edges:\ns1: {s1},\ns2 : {s2}')



    def _case_2c(self, g):
        s0 = Geodesic(ZERO, INF)
        g1 = g * G_
        g2 = g * G__
        s1 = g1.moe(s0)
        s2 = g2.moe(s0)
        self.E.extend([s1, s2])
        self.involutions.append([s1, s2, g2 * (g1 * G0).inv()])
        logging.debug(f'case 2c: Star V__ is a racket\nadded edges:\ns1 : {s1},\ns2 : {s2}')


    def unique(self, triple):
        for x in triple:
            if triple.count(x) == 1:
                return x

