from .qt_api import QtApi
from api import ClassicalSubgroups
from matplotlib.axes import Axes
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtGui import QFontDatabase, QFontMetrics

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from plotter.qt_canvas import GraphCanvas, DomainCanvas


class App(QMainWindow):
    digest = pyqtSignal(ClassicalSubgroups, str, Axes, Axes, name="digest")

    def __init__(self):
        super(__class__, self).__init__()

        self.left = 10
        self.top = 10
        self.width = 1080
        self.height = 720
        self.title = 'Modular'
        self.statusBar = QStatusBar()
        self.subgroups_combo = None
        self.graph_canvas = GraphCanvas(self)
        self.domain_canvas = DomainCanvas(self)
        self.generatorsTextEdit = None
        self.matrixLineEdit = None
        self.decompositionTextEdit = None

        self.minimumCanvasHeight = 550

        self.api_thread = QThread()
        self.api = QtApi()

        self.digest.connect(self.api.on_digest)
        self.api.handle_graph_axes.connect(self.graph_canvas.update_plot)
        self.api.handle_domain_axes.connect(self.domain_canvas.update_plot)
        self.api.handle_generators.connect(self.handleDigested)
        # self._qt_api.finished.connect(self.thread.quit)
        # self._qt_api.finished.connect(self.thread.deleteLater)

        self.api.moveToThread(self.api_thread)
        self.api_thread.start()

        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        layout = QVBoxLayout(self.centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(self.centralWidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(self.width)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.horizontalScrollBar().setEnabled(False)

        layout.addWidget(self.scroll_area)

        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 640, 400))

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.grid = QGridLayout(self.scroll_area_widget_contents)

        self.grid.addWidget(self.createGammaSection(), 0, 0)
        self.grid.addWidget(self.create_graph_section(), 1, 0)
        self.grid.addWidget(self.createDomainSection(), 2, 0)
        self.grid.addWidget(self.createGeneratorsSection(), 3, 0)
        self.grid.addWidget(self.createDecompositionSection(), 4, 0)

        self.scroll_area_widget_contents.setLayout(self.grid)

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

    def create_graph_section(self):
        group_box = QGroupBox("Graph visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()

        toolbar = NavigationToolbar(self.graph_canvas, self)

        vbox.addWidget(self.graph_canvas, Qt.AlignLeft)
        vbox.addWidget(toolbar, Qt.AlignLeft)

        group_box.setLayout(vbox)
        group_box.setMinimumHeight(self.minimumCanvasHeight)
        return group_box

    def createDomainSection(self):
        groupBox = QGroupBox("Domain and tree visualization")

        vbox = QVBoxLayout()
        vbox.addStretch()

        toolbar = MyToolbar(self.domain_canvas, self)
        toolbar.update()

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

    def createDecompositionSection(self):
        groupBox = QGroupBox("Decomposition of matrix")
        groupBoxLayout = QVBoxLayout(groupBox)

        matrixHBox = QWidget(groupBox)
        matrixHBoxLayout = QHBoxLayout(matrixHBox)

        matrixLabel = QLabel(groupBox)
        matrixLabel.setText('Type matrix:')
        self.matrixLineEdit = QLineEdit(groupBox)

        decomposeButton = QPushButton('Decompose')
        decomposeButton.setFixedSize(decomposeButton.sizeHint())
        decomposeButton.clicked.connect(self.onDecomposeButtonClicked)

        matrixHBoxLayout.addWidget(matrixLabel)
        matrixHBoxLayout.addWidget(self.matrixLineEdit)
        matrixHBoxLayout.addWidget(decomposeButton)

        groupBoxLayout.addWidget(matrixHBox)

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

        self.decompositionTextEdit = QTextEdit(self)
        self.monospaceFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self.decompositionTextEdit.setFont(self.monospaceFont)

        # self.generatorsTextEdit.setFontPointSize(16)

        self.decompositionTextEdit.setReadOnly(True)

        vbox.addWidget(self.decompositionTextEdit, Qt.AlignCenter, Qt.AlignTop)

        groupBox.setMinimumSize(groupBox.sizeHint())
        return groupBox

    def onApplyButtonClicked(self):

        self.graph_canvas.cla()
        self.domain_canvas.cla()

        self.digest.emit(
            ClassicalSubgroups.from_str(self.subgroups_combo.currentText()),
            self.line_edit.text(),
            self.graph_canvas.axes,
            self.domain_canvas.axes
        )



    def onDecomposeButtonClicked(self):
        # self.api.decompose(matrix=self.matrixLineEdit.text())
        pass

    @pyqtSlot(object)
    def handleStatusMessage(self, message):
        self.statusBar.showMessage(message, 5000)

    @pyqtSlot()
    def handleChewed(self):
        self.graph_canvas.draw()

    @pyqtSlot(str)
    def handleDigested(self, generators: str):
        if self.generatorsTextEdit:
            self.generatorsTextEdit.setText(generators)
            fontMetrics = QFontMetrics(self.monospaceFont)
            textSize = fontMetrics.size(0, generators)

            textWidth = max(textSize.width() + 30, 1000)  # constant may need to be tweaked
            textHeight = max(textSize.height() + 30, 220) # constant may need to be tweaked

            self.generatorsTextEdit.setMinimumSize(textWidth, textHeight)
            self.generatorsTextEdit.resize(textWidth, textHeight)

    # TODO: make resize
    @pyqtSlot(str)
    def handleDecomposed(self, decomposition):
        self.decompositionTextEdit.setText(decomposition)

    def handleMarkersStateChanged(self):
        #self.api.change_markers_state()
        #self.domain_canvas.draw()
        pass


class MyToolbar(NavigationToolbar):
    def __init__(self, figure_canvas, parent=None):
        self.parent = parent
        self.toolitems = (('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
            ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
            ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
            ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
            ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
            (None, None, None, None),
            ('Markers', 'Change', "change", 'change_state')
                          )

        NavigationToolbar.__init__(self, figure_canvas, parent=self.parent)

    def change_state(self):
        self.parent.handleMarkersStateChanged()
