import sys

import matplotlib

matplotlib.use('WebAgg')

from PyQt5.QtWidgets import *
from gui import App


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
