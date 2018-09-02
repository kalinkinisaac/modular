from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, style=f'{os.getcwd()}/plotter/graph.mplstyle', *args, **kwargs):
        with plt.style.context(style):
            self.fig = plt.Figure()

            super(__class__, self).__init__(self.fig)
            self.setParent(parent)

            self.ax = self.figure.add_subplot(111)
            self.ax.set_aspect('equal')


            FigureCanvasQTAgg.setSizePolicy(self,
                                            QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)

    def cla(self):
        self.ax.clear()

    def plot(self):
        raise NotImplementedError


# class MplCanvas(PlotCanvas):
#     def __init__(self, parent=None, fig_config=None, ax_config=None):
#         super(__class__, self).__init__(parent=parent, **fig_config)
#         self.ax = self.figure.add_subplot(111)
#         self._ax_config = ax_config
#         self._ax_config(self.ax)
#
#
#     def cla(self):
#         self.ax.clear()
#         self._ax_config(self.ax)