from api.subgroups_names import ClassicalSubgroups
from graph_constructor import get_graph
from plotter.graph_plotter import GraphPlotter
from plotter.geodesic_plotter import GeodesicPlotter
from plotter.marker_plotter import MarkerPlotter
from special_polygon import SpecialPolygon
from fimath import Matrix, Field
from reduction import Decomposer
from .error import ApiError, FormatError, ValueRangeError


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
        self._marker_plotter = None

    def set_subgroup(self, subgroup: ClassicalSubgroups, n=2):
        if type(n) is not int:
            if n == '':
                raise FormatError('Field N should be filled')
            try:
                n = int(n)
            except ValueError:
                raise TypeError('N should be int')

        if n <= 1:
            raise ValueRangeError('N should be greater than 1')

        self._subgroup = subgroup.to_class()(n)

    def calc_graph(self):
        if self._subgroup:
            self._graph = get_graph(self._subgroup)
        else:
            raise Exception('subgroup is not set.')

    def plot_graph_on_axes(self, axes):
        if not self._graph:
            raise ApiError('graph is not calculated')
        gd = GraphPlotter(axes)
        gd.plot(self._graph)

    def plot_graph_on_bokeh(self, fig):
        if not self._graph:
            raise ApiError('graph is not calculated')
        gd = GraphPlotter(bokeh_fig=fig)
        gd.plot(self._graph)

    def calc_domain(self):
        if self._graph:
            sp = SpecialPolygon(self._graph)
            try:
                sp.construct_polygon()
            except Exception as e:
                raise ApiError(f'unexpected error during constructing polygon: {e}')
            self._domain = sp.edges
            self._tree = sp.tree
            self._involutions = sp.involutions
            self._white_markers = sp.white_vertices
            self._black_markers = sp.black_vertices
            self._cut_markers = sp.cut_vertices
            self._generators = list(zip(*self._involutions))[2]
        else:
            raise ApiError('graph is not set.')

    @property
    def markers(self):
        return [self._white_markers, self._black_markers, self._cut_markers]

    def plot_domain_on_axes(self, axes, markers=False):
        gp = GeodesicPlotter(ax=axes)
        gp.plot(self._domain)
        gp.plot(self._tree, color='r', alpha=0.8, linewidth=0.75, linestyle='--')
        if markers:
            _marker_plotter = MarkerPlotter(axes)
            try:
                _marker_plotter.plot(self._white_markers, self._black_markers, self._cut_markers)
            except Exception:
                raise ApiError('unexpected error.')

    def plot_domain_on_bokeh(self, fig, markers=True):
        gp = GeodesicPlotter(bokeh_fig=fig)
        gp.plot(self._domain)
        gp.plot(self._tree, color='red', alpha=0.8, line_width=0.75, dashed=True)
        if markers:
            _marker_plotter = MarkerPlotter(bokeh_fig=fig)
            _marker_plotter.plot(self._white_markers, self._black_markers, self._cut_markers)
            # try:
            #     _marker_plotter.plot(self._white_markers, self._black_markers, self._cut_markers)
            # except Exception:
            #     raise ApiError('unexpected error.')

    def change_markers_state(self):
        if self._marker_plotter:
            self._marker_plotter.change_visible()

    def get_generators_str(self):
        return Matrix.beautify(self._generators)

    def decompose_matrix(self, matrix_str):
        try:
            matrix = Matrix.from_str(matrix_str)
        except Exception:
            raise FormatError('Matrix should be in following format: a, b, c, d')

        z = Field(0.5+1.5j)
        w = matrix.moe(z)
        decomposer = Decomposer(polygon=self._domain, involutions=self._involutions, z=z, w=w)

        try:
            self._decomposition = decomposer.decompose()
        except Exception:
            raise ApiError('Matrix does not belong to subgroup or another unexpected error occurred.')

    def get_decomposition(self):
        return Matrix.beautify(self._decomposition)
