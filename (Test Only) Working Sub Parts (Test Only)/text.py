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

        self.low = "This is a list of words that I made with split".split(' ')

    def setBackgroundColor(self, bgColor):
        brush = QBrush(bgColor)
        brush.setStyle(Qt.SolidPattern)
        self.setBackgroundBrush(brush)

    def mousePressEvent(self, event):
        try:
            word = self.low.pop(0)
            pos  = QPointF(event.pos())
            self.scene.addItem(Text(word, pos))
        except:
            pass
        super(View, self).mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.snapLines = True

        if event.key() == Qt.Key_Escape:
            sys.exit()

class Text(QGraphicsTextItem):

    def __init__(self, text, pos):

        self.text   = QString(text)
        self.pos    = pos
        super(Text, self).__init__(self.text)

        self.setPos(self.pos)
        self.setDefaultTextColor(Qt.white)
        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable)

        self.show()

def run():
    app = QApplication(sys.argv)
    a   = Main(None)
    a.show()
    sys.exit(app.exec_())

run()
