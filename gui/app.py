from .qt_api import QtApi
from subgroups_names import ClassicalSubgroups

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, pyqtSlot
from PyQt5.QtGui import QFontDatabase

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from plotter.qt_canvas import GraphCanvas, DomainCanvas


class App(QMainWindow):

    def __init__(self):
        super(__class__, self).__init__()
        self.api = QtApi(
            handleStatusMessage=self.handleStatusMessage,
            handleChewed=self.handleChewed,
            handleDigested=self.handleDigested
        )
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.title = 'Modular'
        self.statusBar = QStatusBar()
        self.subgroups_combo = None
        self.graph_canvas = GraphCanvas(parent=self)
        self.domain_canvas = DomainCanvas(parent=self)
        self.generators_text_edit = None

        self.minimumCanvasHeight = 550
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        layout = QVBoxLayout(self.centralWidget)

        self.scrollArea = QScrollArea(self.centralWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumWidth(self.width)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.horizontalScrollBar().setEnabled(False)

        layout.addWidget(self.scrollArea)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 640, 400))

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)



        self.grid = QGridLayout(self.scrollAreaWidgetContents)

        self.grid.addWidget(self.create_gamma_section(), 0, 0)
        self.grid.addWidget(self.create_graph_section(), 1, 0)
        self.grid.addWidget(self.create_domain_section(), 2, 0)
        self.grid.addWidget(self.create_generators_section(), 3, 0)

        self.scrollAreaWidgetContents.setLayout(self.grid)

        self.setCentralWidget(self.centralWidget)

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
        hbox.addWidget(button, Qt.AlignCenter, Qt.AlignRight)
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
        groupBox.setMinimumHeight(self.minimumCanvasHeight)
        return groupBox

    def create_domain_section(self):
        groupBox = QGroupBox("Independent set of generators")

        vbox = QVBoxLayout()
        vbox.addStretch()

        toolbar = NavigationToolbar(self.domain_canvas, self)

        vbox.addWidget(self.domain_canvas, Qt.AlignLeft)
        vbox.addWidget(toolbar, Qt.AlignLeft)

        groupBox.setLayout(vbox)
        groupBox.setMinimumHeight(self.minimumCanvasHeight)
        return groupBox

    def create_generators_section(self):
        groupBox = QGroupBox("Domain and tree visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()

        self.generators_text_edit = QTextEdit(self)
        try:
            self.generators_text_edit.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        except:
            pass
        finally:
            self.generators_text_edit.setFontPointSize(16)
        self.generators_text_edit.setReadOnly(True)
        self.generators_text_edit.setMaximumHeight(240)


        vbox.addWidget(self.generators_text_edit, Qt.AlignLeft, Qt.AlignTop)

        groupBox.setLayout(vbox)
        groupBox.setMinimumHeight(self.minimumCanvasHeight)
        return groupBox

    def on_construct_graph_button_clicked(self):
        self.api.digest(
            subgroup=ClassicalSubgroups.from_str(self.subgroups_combo.currentText()),
            n=int(self.line_edit.text()),
            graph_canvas=self.graph_canvas,
            domain_canvas=self.domain_canvas
        )
        try:
            pass
        except ValueError:
            self.statusBar.showMessage('Type number N in text field on top', 5000)
        except:
            self.statusBar.showMessage('Unknown error', 5000)

    @pyqtSlot(object)
    def handleStatusMessage(self, message):
        self.statusBar.showMessage(message, 2000)

    @pyqtSlot()
    def handleChewed(self):
        self.graph_canvas.draw()

    @pyqtSlot(str)
    def handleDigested(self, generators: str):
        self.domain_canvas.draw()

        if self.generators_text_edit:
            self.generators_text_edit.setText(generators)


