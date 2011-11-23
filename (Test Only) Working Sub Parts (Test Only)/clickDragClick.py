from PyQt4.QtGui  import *
from PyQt4.QtCore import *
import math
import sys

class Main(QWidget):

    def __init__(self, parent):
        super(Main, self).__init__(parent)

        self.resize(300, 300)
        vBox = QVBoxLayout(self)
        view = View(self)
        vBox.addWidget(view)

class View(QGraphicsView):

    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.setBackgroundColor(Qt.black)
        self.setMouseTracking(True)

        self.click = 'start'

    def setBackgroundColor(self, bgColor):
        brush = QBrush(bgColor)
        brush.setStyle(Qt.SolidPattern)
        self.setBackgroundBrush(brush)

    def mousePressEvent(self, event):
        if self.click == 'start':
            self.line = Line(self, event.pos())
            self.scene.addItem(self.line)
            self.click = 'mid'
        elif self.click == 'mid':
            self.click = 'stop'

    def mouseMoveEvent(self, event):
        if self.click == 'mid':
            p1 = self.line.line.p1()
            p2 = QPointF(event.pos())
            self.line.setLine(QLineF(p1, p2))

    def mouseReleaseEvent(self, event):
        if self.click == 'stop':
            self.line._setPen(Qt.white, 1.0)
            self.click = 'start'

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.snapLines = True

        if event.key() == Qt.Key_Escape:
            sys.exit()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.snapLines = False

class Line(QGraphicsLineItem):

    def __init__(self, parent, p1):
        # args = start, stop
        p1 = QPointF(parent.mapToScene(p1))
        self.line = QLineF(p1, p1)
        super(Line, self).__init__(self.line)

        self._setPen(Qt.green, 5)

    def _setPen(self, color, width):
        self.setPen(QPen(QBrush(color), width))

def run():
    app = QApplication(sys.argv)
    a   = Main(None)
    a.show()
    sys.exit(app.exec_())

run()
