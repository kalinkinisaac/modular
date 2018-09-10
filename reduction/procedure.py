from fimath.geodesic import Geodesic, undirected_eq
from .sort import cyclic_sorted
from fimath import Matrix

class Decompositor(object):
    def __init__(self, polygon, involutions, z, w):
        self._poly = polygon
        self._cur_poly = []
        self.involutions = involutions
        self.line = Geodesic(w, z)
        self.decomposition = []
        self.mul_dec = Matrix()
        self.previous_edge = None
        self._involution_dict = None
        self.crossing = True

    def decompose(self):
        self.prepare_involutions()

        self._poly = cyclic_sorted(self._poly)
        self._cur_poly = self._poly[::]

        previous_edges = get_cross_edges(self._cur_poly, self.line)

        if len(previous_edges) != 1:
            raise Exception('Number of crossed edges is not equal to 1')

        self.previous_edge = previous_edges[0]


        while self.crossing:
            self.iteration()

        return self.decomposition

    def iteration(self):
        _g_i = self.get_involution(self.previous_edge).inv()
        g_i = self.mul_dec * _g_i * self.mul_dec.inv()

        self.decomposition.append(_g_i)
        self.mul_dec = g_i * self.mul_dec

        for i in range(len(self._cur_poly)):
            self._cur_poly[i] = g_i.moe(self._cur_poly[i])

        geo_drawer.draw(self._cur_poly, color='grey')

        crossed = get_cross_edges(self._cur_poly, self.line)
        crossed = list(filter(lambda e: not undirected_eq(e, self.previous_edge), crossed))

        if not crossed:
            self.crossing = False

        elif len(crossed) == 1:
            self.previous_edge = crossed[0]

        elif len(crossed) == 2:
            # Decision: which way should we go
            # Trying first
            first_poly = self._cur_poly[::]
            for i in range(len(first_poly)):
                first_poly[i] = g_i.moe(first_poly[i])
            _crossed = get_cross_edges(self._cur_poly, self.line)
            _crossed = list(filter(lambda e: not undirected_eq(e, crossed[0]), _crossed))

            if _crossed:
                self.previous_edge = crossed[0]
            else:
                self.previous_edge = crossed[1]

        else:
            raise Exception('there are more than 2 crossing edges')

    def prepare_involutions(self):
        self._involution_dict = dict()

        for a, b, g in self.involutions:
            self._involution_dict[a] = g
            self._involution_dict[b] = g.inv()

    def get_involution(self, edge):
        edge_ = self._poly[self._cur_poly.index(edge)]
        return self._involution_dict[edge_]

# O(n)
def get_cross_edges(polygon, line : Geodesic):
    edges = []
    for edge in polygon:
        if is_crossing(edge, line):
            edges.append(edge)
    return edges

# O(1)
def is_crossing(line1 : Geodesic, line2 : Geodesic):
    l1_is_vert = line1.is_vertical
    l2_is_vert = line2.is_vertical

    if l1_is_vert or l2_is_vert:

        if l2_is_vert:
            line1, line2 = line2, line1

        if l2_is_vert:
            return line1.vertical_x == line2.vertical_x and (line1.bot.imag <= line2.begin.imag <= line1.top.imag or
                                                                 line1.bot.imag <= line2.end.imag <= line1.top.imag)
        else:
            x_cross = line1.vertical_x
            if line2.left.real <= x_cross <= line2.right.real:
                sq_y = line2.sq_radius - (line2.center - x_cross) ** 2
                if line1.has_inf:
                    return line1.bot.imag ** 2 <= sq_y
                else:
                    return line1.bot.imag ** 2 <= sq_y <= line1.top.imag ** 2
            else:
                return False

    else:

        if line1.center == line2.center:
            return line1.sq_radius == line2.sq_radius

        x_cross = 0.5 * (line1.center + line2.center +
                             (line1.sq_radius - line2.sq_radius) / (line2.center - line1.center))

        if line1.left.real <= x_cross <= line1.right.real and line2.left.real <= x_cross <= line2.right.real:
            return True

        else:
            return False

