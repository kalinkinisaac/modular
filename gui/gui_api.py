from .subgroups_names import ClassicalSubgroups
from graph_constructor import get_graph
from graph_drawer import GraphCanvas
from special_polygon import get_all


class Api(object):

    def __init__(self):
        self._subgroup = None
        self._graph = None
        self._graph_canvas = None
        self._domain = None
        self._tree = None
        self._involutions = None
        self._generators = None

    def set_subgroup(self, subgroup: ClassicalSubgroups, n=2):
        self._subgroup = subgroup.to_class()(n)

    def calc_graph(self):
        if self._subgroup:
            self._graph = get_graph(self._subgroup)
        else:
            raise Exception('subgroup is not set')

    def plot_graph_canvas(self, parent):
        self._graph_canvas = GraphCanvas(parent=parent, graph=self._graph)

    def get_canvas(self):
        return self._graph_canvas

    def calc_domain(self):
        if self._graph:
            self._domain, self._tree, self._involutions = get_all(self._graph)
            self._generators = zip(*self._involutions)[2]
        else:
            raise Exception('graph is not set')