from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *


class RdText(QGraphicsTextItem):

    def __init__(self, text, pos):

        self.text   = QString(text)
        super(RdText, self).__init__(self.text)
        self.height   = self.boundingRect().height()
        self.setPosition(pos)
        self.setDefaultTextColor(Qt.white)

    def setPosition(self, pos):
        self.setPos(QPointF(pos.x(), pos.y() - self.height))

    def update(self, text=None):
        if text:
            self.setPlainText(text)
        else:
            self.setPlainText(self.text)
