from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from matplotlib.axes import Axes
from api import Api, ApiError, ClassicalSubgroups


class QtApi(QObject):
    handle_graph_axes = pyqtSignal(Axes)
    handle_domain_axes = pyqtSignal(Axes)
    handle_generators = pyqtSignal(str)
    handle_decomposition = pyqtSignal(str)
    handle_status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super(__class__, self).__init__()
        self._api = Api()
        self.terminated = False

    @pyqtSlot(ClassicalSubgroups, str, Axes, Axes, name='onDigest')
    def on_digest(self, subgroup, n, graph_axes, domain_axes):
        self._digest(subgroup, n)
        self._calc_graph()
        self._plot_graph(graph_axes)
        self._calc_domain()
        self._plot_domain(domain_axes)
        self._show_generators()
        # self.terminated = True
        # self.finished.emit()

    def _digest(self, subgroup, n):
        if self.terminated:
            return

        self.handle_status.emit('Calculating subgroup data')
        try:
            self._api.set_subgroup(subgroup, n)
        except ApiError as e:
            self.handle_status.emit(f'Api error: {e}')
            return
        except Exception as e:
            self.handle_status.emit(f'Unexpected error: {e}')
            return

    def _calc_graph(self):
        if self.terminated:
            return

        self.handle_status.emit('Calculating graph data')

        try:
            self._api.calc_graph()
        except Exception as e:
            self.handle_status.emit(f'Unexpected error: {e}')
            return

    def _plot_graph(self, graph_axes):
        if self.terminated:
            return

        self._api.plot_graph_on_axes(graph_axes)
        self.handle_graph_axes.emit(graph_axes)

    def _calc_domain(self):
        if self.terminated:
            return
        self._api.calc_domain()

    def _plot_domain(self, domain_axes):
        if self.terminated:
            return

        self._api.plot_domain_on_axes(domain_axes, _markers=False)
        self.handle_domain_axes.emit(domain_axes)

    def _show_generators(self):
        self.handle_generators.emit(self._api.get_generators_str())






