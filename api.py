from subgroups_names import ClassicalSubgroups
from graph_constructor import get_graph
from plotter.graph_plotter import GraphPlotter
from plotter.geodesic_plotter import GeodesicPlotter
from special_polygon import get_all
from fimath import Matrix

class Api(object):

    def __init__(self):
        self._subgroup = None
        self._graph = None
        self._domain = None
        self._tree = None
        self._involutions = None
        self._generators = None

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
        gd.draw(self._graph)

    def calc_domain(self, *args, **kwargs):
        if self._graph:
            self._domain, self._tree, self._involutions = get_all(self._graph)
            self._generators = list(zip(*self._involutions))[2]
        else:
            raise Exception('graph is not set')

    def plot_domain_on_canvas(self, canvas, *args, **kwargs):
        canvas.cla()
        geo_drawer = GeodesicPlotter(canvas.ax)
        geo_drawer.draw(self._domain)

    def get_generators_str(self):
        return Matrix.beautify(self._generators)
