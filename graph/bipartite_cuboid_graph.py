from .vertex_type import VertexType

class BipartiteCuboidGraph(object):

    def __init__(self, V0=[], V1=[], dist_edge=[0, 1, 0], sort_key=lambda x: x):
        self.V0 = V0
        self.V1 = V1
        self.v0, self.v1, self.dist_j = dist_edge

        self.__size = len(V0) + len(V1)

    @property
    def size(self):
        return self.__size

    @staticmethod
    def cyclic_next(vertex, order):
        if vertex == order[0]:
            return order[1]
        elif vertex == order[1]:
            return order[2]
        else:
            return order[0]


    def is_V0_univalent(self, v):
        return len(self.V0_neighbors(v)) == 1

    def V0_neighbors(self, vertex):
        return self.V0[vertex]

    def V1_neighbors(self, vertex):
        return self.V1[vertex]

