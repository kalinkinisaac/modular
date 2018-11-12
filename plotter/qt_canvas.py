from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt
import os

graph_style_path = f'{os.getcwd()}/plotter/graph.mplstyle'
domain_style_path = f'{os.getcwd()}/plotter/domain.mplstyle'
# graph_style_path = '/Users/kalinkinisaac/PycharmProjects/modular/plotter/graph.mplstyle'
# domain_style_path = '/Users/kalinkinisaac/PycharmProjects/modular/plotter/domain.mplstyle'


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, style='ggplot', _full=False, *args, **kwargs):
        self._style = style

        with plt.style.context(self._style):
            self._fig = plt.Figure()

            super(__class__, self).__init__(self._fig)
            self.setParent(parent)

            if _full:
                self.ax = self.figure.add_axes([0,0,1,1])
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
