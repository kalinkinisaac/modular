from PyQt5.QtCore import QThread, pyqtSignal, QObject

from .api import Api

class QtApi(QObject):
    def __init__(self, app):
        super(__class__, self).__init__()
        self.api = Api()
        self.app = app
        self.subgroup_set_thread = None
        self.graph_calc_thread = None
        self.graph_draw_thread = None

    def construct_graph(self, *args, **kwargs):
        self.on_subgroup_calc(*args, **kwargs)


    def on_subgroup_calc(self, *args, **kwargs):
        if not self.subgroup_set_thread:
            self.subgroup_set_thread = SubgroupThread(self.api, *args, **kwargs)
            self.subgroup_set_thread.statusMessage.connect(self.app.handle_status_message)
            self.subgroup_set_thread.finished.connect(self.on_subgroup_calc_finished)
            self.subgroup_set_thread.start()

    def on_subgroup_calc_finished(self):
        self.subgroup_set_thread.statusMessage.disconnect(self.app.handle_status_message)
        self.subgroup_set_thread.finished.disconnect(self.on_subgroup_calc_finished)
        self.subgroup_set_thread = None
        self.app.handle_graph_draw_finished()
        self.app.handle_domain_draw_finished()



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

        self.statusMessage.emit('Calculating graph data')
        self.api.calc_graph()

        self.statusMessage.emit('Plotting graph')
        self.api.plot_graph_on_canvas(*self.args, **self.kwargs)

        self.statusMessage.emit('Calculating domain')
        self.api.calc_domain()

        self.statusMessage.emit('Plotting domain')
        self.api.plot_domain_on_canvas(*self.args, **self.kwargs)
