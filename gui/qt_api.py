from PyQt5.QtCore import QThread, pyqtSignal, QObject

from api import Api


class QtApi(QObject):
    def __init__(self, handleStatusMessage, handleChewed, handleDigested):
        super(__class__, self).__init__()
        self.api = Api()
        self.digestionThread = None
        self._handle_status_message = handleStatusMessage
        self._handle_chewed = handleChewed
        self._handle_digested = handleDigested

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
