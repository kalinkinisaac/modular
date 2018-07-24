class BipartiteCuboidGraph(object):

    def __init__(self, V0=[], V1=[], dist_edge=(0, 1, 0)):
        self.V0 = V0
        self.V1 = V1
        self.v0, self.v1, self.dist_j = dist_edge

        self.__size = len(V0) + len(V1)

    @property
    def size(self):
        return self.__size

    @staticmethod
    def cyc_next(vertex, order):
        if vertex == order[0]:
            return order[1]
        elif vertex == order[1]:
            return order[2]
        else:
            return order[0]


    def is_v0_uni(self, v):
        return len(self.v0_nei(v)) == 1

    def v0_nei(self, vertex):
        return self.V0[vertex]

    def v1_nei(self, vertex):
        return self.V1[vertex]

