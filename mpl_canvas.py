from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


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
    def __init__(self, parent=None, fig_config=None, ax_config=None):
        super(__class__, self).__init__(parent=parent, **fig_config)
        self.ax = self.figure.add_subplot(111)
        self._ax_config = ax_config
        self._ax_config(self.ax)


    def cla(self):
        self.ax.clear()
        self._ax_config(self.ax)