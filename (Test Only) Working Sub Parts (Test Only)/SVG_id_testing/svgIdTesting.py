import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyQt4.QtCore import *

from gui import Ui_view

class Main(QWidget):

    def __init__(self, parent):
        super(Main, self).__init__(parent)

        hBox = QHBoxLayout(self)
        self.view  = View(self)
        hBox.addWidget(self.view)
        self.centerOnScreen()
        self.resize(300, 300)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()

        if event.key() == Qt.Key_C:
            self.image.setElementColor()

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

class View(QGraphicsView):

    def __init__(self, parent):
        super(View, self).__init__(parent)

        self.scene = QGraphicsScene()
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        self.scene.setBackgroundBrush(brush)
        self.setScene(self.scene)

        self.setMouseTracking(True)

        self.image = Image()
        self.scene.addItem(self.image)

    def mouseMoveEvent(self, event):
        if self.scene.items(QPointF(event.pos())):
            print 'over'



class Image(QGraphicsSvgItem):

    def __init__(self):
        super(Image, self).__init__('drawing.svg')
        self.id = self.setElementId('blank')
        self.imageIdList = ['blank', 'top', 'right', 'bottom', 'left', 'center']
        self.imageIdList = map(QString, self.imageIdList)

        self.setPos(150, 150)

        print self.boundingRect()

    def setElementColor(self):
        id = self.imageIdList.pop(0)
        self.setElementId(id)
        self.imageIdList.append(id)

class RunMain:

    def __init__(self):
        app = QApplication(sys.argv)
        test = Main(None)
        test.show()
        sys.exit(app.exec_())

RunMain()
