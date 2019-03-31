import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFontDatabase, QFontMetrics, QFont
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from plotter.qt_canvas import MplCanvas, GraphCanvas, DomainCanvas
from gui.qt_api import QtApi
from api import ClassicalSubgroups


class App(QMainWindow):
    digest = pyqtSignal(ClassicalSubgroups, str, Axes, Axes, name='digest')
    decompose = pyqtSignal(str, name='decompose')
    STATUS_MESSAGE_COOLDOWN_TIME = 5000

    def __init__(self):
        super(__class__, self).__init__()

        self.graph_canvas = GraphCanvas()
        self.domain_canvas = DomainCanvas()

        self.worker_thread = QThread()
        self.worker = QtApi()

        self.digest.connect(self.worker.on_digest)
        self.decompose.connect(self.worker.on_decompose)
        self.worker.handle_status_message.connect(self.status_message_handler)
        self.worker.handle_graph_axes.connect(self.graph_axes_handler)
        self.worker.handle_domain_axes.connect(self.domain_axes_handler)
        self.worker.handle_generators.connect(self.generators_handler)
        self.worker.handle_decomposition.connect(self.decomposition_handler)
        self.worker.handle_markers_state_plotted.connect(self.on_markers_state_plotted)

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.central_widget = QWidget(self)
        self.status_bar = QStatusBar()

        self.subgroup_combo_box = None
        self.number_line_edit = None
        self.generators_text_edit = None
        self.matrix_line_edit = None
        self.decomposition_text_edit = None

        self.MONOSPACE_FONT = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self.init_ui()

    def init_ui(self):
        central_widget_layout = QVBoxLayout()

        central_widget_layout.addWidget(self.create_setup_section())
        central_widget_layout.addWidget(self.create_plots_section())
        central_widget_layout.addWidget(self.create_generators_section())
        central_widget_layout.addWidget(self.create_decompose_section())

        self.central_widget.setLayout(central_widget_layout)
        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)
        self.show()
        self.update()
    
    def create_setup_section(self):
        setup_section = QGroupBox("Subgroup setup")
        setup_section_layout = QHBoxLayout()
        
        subgroup_label = QLabel('Choose subgroup: ')
        subgroup_label.setFixedSize(subgroup_label.sizeHint())

        self.subgroup_combo_box = QComboBox()
        self.subgroup_combo_box.addItems(ClassicalSubgroups.get_all_names())
        self.subgroup_combo_box.setFixedSize(self.subgroup_combo_box.sizeHint())
        
        number_label = QLabel('Type N: ')
        number_label.setFixedSize(number_label.sizeHint())

        self.number_line_edit = QLineEdit()
        self.number_line_edit.setFixedWidth(40)

        setup_button = QPushButton('Apply')
        setup_button.setFixedSize(setup_button.sizeHint())
        setup_button.clicked.connect(self.on_digest_button_click)
        
        setup_section_layout.addWidget(subgroup_label)
        setup_section_layout.addWidget(self.subgroup_combo_box)
        setup_section_layout.addWidget(number_label)
        setup_section_layout.addWidget(self.number_line_edit, alignment=Qt.AlignLeft)
        setup_section_layout.addWidget(setup_button, alignment=Qt.AlignRight)

        setup_section.setLayout(setup_section_layout)
        return setup_section

    def create_plots_section(self):
        plots = QGroupBox("Graph and domain")
        plots_layout = QHBoxLayout()

        graph = QWidget(parent=plots)
        graph_layout = QVBoxLayout()
        graph_canvas_toolbar = NavigationToolbar2QT(self.graph_canvas, graph)
        graph_layout.addWidget(self.graph_canvas)
        graph_layout.addWidget(graph_canvas_toolbar)
        graph.setLayout(graph_layout)
        graph.setMinimumHeight(300)

        domain = QWidget(parent=plots)
        domain_layout = QVBoxLayout()
        domain_canvas_toolbar = DomainToolbar(self.domain_canvas, domain)
        domain_canvas_toolbar.handle_markers_state_changed.connect(self.worker.on_markers_state_changed)
        domain_layout.addWidget(self.domain_canvas)
        domain_layout.addWidget(domain_canvas_toolbar)
        domain.setLayout(domain_layout)
        domain.setMinimumHeight(300)

        plots_layout.addWidget(graph, stretch=1)
        plots_layout.addWidget(domain, stretch=1)

        plots.setLayout(plots_layout)
        return plots

    def create_generators_section(self):
        generators_section = QGroupBox("List of subgroup generators")
        generators_section_layout = QVBoxLayout()

        self.generators_text_edit = QTextEdit()
        self.generators_text_edit.setReadOnly(True)
        self.generators_text_edit.setMaximumHeight(60)
        self.generators_text_edit.setFont(self.MONOSPACE_FONT)
        self.generators_text_edit.setLineWrapMode(QTextEdit.FixedPixelWidth)

        generators_section_layout.addWidget(self.generators_text_edit)

        generators_section.setLayout(generators_section_layout)
        generators_section.setFixedHeight(generators_section.minimumSizeHint().height())
        return generators_section

    def create_decompose_section(self):
        group_box = QGroupBox("Decomposition of matrix")
        group_box_layout = QVBoxLayout()

        matrix_input = QWidget(parent=group_box)
        matrix_input_layout = QHBoxLayout()

        matrix_label = QLabel('Type matrix: ')
        matrix_label.setFixedSize(matrix_label.sizeHint())

        self.matrix_line_edit = QLineEdit()
        self.matrix_line_edit.setFixedWidth(140)

        decompose_button = QPushButton('Apply')
        decompose_button.setFixedSize(decompose_button.sizeHint())
        decompose_button.clicked.connect(self.on_decompose)

        matrix_input_layout.addWidget(matrix_label)
        matrix_input_layout.addWidget(self.matrix_line_edit, alignment=Qt.AlignLeft)
        matrix_input_layout.addWidget(decompose_button, alignment=Qt.AlignRight)

        matrix_input.setLayout(matrix_input_layout)

        self.decomposition_text_edit = QTextEdit()
        self.decomposition_text_edit.setReadOnly(True)
        self.decomposition_text_edit.setMaximumHeight(60)
        self.decomposition_text_edit.setFont(self.MONOSPACE_FONT)
        self.decomposition_text_edit.setLineWrapMode(QTextEdit.FixedPixelWidth)

        group_box_layout.addWidget(matrix_input)
        group_box_layout.addWidget(self.decomposition_text_edit)

        group_box.setLayout(group_box_layout)
        group_box.setFixedHeight(group_box.minimumSizeHint().height())
        return group_box

    @pyqtSlot(str, int, name='statusMessageHandler')
    def status_message_handler(self, status_message, cooldown_time):
        self.status_bar.showMessage(status_message, self.STATUS_MESSAGE_COOLDOWN_TIME)

    def on_digest_button_click(self):
        self.graph_canvas.cla()
        self.domain_canvas.cla()

        self.digest.emit(
            ClassicalSubgroups.from_str(self.subgroup_combo_box.currentText()),
            self.number_line_edit.text(),
            self.graph_canvas.axes,
            self.domain_canvas.axes
        )

    @pyqtSlot(Axes, name='graphAxesHandler')
    def graph_axes_handler(self, axes):
        self.graph_canvas.update_plot(axes)

    @pyqtSlot(Axes, name='domainAxesHandler')
    def domain_axes_handler(self, axes):
        self.domain_canvas.update_plot(axes)

    @pyqtSlot(str, name='generatorsHandler')
    def generators_handler(self, generators: str):
        self.generators_text_edit.setText(generators)
        font_metrics = QFontMetrics(self.MONOSPACE_FONT)
        text_width = font_metrics.boundingRect(generators.split('\n')[0]).width() + 30
        self.generators_text_edit.setLineWrapColumnOrWidth(text_width)

    def on_decompose(self):
        self.decompose.emit(self.matrix_line_edit.text())

    @pyqtSlot(str, name='decompositionHandler')
    def decomposition_handler(self, decomposition):
        self.decomposition_text_edit.setText(decomposition)
        font_metrics = QFontMetrics(self.MONOSPACE_FONT)
        text_width = font_metrics.boundingRect(decomposition.split('\n')[0]).width() + 30
        self.decomposition_text_edit.setLineWrapMode(text_width)

    def on_markers_state_plotted(self):
        self.domain_canvas.draw()


class DomainToolbar(NavigationToolbar2QT):
    handle_markers_state_changed = pyqtSignal()

    def __init__(self, figure_canvas, parent=None, ):
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

        NavigationToolbar2QT.__init__(self, figure_canvas, parent=self.parent)

    def change_state(self):
        self.handle_markers_state_changed.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
