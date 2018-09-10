from .qt_api import QtApi
from subgroups_names import ClassicalSubgroups

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, pyqtSlot
from PyQt5.QtGui import QFontDatabase, QFontMetrics

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
        self.generatorsTextEdit = None

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

        self.grid.addWidget(self.createGammaSection(), 0, 0)
        self.grid.addWidget(self.createGraphSection(), 1, 0)
        self.grid.addWidget(self.createDomainSection(), 2, 0)
        self.grid.addWidget(self.createGeneratorsSection(), 3, 0)

        self.scrollAreaWidgetContents.setLayout(self.grid)

        self.setCentralWidget(self.centralWidget)

        self.setStatusBar(self.statusBar)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def createGammaSection(self):
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

        applyButton = QPushButton('Apply')
        applyButton.setFixedSize(applyButton.sizeHint())
        applyButton.clicked.connect(self.onApplyButtonClicked)

        hbox = QHBoxLayout()

        hbox.addWidget(lbl)
        hbox.addWidget(self.subgroups_combo)
        hbox.addWidget(lbl2)
        hbox.addWidget(self.line_edit)
        hbox.addWidget(applyButton, Qt.AlignCenter, Qt.AlignRight)
        hbox.addStretch()

        groupBox.setLayout(hbox)

        return groupBox

    def createGraphSection(self):
        groupBox = QGroupBox("Graph visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()


        toolbar = NavigationToolbar(self.graph_canvas, self)

        vbox.addWidget(self.graph_canvas, Qt.AlignLeft)
        vbox.addWidget(toolbar, Qt.AlignLeft)

        groupBox.setLayout(vbox)
        groupBox.setMinimumHeight(self.minimumCanvasHeight)
        return groupBox

    def createDomainSection(self):
        groupBox = QGroupBox("Domain and tree visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()

        toolbar = NavigationToolbar(self.domain_canvas, self)

        vbox.addWidget(self.domain_canvas, Qt.AlignLeft)
        vbox.addWidget(toolbar, Qt.AlignLeft)

        groupBox.setLayout(vbox)
        groupBox.setMinimumHeight(self.minimumCanvasHeight)
        return groupBox

    def createGeneratorsSection(self):
        groupBox = QGroupBox("Independent set of generators")
        groupBoxLayout = QHBoxLayout(groupBox)

        scrollArea = QScrollArea(groupBox)
        scrollArea.setWidgetResizable(True)
        scrollArea.setMinimumHeight(150)
        scrollArea.setFrameShape(QFrame.NoFrame)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.verticalScrollBar().setEnabled(False)

        groupBoxLayout.addWidget(scrollArea)

        scrollAreaWidgetContents = QWidget()
        scrollAreaWidgetContents.setGeometry(QRect(0, 0, 640, 400))

        scrollArea.setWidget(scrollAreaWidgetContents)

        vbox = QVBoxLayout(scrollAreaWidgetContents)
        vbox.addStretch()

        self.generatorsTextEdit = QTextEdit(self)
        self.monospaceFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self.generatorsTextEdit.setFont(self.monospaceFont)

        # self.generatorsTextEdit.setFontPointSize(16)

        self.generatorsTextEdit.setReadOnly(True)

        vbox.addWidget(self.generatorsTextEdit, Qt.AlignCenter, Qt.AlignTop)

        # scrollAreaWidgetContents.addWidget(self.generators_text_edit, Qt.AlignLeft, Qt.AlignTop)

        groupBox.setMinimumSize(groupBox.sizeHint())
        return groupBox

    def onApplyButtonClicked(self):
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

        if self.generatorsTextEdit:
            self.generatorsTextEdit.setText(generators)
            fontMetrics = QFontMetrics(self.monospaceFont)
            textSize = fontMetrics.size(0, generators)

            textWidth = textSize.width() + 30  # constant may need to be tweaked
            textHeight = textSize.height() + 30  # constant may need to be tweaked

            self.generatorsTextEdit.setMinimumSize(textWidth, textHeight)  # good if you want to insert this into a layout
            self.generatorsTextEdit.resize(textWidth, textHeight)



