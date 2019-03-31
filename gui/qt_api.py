from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from matplotlib.axes import Axes
from api import Api, ApiError, ClassicalSubgroups


def error_handled(func):
    def wrapped(*args, **kwargs):
        self = args[0]
        if self.terminated:
            return
        try:
            func(*args, **kwargs)
        except ApiError as e:
            self.update_status_message(f'Api error: {e}')
            self.soft_terminate()
    return wrapped


class QtApi(QObject):
    handle_status_message = pyqtSignal(str, int)
    handle_graph_axes = pyqtSignal(Axes)
    handle_domain_axes = pyqtSignal(Axes)
    handle_generators = pyqtSignal(str)
    handle_decomposition = pyqtSignal(str)
    handle_markers_state_plotted = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(__class__, self).__init__()
        self._api = Api()
        self.terminated = False

    def soft_terminate(self):
        self.terminated = True

    def update_status_message(self, status_message, cooldown_time=0):
        self.handle_status_message.emit(status_message, cooldown_time)

    @pyqtSlot(ClassicalSubgroups, str, Axes, Axes, name='onDigest')
    def on_digest(self, subgroup, n, graph_axes, domain_axes):
        self.terminated = False
        self._digest(subgroup, n)
        self._calc_graph()
        self._plot_graph(graph_axes)
        self._calc_domain()
        self._plot_domain(domain_axes)
        self._show_generators()

    @pyqtSlot(str, name='onDecompose')
    def on_decompose(self, matrix: str):
        self.terminated = False
        self._decompose(matrix)

    @error_handled
    def _digest(self, subgroup, n):
        self.update_status_message('Calculating subgroup data...')
        self._api.set_subgroup(subgroup, n)

    @error_handled
    def _calc_graph(self):
        self.update_status_message('Calculating graph data...')
        self._api.calc_graph()

    @error_handled
    def _plot_graph(self, graph_axes):
        self._api.plot_graph_on_axes(graph_axes)
        self.handle_graph_axes.emit(graph_axes)
        self.update_status_message('Graph is plotted!', 3000)

    @error_handled
    def _calc_domain(self):
        self.update_status_message('Calculating domain...')
        self._api.calc_domain()

    @error_handled
    def _plot_domain(self, domain_axes):
        self._api.plot_domain_on_axes(domain_axes, _markers=False)
        self.handle_domain_axes.emit(domain_axes)
        self.update_status_message('Domain is plotted!', 3000)

    @error_handled
    def _show_generators(self):
        self.handle_generators.emit(self._api.get_generators_str())

    @error_handled
    def _decompose(self, matrix):
        self.update_status_message('Decomposing matrix...')
        self._api.decompose_matrix(matrix)
        self.handle_decomposition.emit(self._api.get_decomposition())
        self.update_status_message('Matrix is decomposed!', 3000)

    @pyqtSlot(name='onMarkersStateChanged')
    @error_handled
    def on_markers_state_changed(self):
        self._api.change_markers_state()
        self.handle_markers_state_plotted.emit()

