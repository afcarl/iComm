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

        self.backgroundColor = Qt.black

        self.snapLines = False
        self.setBackgroundColor()
        
    def setBackgroundColor(self):
        brush = QBrush(self.backgroundColor)
        brush.setStyle(Qt.SolidPattern)
        self.setBackgroundBrush(brush)

    def mousePressEvent(self, event):
        self.p1 = event.pos()
        self.x1 = event.pos().x()
        self.y1 = event.pos().y()
        self.line = Line(self, self.p1)
        self.scene.addItem(self.line)

    def mouseMoveEvent(self, event):
        x2 = event.pos().x()
        y2 = event.pos().y()
        self.line.setLine(self.x1, self.y1, x2, y2)

    def mouseReleaseEvent(self, event):
        self.line._setPen(Qt.white, 1.0)

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
        super(Line, self).__init__(QLineF(p1, p1))

        self._setPen(Qt.green, 5)

    def _setPen(self, color, width):
        self.setPen(QPen(QBrush(color), width))
        

def run():
    app = QApplication(sys.argv)
    a   = Main(None)
    a.show()
    sys.exit(app.exec_())
    
run()
