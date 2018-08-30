from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, *args, **kwargs):

        super(__class__, self).__init__(Figure( *args, **kwargs))

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)



    def plot(self):
        raise NotImplementedError