from subgroups_names import ClassicalSubgroups
from graph_constructor import get_graph
from plotter.graph_plotter import GraphPlotter
from plotter.geodesic_plotter import GeodesicPlotter
from plotter.marker_potter import MarkerPlotter
from special_polygon import SpecialPolygon
from fimath import Matrix, Field
from reduction import Decomposer

class Api(object):

    def __init__(self):
        self._subgroup = None
        self._graph = None
        self._domain = None
        self._tree = None
        self._involutions = None
        self._generators = None
        self._white_markers = None
        self._black_markers = None
        self._cut_markers = None
        self._decomposition = None

    def set_subgroup(self, subgroup: ClassicalSubgroups, n=2, *args, **kwargs):
        self._subgroup = subgroup.to_class()(n)

    def calc_graph(self, *args, **kwargs):
        if self._subgroup:
            self._graph = get_graph(self._subgroup)
        else:
            raise Exception('subgroup is not set')

    def plot_graph_on_canvas(self, canvas, *args, **kwargs):
        canvas.cla()
        gd = GraphPlotter(canvas.ax)
        gd.plot(self._graph)

    def calc_domain(self, *args, **kwargs):
        if self._graph:
            sp = SpecialPolygon(self._graph)
            sp.construct_polygon()
            self._domain = sp.edges
            self._tree = sp.tree
            self._involutions = sp.involutions
            self._white_markers = sp.white_vertices
            self._black_markers = sp.black_vertices
            self._cut_markers = sp.cut_vertices
            self._generators = list(zip(*self._involutions))[2]
        else:
            raise Exception('graph is not set')

    def plot_domain_on_canvas(self, canvas, *args, **kwargs):
        canvas.cla()
        geo_drawer = GeodesicPlotter(canvas.ax)
        geo_drawer.plot(self._domain)
        geo_drawer.plot(self._tree, color='r', alpha=0.8, linewidth=0.75, linestyle='--')
        mp = MarkerPlotter(canvas.ax)
        mp.plot(self._white_markers, self._black_markers, self._cut_markers)

    def get_generators_str(self):
        return Matrix.beautify(self._generators)

    def decompose_matrix(self, matrix_str):
        matrix = Matrix(matrix_str)
        z = Field(0.5+1.5j)
        w = matrix.moe(z)
        decomposer = Decomposer(polygon=self._domain, involutions=self._involutions, z=z, w=w)
        self._decomposition = decomposer.decompose()

    def get_decomposition(self):
        return Matrix.beautify(self._decomposition)
