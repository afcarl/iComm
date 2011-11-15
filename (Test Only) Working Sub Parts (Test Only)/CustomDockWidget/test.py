import sys
import os


import pyinterp

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gui import Ui_MainWindow


class Main(QMainWindow):

    def __init__(self, parent):

        super(Main, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.ui.textEdit.initInterpreter(locals())
        self.ui.textEdit.updateInterpreterLocals(self.ui.dockWidget)


class Run:
    def __init__(self):
        app = QApplication(sys.argv)
        test = Main(None)
        test.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    Run()
