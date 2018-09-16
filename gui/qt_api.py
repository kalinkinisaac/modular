from PyQt5.QtCore import QThread, pyqtSignal, QObject

from api import Api


class QtApi(QObject):
    def __init__(self, handleStatusMessage, handleChewed, handleDigested, handleDecomposed):
        super(__class__, self).__init__()
        self.api = Api()
        self.digestionThread = None
        self._handle_status_message = handleStatusMessage
        self._handle_chewed = handleChewed
        self._handle_digested = handleDigested
        self._handle_decomposed = handleDecomposed

    def digest(self, *args, **kwargs):
        self._on_eat(*args, **kwargs)

    def _on_eat(self, *args, **kwargs):
        if not self.digestionThread:
            self.digestionThread = DigestionThread(api=self.api, *args, **kwargs)

            self.digestionThread.statusMessage.connect(self._handle_status_message)
            self.digestionThread.onChewed.connect(self._handle_chewed)
            self.digestionThread.onDigested.connect(self._handle_digested)
            self.digestionThread.finished.connect(self._on_digested)
            self.digestionThread.start()

    def _on_digested(self):
        self.digestionThread.statusMessage.disconnect(self._handle_status_message)
        self.digestionThread.onChewed.disconnect(self._handle_chewed)
        self.digestionThread.onDigested.disconnect(self._handle_digested)
        self.digestionThread.finished.disconnect(self._on_digested)
        self.digestionThread = None

    def decompose(self, matrix):
        self._on_decompose(matrix)

    def _on_decompose(self, matrix_str):
        if not self.digestionThread:
            self.decompositionThread = DecompositionThread(api=self.api, matrix_str=matrix_str)
            self.decompositionThread.statusMessage.connect(self._handle_status_message)
            self.decompositionThread.onDecomposed.connect(self._handle_decomposed)
            self.decompositionThread.finished.connect(self._on_decomposed)
            self.decompositionThread.start()

    def _on_decomposed(self):
        self.decompositionThread.statusMessage.disconnect(self._handle_status_message)
        self.decompositionThread.onDecomposed.disconnect(self._handle_decomposed)
        self.decompositionThread.finished.disconnect(self._on_decomposed)
        self.decompositionThread = None

class DigestionThread(QThread):
    statusMessage = pyqtSignal(object)
    onChewed = pyqtSignal()
    onDigested = pyqtSignal(str)

    def __init__(self, api: Api, subgroup, n, graph_canvas, domain_canvas):
        super(__class__, self).__init__()
        self.api = api
        self.subgroup = subgroup
        self.n = n
        self.graph_canvas = graph_canvas
        self.domain_canvas = domain_canvas

    def run(self):
        self.statusMessage.emit('Calculating subgroup data')
        self.api.set_subgroup(self.subgroup, self.n)

        self.statusMessage.emit('Calculating graph data')
        self.api.calc_graph()

        self.statusMessage.emit('Plotting graph')
        self.api.plot_graph_on_canvas(self.graph_canvas)
        self.onChewed.emit()

        self.statusMessage.emit('Calculating domain')
        self.api.calc_domain()

        self.statusMessage.emit('Plotting domain')
        self.api.plot_domain_on_canvas(self.domain_canvas)
        self.onDigested.emit(self.api.get_generators_str())


class DecompositionThread(QThread):
    statusMessage = pyqtSignal(object)
    onDecomposed = pyqtSignal(str)

    def __init__(self, api: Api, matrix_str):
        super(__class__, self).__init__()
        self.api = api
        self.matrix_str = matrix_str

    def run(self):
        self.statusMessage.emit('Decomposing matrix')
        try:
            self.api.decompose_matrix(self.matrix_str)
            self.statusMessage.emit('Decomposed successfully')
            self.onDecomposed.emit(self.api.get_decomposition())
        except ValueError:
            self.statusMessage.emit('You should write matrix in following format: a,b,c,d')

