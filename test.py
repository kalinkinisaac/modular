import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFontDatabase, QFontMetrics, QFont
from matplotlib.axes import Axes
from plotter.qt_canvas import MplCanvas
from gui.qt_api import QtApi
from api import ClassicalSubgroups


class App(QMainWindow):
    digest = pyqtSignal(ClassicalSubgroups, str, Axes, Axes, name='digest')

    def __init__(self):
        super(__class__, self).__init__()

        self.graph_canvas = MplCanvas(style='fast')
        self.domain_canvas = MplCanvas(style='ggplot')

        self.worker_thread = QThread()
        self.worker = QtApi()

        self.digest.connect(self.worker.on_digest)
        self.worker.handle_graph_axes.connect(self.graph_axes_handler)
        self.worker.handle_domain_axes.connect(self.domain_axes_handler)
        self.worker.handle_generators.connect(self.generators_handler)

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.central_widget = QWidget(self)

        self.number_line_edit = None
        self.generators_text_edit = None
        self.subgroup_combo_box = None

        self.MONOSPACE_FONT = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self.init_ui()

    def init_ui(self):
        central_widget_layout = QVBoxLayout(self.central_widget)

        central_widget_layout.addWidget(self.create_setup_section())
        central_widget_layout.addWidget(self.create_plots_section())
        central_widget_layout.addWidget(self.create_generators_section())

        self.setCentralWidget(self.central_widget)
        self.show()
    
    def create_setup_section(self):
        setup_section = QWidget(parent=self.central_widget)
        setup_section_layout = QHBoxLayout(setup_section)
        
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
        setup_section_layout.addWidget(self.number_line_edit, Qt.AlignCenter, Qt.AlignLeft)
        setup_section_layout.addWidget(setup_button, Qt.AlignCenter, Qt.AlignRight)
        
        return setup_section

    def create_plots_section(self):
        plots = QWidget(parent=self.central_widget)
        plots_layout = QHBoxLayout(plots)

        plots_layout.addWidget(self.graph_canvas, Qt.AlignLeft)
        plots_layout.addWidget(self.domain_canvas, Qt.AlignLeft)

        return plots

    def create_generators_section(self):
        generators_section = QWidget(parent=self.central_widget)
        generators_section_layout = QVBoxLayout(generators_section)

        self.generators_text_edit = QTextEdit(generators_section)
        self.generators_text_edit.setFont(self.MONOSPACE_FONT)
        # self.generatorsTextEdit.setFontPointSize(16)
        #self.generators_text_edit.setLineWrapColumnOrWidth(45000)
        self.generators_text_edit.setLineWrapMode(QTextEdit.FixedPixelWidth)


        generators_section_layout.addWidget(self.generators_text_edit)


        return generators_section

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
        font_metrics = QFontMetrics(self.MONOSPACE_FONT)
        text_width = font_metrics.boundingRect(generators.split('\n')[0]).width() + 30
        self.generators_text_edit.setLineWrapColumnOrWidth(text_width)
        self.generators_text_edit.setText(generators)
        #
        # text_width = max(text_width.width() + 30, 1000)  # constant may need to be tweaked
        # textHeight = max(text_width.height() + 30, 220)  # constant may need to be tweaked
        #
        # self.generatorsTextEdit.setMinimumSize(text_width, textHeight)
        # self.generatorsTextEdit.resize(text_width, textHeight)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
