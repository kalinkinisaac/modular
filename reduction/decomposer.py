from fimath.geodesic import Geodesic, undirected_eq
from fimath import Matrix
from .sort import cyclic_sorted


class Decomposer(object):
    def __init__(self, polygon, involutions, z, w):
        self._poly = polygon
        self._cur_poly = []
        self._involutions = involutions
        self._w = w
        self._z = z
        self._line = None
        self._decomposition = []
        self._mul_dec = Matrix()
        self._previous_edge = None
        self._involution_dict = None
        self._crossing = True

    def decompose(self):
        if self._w == self._z:
            return [Matrix(1, 0, 0, 1)]

        self._line = Geodesic(self._w, self._z)

        self.prepare_involutions()

        self._poly = cyclic_sorted(self._poly)
        self._cur_poly = self._poly[::]

        previous_edges = get_cross_edges(self._cur_poly, self._line)

        if len(previous_edges) != 1:
            raise Exception('Number of crossed edges is not equal to 1')

        self._previous_edge = previous_edges[0]

        while self._crossing:
            self._iteration()

        return self._decomposition

    def _iteration(self):
        _g_i = self._get_involution(self._previous_edge).inv()
        g_i = self._mul_dec * _g_i * self._mul_dec.inv()

        self._decomposition.append(_g_i)
        self._mul_dec = g_i * self._mul_dec

        for i in range(len(self._cur_poly)):
            self._cur_poly[i] = g_i.moe(self._cur_poly[i])

        # geo_drawer.draw(self._cur_poly, color='grey')

        crossed = get_cross_edges(self._cur_poly, self._line)
        crossed = list(filter(lambda e: not undirected_eq(e, self._previous_edge), crossed))

        if not crossed:
            self._crossing = False

        elif len(crossed) == 1:
            self._previous_edge = crossed[0]

        elif len(crossed) == 2:
            # Decision: which way should we go
            # Trying first
            first_poly = self._cur_poly[::]
            for i in range(len(first_poly)):
                first_poly[i] = g_i.moe(first_poly[i])
            _crossed = get_cross_edges(self._cur_poly, self._line)
            _crossed = list(filter(lambda e: not undirected_eq(e, crossed[0]), _crossed))

            if _crossed:
                self._previous_edge = crossed[0]
            else:
                self._previous_edge = crossed[1]

        else:
            raise Exception('there are more than 2 crossing edges')

    def prepare_involutions(self):
        self._involution_dict = dict()

        for a, b, g in self._involutions:
            self._involution_dict[a] = g
            self._involution_dict[b] = g.inv()

    def _get_involution(self, edge):
        edge_ = self._poly[self._cur_poly.index(edge)]
        return self._involution_dict[edge_]


# O(n)
def get_cross_edges(polygon, line: Geodesic):
    edges = []
    for edge in polygon:
        if is_crossing(edge, line):
            edges.append(edge)
    return edges


# O(1)
def is_crossing(line1: Geodesic, line2: Geodesic):
    if line1.is_vertical or line2.is_vertical:

        if line2.is_vertical:
            line1, line2 = line2, line1

        if line2.is_vertical:
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

        x_cross = 0.5 * (line1.center +
                         line2.center + (line1.sq_radius - line2.sq_radius) / (line2.center - line1.center))

        if line1.left.real <= x_cross <= line1.right.real and line2.left.real <= x_cross <= line2.right.real:
            return True

        else:
            return False
