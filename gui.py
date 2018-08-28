import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib

import random


class App(QMainWindow):

    def __init__(self):
        super(__class__, self).__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.title = 'Modular'
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()

        self.grid.addWidget(self.create_gamma_section(), 0, 0)




        self.grid.addWidget(self.create_graph_section(), 1, 0)
        # self.grid.addWidget(self.create_domain_section(), 0, 2)
        # self.grid.addWidget(self.create_generators_section(), 0, 3)

        widget = QWidget()
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def create_gamma_section(self):
        groupBox = QGroupBox("Subgroup selection")


        lbl = QLabel('Choose subgroup: ')
        lbl.setFixedSize(lbl.sizeHint())

        combo = QComboBox()
        combo.addItems(['Gamma', 'Gamma_0', 'Gamma^0', 'Gamma_1', 'Gamma^1'])
        combo.setFixedSize(combo.sizeHint())

        lbl2 = QLabel('Type N: ')
        lbl2.setFixedSize(lbl2.sizeHint())

        line_edit = QLineEdit()
        line_edit.setFixedWidth(40)

        button = QPushButton('Construct graph')
        button.setFixedSize(button.sizeHint())
        button.clicked.connect(self.on_construct_graph_button_clicked)

        hbox = QHBoxLayout()

        hbox.addWidget(lbl)
        hbox.addWidget(combo)
        hbox.addWidget(lbl2)
        hbox.addWidget(line_edit)
        hbox.addWidget(button)
        hbox.addStretch()

        groupBox.setLayout(hbox)

        return groupBox

    def create_graph_section(self):
        groupBox = QGroupBox("Graph visualization")

        hbox = QHBoxLayout()
        hbox.addStretch()

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas = PlotCanvas()
        # self.toolbar = NavigationToolbar(self.canvas, self)
        hbox.addWidget(self.canvas, Qt.AlignLeft)
        groupBox.setLayout(hbox)
        return groupBox

    def create_domain_section(self):
        pass

    def create_generators_section(self):
        pass


    def on_construct_graph_button_clicked(self):
        QCoreApplication.quit()

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)

        super(__class__, self).__init__(fig)
        self.setParent(parent)
        #
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())