from PyQt5.QtCore import QThread, pyqtSignal, QObject

from .api import Api


class QtApi(QObject):
    def __init__(self, app):
        super(__class__, self).__init__()
        self.api = Api()
        self.app = app
        self.sub_calc_thread = None

    def construct_graph(self, *args, **kwargs):
        self.on_sub_calc(*args, **kwargs)

    def on_sub_calc(self, *args, **kwargs):
        if not self.sub_calc_thread:
            self.sub_calc_thread = SubgroupThread(
                self.api,
                self.app.graph_canvas,
                self.app.domain_canvas,
                *args, **kwargs
            )
            self.sub_calc_thread.statusMessage.connect(self.app.handle_status_message)
            self.sub_calc_thread.on_graph_plotted.connect(self.app.handle_graph_draw_finished)
            self.sub_calc_thread.on_domain_plotted.connect(self.app.handle_domain_draw_finished)
            self.sub_calc_thread.finished.connect(self.on_sub_calc_finished)
            self.sub_calc_thread.start()

    def on_sub_calc_finished(self):
        self.sub_calc_thread.statusMessage.disconnect(self.app.handle_status_message)
        self.sub_calc_thread.on_graph_plotted.disconnect(self.app.handle_graph_draw_finished)
        self.sub_calc_thread.on_domain_plotted.disconnect(self.app.handle_domain_draw_finished)
        self.sub_calc_thread.finished.disconnect(self.on_sub_calc_finished)
        self.sub_calc_thread = None


class SubgroupThread(QThread):
    statusMessage = pyqtSignal(object)
    on_graph_plotted = pyqtSignal()
    on_domain_plotted = pyqtSignal()

    def __init__(self, api: Api, graph_canvas, domain_canvas, *args, **kwargs):
        super(__class__, self).__init__()
        self.api = api
        self.graph_canvas = graph_canvas
        self.domain_canvas = domain_canvas
        self.args = args
        self.kwargs = kwargs
        # remove args

    def run(self):
        self.statusMessage.emit('Calculating subgroup data')
        self.api.set_subgroup(*self.args, **self.kwargs)

        self.statusMessage.emit('Calculating graph data')
        self.api.calc_graph()

        self.statusMessage.emit('Plotting graph')
        self.api.plot_graph_on_canvas(self.graph_canvas)
        self.on_graph_plotted.emit()

        self.statusMessage.emit('Calculating domain')
        self.api.calc_domain()

        self.statusMessage.emit('Plotting domain')
        self.api.plot_domain_on_canvas(self.domain_canvas)
        self.on_domain_plotted.emit()
        self.statusMessage.emit('Domain is plotted!')
