from .qt_api import QtApi
from .subgroups_names import ClassicalSubgroups

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

from plotter.qt_canvas import MplCanvas


class App(QMainWindow):

    def __init__(self):
        super(__class__, self).__init__()
        self.api = QtApi(self)
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.title = 'Modular'
        self.statusBar = QStatusBar()
        self.subgroups_combo = None
        self.graph_canvas = MplCanvas(parent=self)
        self.domain_canvas = MplCanvas(parent=self)
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()

        self.grid.addWidget(self.create_gamma_section(), 0, 0)

        self.grid.addWidget(self.create_graph_section(), 1, 0)
        self.grid.addWidget(self.create_domain_section(), 2, 0)
        # self.grid.addWidget(self.create_generators_section(), 0, 3)

        widget = QWidget()
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)


        self.setStatusBar(self.statusBar)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def create_gamma_section(self):
        groupBox = QGroupBox("Subgroup selection")


        lbl = QLabel('Choose subgroup: ')
        lbl.setFixedSize(lbl.sizeHint())

        self.subgroups_combo = QComboBox()
        self.subgroups_combo.addItems(ClassicalSubgroups.get_all_names())
        self.subgroups_combo.setFixedSize(self.subgroups_combo.sizeHint())

        lbl2 = QLabel('Type N: ')
        lbl2.setFixedSize(lbl2.sizeHint())

        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(40)

        button = QPushButton('Construct graph')
        button.setFixedSize(button.sizeHint())
        button.clicked.connect(self.on_construct_graph_button_clicked)

        hbox = QHBoxLayout()

        hbox.addWidget(lbl)
        hbox.addWidget(self.subgroups_combo)
        hbox.addWidget(lbl2)
        hbox.addWidget(self.line_edit)
        hbox.addWidget(button)
        hbox.addStretch()

        groupBox.setLayout(hbox)

        return groupBox

    def create_graph_section(self):
        groupBox = QGroupBox("Graph visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()

        toolbar = NavigationToolbar(self.graph_canvas, self)

        vbox.addWidget(self.graph_canvas, Qt.AlignLeft)
        vbox.addWidget(toolbar, Qt.AlignLeft)

        groupBox.setLayout(vbox)

        return groupBox

    def create_domain_section(self):
        groupBox = QGroupBox("Domain and tree visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()

        toolbar = NavigationToolbar(self.domain_canvas, self)

        vbox.addWidget(self.domain_canvas, Qt.AlignLeft)
        vbox.addWidget(toolbar, Qt.AlignLeft)

        groupBox.setLayout(vbox)

        return groupBox

    def create_generators_section(self):
        pass

    def on_construct_graph_button_clicked(self):
        self.api.on_sub_calc(
            subgroup=ClassicalSubgroups.from_str(self.subgroups_combo.currentText()),
            n=int(self.line_edit.text())
        )

    @pyqtSlot(object)
    def handle_status_message(self, message):
        self.statusBar.showMessage(message, 2000)

    @pyqtSlot()
    def handle_graph_draw_finished(self):
        self.graph_canvas.draw()

    @pyqtSlot()
    def handle_domain_draw_finished(self):
        self.domain_canvas.draw()
