from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


graph_style_path = resource_path('plotter/graph.mplstyle')
domain_style_path = resource_path('plotter/domain.mplstyle')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, style='ggplot', _full=False, *args, **kwargs):
        self._style = 'ggplot'

        with plt.style.context(self._style):
            self._fig = plt.Figure()

            super(__class__, self).__init__(self._fig)
            self.setParent(parent)
            self.figure.set_tight_layout(False)
            if _full:
                self.ax = self.figure.add_axes([0, 0, 1, 1])
            else:
                self.ax = self.figure.add_subplot(111)
            self.ax.set_aspect('equal')
            self.config()

            FigureCanvasQTAgg.setSizePolicy(self,
                                            QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)

    def cla(self):
        with plt.style.context(self._style):
            self.ax.clear()
            self.config()


    def config(self):
        pass


class GraphCanvas(MplCanvas):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(style=graph_style_path, *args, **kwargs)
        # super(__class__, self).__init__(style='ggplot', *args, **kwargs)

    def config(self):
        # self.ax.axis('off')
        pass


class DomainCanvas(MplCanvas):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(style=domain_style_path, *args, **kwargs)


class MplCanvas2(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)

        # We want the axes cleared every time plot() is called
#        self.axes.hold(False)

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def update_plot(self, axes):
        self.axes = axes
        self.draw()
