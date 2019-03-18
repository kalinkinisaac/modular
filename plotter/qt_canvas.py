import os
import sys
import matplotlib.pyplot as plt

from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS')
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


graph_style_path = resource_path('plotter/graph.mplstyle')
domain_style_path = resource_path('plotter/domain.mplstyle')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, style='fast'):
        with plt.style.context(style):
            fig = Figure()
            super(__class__, self).__init__(fig)

            self._style = style

            self.delayEnabled = False
            self.delayTimeout = 100

            self._resizeTimer = QtCore.QTimer(self)
            self._resizeTimer.timeout.connect(self._delayedUpdate)

            self.axes = self.figure.add_subplot(111)
            self.figure.set_tight_layout(False)
            self.axes.set_aspect('equal')

            FigureCanvasQTAgg.__init__(self, self.figure)
            self.setParent(parent)

            FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
            FigureCanvasQTAgg.updateGeometry(self)

    def cla(self):
        with plt.style.context(self._style):
            self.axes.clear()

    def update_plot(self, axes):
        self.axes = axes
        self.draw()

    def resizeEvent(self, event):
        if self.delayEnabled:
            self._resizeTimer.start(self.delayTimeout)
            self.setUpdatesEnabled(False)

        super(__class__, self).resizeEvent(event)

    def _delayedUpdate(self):
        self._resizeTimer.stop()
        self.setUpdatesEnabled(True)


class GraphCanvas(MplCanvas):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(style=graph_style_path, *args, **kwargs)


class DomainCanvas(MplCanvas):

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(style=domain_style_path, *args, **kwargs)


