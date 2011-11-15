import os 
import sys

from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyQt4.QtCore import *

from gui import Ui_view

class Main(QWidget):
    
    def __init__(self, parent):
        super(Main, self).__init__(parent)

        self.ui = Ui_view()
        self.ui.setupUi(self)

        self.view  = self.ui.graphicsView
        self.scene = QGraphicsScene()

        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        self.scene.setBackgroundBrush(brush)
        
        self.view.setScene(self.scene)
        
        self.image = Image()
        self.scene.addItem(self.image)
        self.centerOnScreen()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()
            
        if event.key() == Qt.Key_C:
            self.image.setElementColor()
        
    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
                  
class Image(QGraphicsSvgItem):
    
    def __init__(self):
        super(Image, self).__init__('drawing.svg')
        self.id = self.elementId()
        self.imageIdList = ['black', 'green', 'red', 'blue', 'yellow']
        self.imageIdList = map(QString, self.imageIdList)

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
