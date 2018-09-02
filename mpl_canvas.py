from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

from graph_drawer import fig_config, ax_config


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, *args, **kwargs):

        super(__class__, self).__init__(Figure(*args, **kwargs))

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)

    def plot(self):
        raise NotImplementedError


class MplCanvas(PlotCanvas):
    def __init__(self, parent=None, graph=None):
        super(__class__, self).__init__(parent=parent, **fig_config)
        self._graph = graph
        self.ax = self.figure.add_subplot(111)
        ax_config(self.ax)


    def cla(self):
        self.ax.clear()
        ax_config(self.ax)