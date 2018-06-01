from graph import (BCGraph, VertexType)
from .star_type import StarType
import numpy as np
from numpy import linalg as LA
from constants import *
from .mobius_transform import geodesic_mt, mobius_transform as mt
from .algo import inv
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', filename='log.log',level=logging.INFO)

def int_round(x):
    return int(round(x))

int_round = np.vectorize(int_round)

class SpecialPolygon(object):

    def __init__(self, graph=BCGraph()):
        self.graph = graph

    def construct_polygon(self):
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

        neighbors = self.graph.V1_neighbors(self.v1)
        star_v1 = StarType.star_type(neighbors)

        self.T.append([V0, V1])

        if star_v1 == StarType.Segment:
            self.L0.append(self.v0)
            self.L1.append(self.v1)
            self.G.append(IDM)
            self.I.append(0)
            s1 = [V1, INF]
            s2 = [V1, ZERO]
            self.E.extend([s1, s2])
            self.involutions.append([s1, s2, G1])

        else:
            self.T.extend([geodesic_mt([V0, V1], G1),
                           geodesic_mt([V0, V1], G1_2)])
            self.generators.extend([G1, G1_2])
            if star_v1 == StarType.SlingShot:
                v_ = BCGraph.cyclic_next(self.v0, neighbors)
                v__ = BCGraph.cyclic_next(v_, neighbors)

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
                v = self.unique(neighbors)
                j = self.graph.dist_j
                self.L0.append(v)
                self.L1.append(self.v1)
                self.G.append(int_round(LA.matrix_power(G1, j)))
                self.I[v] = 0
                s = [[ZERO, INF], [ZERO, ONE], [ONE, INF]]
                self.E.extend([s[(j + 1) % 3], s[(j + 2) % 3]])
                # if j != 0:
                #     self.T.append(geodesic_mt([V0, V1], LA.matrix_power(G1, 3 - j)))
                self.involutions.append([s[(j + 1) % 3], s[(j + 2) % 3],
                                         int_round(LA.matrix_power(G1, j - 1)).dot(G_).dot(int_round(LA.matrix_power(G1, 1 - j)))])

        while(self.L0):
            self.induction()

        return self.E, self.T, self.involutions



    def induction(self):

        logging.info('New induction step starts\n\tL0 = {}\n\tL1 = {}\n\tG =\n{}'.format(
            str(self.L0),
            str(self.L1),
            '\n'.join(list(map(str, self.G)))))

        v = self.L0.pop()
        v_ = self.L1.pop()
        g = self.G.pop()

        logging.info('Popped \n\tV = {},\n\tV\' = {},\n\tg =\n{}\n\n'.format(str(v), str(v_), str(g)))

        if self.removed[v]:
            logging.info('V was marked \" to be removed\".\n\n==-End of induction-==\n\n')
            return

        if self.graph.is_V0_univalent(v):
            self._case_1(g)

        else:
            v__ = (set(self.graph.V0_neighbors(v)) - {v_}).pop()
            star_v__ = StarType.star_type(self.graph.V1_neighbors(v__))

            logging.info('2. V has valency 2.\n\tV\'\' = {},\n\tStar(V\'\') : {}\n'.format(str(v__), str(star_v__)))

            if star_v__ == StarType.Segment:
                self._case_2a(g)

            else:
                self.T.extend([geodesic_mt([V0, V1], g.dot(G0)),
                               geodesic_mt([V0, V1], g.dot(G_)),
                               geodesic_mt([V0, V1], g.dot(G__))])

                if star_v__ == StarType.SlingShot:
                    self._case_2b(v, g, v__, star_v__)

                elif star_v__ == StarType.Racket:
                    self._case_2c(g)

                else:
                    raise Exception('There is not such case')



    def _case_1(self, g):
        s1_ = [V0, ZERO]
        s2_ = [V0, INF]

        s1 = geodesic_mt(s1_, g)
        s2 = geodesic_mt(s2_, g)

        self.E.extend([s1, s2])
        self.involutions.append([s1, s2, g.dot(G0).dot(inv(g))])

        logging.info('1. V is univalent.\n\ts1 = {},\n\ts2 = {}\n\n==-End of induction-==\n\n'.format(str(s1), str(s2)))


    def _case_2a(self, g):
        s1_ = [V1, ZERO]
        s2_ = [V1, INF]

        gG0 = g.dot(G0)

        s1 = geodesic_mt(s1_, gG0)
        s2 = geodesic_mt(s2_, gG0)

        self.E.extend([s1, s2])
        self.T.append(geodesic_mt([V0, V1], gG0))
        self.involutions.append([s1, s2, gG0.dot(G1_2).dot(inv(gG0))])

        logging.info('2a. Star(V\'\') -- Segment,\n\ts1 = {},\n\ts2 = {}\n\n==-End of induction-==\n'.format(str(s1), str(s2)))


    def _case_2b(self, v, g, v__, star_v__):
        self.T.extend([geodesic_mt([V0, V1], g.dot(G0)),
                       geodesic_mt([V0, V1], g.dot(G_)),
                       geodesic_mt([V0, V1], g.dot(G__))])
        if star_v__ == StarType.SlingShot:
            v1 = self.graph.cyclic_next(v, self.graph.V1_neighbors(v__))
            v2 = self.graph.cyclic_next(v1, self.graph.V1_neighbors(v__))

            logging.info('2b. Star(V\'\') -- Sling Shot,\n\tV1 = {},\n\tV2 = {}\n'.format(str(v1), str(v2)))

            for w in [v1, v2]:
                if self.visited[w]:
                    self._case_2b__(g, v__, w, v1)
                else:
                    self._case_2b_(g, v__, w, v1)


            logging.info('==-End of induction-==\n\n')


    def _case_2b_(self, g, v__, w, v1):
        self.I[w] = len(self.L0)
        self.L0.append(w)
        self.L1.append(v__)

        if w == v1:
            self.G.append(g.dot(G_))
        else:
            self.G.append(g.dot(G__))

        self.visited[w] = True
        logging.info('2b\'. W({}) marked as \"unvisited\".\n'.format(str(w)))


    def _case_2b__(self, g, v__, w, v1):
        l = self.I[w]
        g_ = self.G[l]

        if w == v1:
            e = G_
        else:
            e = G__


        s0 = [ZERO, INF]
        s1 = geodesic_mt(s0, g.dot(e))
        s2 = geodesic_mt(s0, g_)
        self.E.extend([s1, s2])
        self.involutions.append([s1, s2, g_.dot(G0).dot(inv(g.dot(e)))])
        self.removed[self.L0[l]] = True
        logging.info('2b\'\'. W({}) marked as \"visited\".\n\ts1: {},\n\ts2 : {}\n'.format(str(w), str(s1), str(s2)))



    def _case_2c(self, g):
        s0 = [ZERO, INF]
        g1 = g.dot(G_)
        g2 = g.dot(G__)
        s1 = geodesic_mt(s0, g1)
        s2 = geodesic_mt(s0, g2)
        self.E.extend([s1, s2])
        self.involutions.append([s1, s2, g2.dot(inv(g1.dot(G0)))])

        logging.info('2c. Star(V__) : Racket\n\t s1 : {},\n\ts2 : {},\n\nEnd of induction\n\n'.format(str(s1), str(s2)))


    def unique(self, triple):
        for x in triple:
            if triple.count(x) == 1:
                return x

