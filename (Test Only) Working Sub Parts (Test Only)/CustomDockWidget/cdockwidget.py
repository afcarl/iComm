
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class CDockWidget(QDockWidget):

    def __init__(self, parent):
        title = QString('Embedded Python Interpreter')
        super(CDockWidget, self).__init__(title, parent)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setFeatures(QDockWidget.DockWidgetMovable|
                         QDockWidget.DockWidgetClosable)

        self.setTitleBarWidget(CustomTitleBar(self))


        self.showState = False
        self.widget_height = 200

    def closeEvent(self, event):
        event.ignore()
        print self.parent().size().height()

        if self.showState:
            self.widget_height = self.height()
            self.setFixedHeight(35)
            self.setVisible(False)
            self.setVisible(True)
        else:
            self.setFixedHeight(self.widget_height)
            self.setVisible(False)
            self.setVisible(True)
            self.setMinimumHeight(35)
            self.setMaximumHeight(self.parent().size().height())
            
            

            
        self.showState = not self.showState

class CustomTitleBar(QWidget):

    def __init__(self, parent):
        super(CustomTitleBar, self).__init__(parent)
        

        self.collapseButton = TitleBarButtons(self)
        ##self.connect(self.collapseButton, SIGNAL("clicked()"),
                     ##self.toggleCollapsed)
        self.collapseButton.setVisible(True)

class TitleBarButtons(QAbstractButton):

    def __init__(self, parent):
        super(TitleBarButtons, self).__init__(parent)
        self.setIcon(QIcon('arrow-right.png'))

        self.resize(30, 30)
        print self.size()

    def paintEvent(self, event):
        p = QPainter(self)
        r = self.rect()
        
        opt = QStyleOptionToolButton()
        opt.init(self)
        opt.state |= QStyle.State_AutoRaise
        opt.icon = self.icon()
        opt.subControls = QStyle.SubControls()
        opt.activeSubControls = QStyle.SubControls()
        opt.features = QStyleOptionToolButton.None
        opt.arrowType = Qt.NoArrow
        size = self.style().pixelMetric(QStyle.PM_SmallIconSize, None, self)
        opt.iconSize = QSize(size, size)
        self.style().drawComplexControl(QStyle.CC_ToolButton, opt, p, self)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = CustomTitleBar(None)
    button = TitleBarButtons(test)
    test.show()
    sys.exit(app.exec_())
