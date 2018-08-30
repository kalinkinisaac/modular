from PyQt5.QtCore import QThread, pyqtSignal

from .gui_api import Api

class QtApi(object):
    def __init__(self, app):
        self.api = Api()
        self.app = app
        # self.handle_status_message = handle_status_message
        self.subgroup_set_thread = None
        self.graph_calc_thread = None
        self.graph_draw_thread = None

    def construct_graph(self, *args, **kwargs):
        self.on_set_subgroup(*args, **kwargs)


    def on_set_subgroup(self, *args, **kwargs):
        if not self.subgroup_set_thread:
            self.subgroup_set_thread = SubgroupThread(self.api, *args, **kwargs)
            self.subgroup_set_thread.statusMessage.connect(self.app.handle_status_message)
            self.subgroup_set_thread.finished.connect(self.on_set_subgroup_finished)
            self.subgroup_set_thread.start()

    def on_set_subgroup_finished(self):
        self.subgroup_set_thread.statusMessage.disconnect(self.app.handle_status_message)
        self.subgroup_set_thread.finished.disconnect(self.on_set_subgroup_finished)
        self.subgroup_set_thread = None

        self.on_calc_graph()

    def on_calc_graph(self):
        if not self.graph_calc_thread:
            self.graph_calc_thread = GraphCalcThread(self.api)
            self.graph_calc_thread.statusMessage.connect(self.app.handle_status_message)
            self.graph_calc_thread.finished.connect(self.on_calc_graph_finished)
            self.graph_calc_thread.start()

    def on_calc_graph_finished(self):
        self.graph_calc_thread.statusMessage.disconnect(self.app.handle_status_message)
        self.graph_calc_thread.finished.disconnect(self.on_calc_graph_finished)
        self.graph_calc_thread = None

        self.on_graph_draw()

    def on_graph_draw(self):
        if not self.graph_draw_thread:
            self.graph_draw_thread = GraphDrawThread(self.api, parent=self.app)
            self.graph_draw_thread.statusMessage.connect(self.app.handle_status_message)
            self.graph_draw_thread.finished.connect(self.on_graph_draw_finished)
            self.graph_draw_thread.start()

    def on_graph_draw_finished(self):
        self.graph_draw_thread.statusMessage.disconnect(self.app.handle_status_message)
        self.graph_draw_thread.finished.disconnect(self.on_graph_draw_finished)
        self.app.handle_graph_draw_finished(self.api.get_canvas())
        self.graph_draw_thread = None


class SubgroupThread(QThread):
    statusMessage = pyqtSignal(object)

    def __init__(self, api: Api, *args, **kwargs):
        super(__class__, self).__init__()
        self.api = api
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.statusMessage.emit('Calculating subgroup data')
        self.api.set_subgroup(*self.args, **self.kwargs)

class GraphCalcThread(QThread):
    statusMessage = pyqtSignal(object)

    def __init__(self, api: Api):
        super(__class__, self).__init__()
        self.api = api

    def run(self):
        self.statusMessage.emit('Calculating graph data')
        self.api.calc_graph()

class GraphDrawThread(QThread):
    statusMessage = pyqtSignal(object)

    def __init__(self, api: Api, *args, **kwargs):
        super(__class__, self).__init__()
        self.api = api
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.statusMessage.emit('Plotting graph')
        self.api.plot_graph_canvas(*self.args, **self.kwargs)