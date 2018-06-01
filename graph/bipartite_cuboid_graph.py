from .vertex_type import VertexType

class BipartiteCuboidGraph(object):

    def __init__(self, V0=[], V1=[], dist_edge=[0, 1, 0], correspond=dict(), sort_key=lambda x: x):
        self.V0 = V0
        self.V1 = V1
        self.v0, self.v1, self.dist_j = dist_edge

        self.__size = len(V0) + len(V1)

        self.correspond = correspond
        inv_correspond  = {v: k for k, v in self.correspond.items()}
        self.correspond.update(inv_correspond)

        self.__leaves = []
        self.__set_leaves()

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

    @property
    def size(self):
        return self.__size

    @property
    def leaves(self):
        return self.__leaves

    @property
    def V(self):
        return [(v, VertexType.Black) for v in range(len(self.V0))] + \
               [(v, VertexType.White) for v in range(len(self.V1))]

    def V0_neighbors(self, vertex):
        return self.V0[vertex]

    def V1_neighbors(self, vertex):
        return self.V1[vertex]

    def is_corresponded(self, vertex):
        return vertex in self.correspond

    def get_correspond(self, vertex):
        if self.is_corresponded(vertex):
            return self.correspond[vertex]
        else:
            return vertex

    def __set_leaves(self):
        for vertex in range(len(self.V0)):
            if len(self.V0[vertex]) == 1:
                self.__leaves.append([vertex, VertexType.Black])

        for vertex in range(len(self.V1)):
            if len(self.V1[vertex]) == 1:
                self.__leaves.append([vertex, VertexType.White])
