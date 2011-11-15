from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

class Stack(QStackedWidget):

    def __init__(self, parent):
        super(Stack, self).__init__(parent)
        self.parent = parent
