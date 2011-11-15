from PyQt4.QtCore import *
from PyQt4.QtGui import *


def hasFeature(dockwidget, feature):
    return dockwidget.features() & feature == feature



class DockWidgetTitleBarButton(QAbstractButton):


    def __init__(self, titlebar):
        QAbstractButton.__init__(self, titlebar)
        self.setFocusPolicy(Qt.NoFocus)

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


import os
__icon_path__ = os.path.dirname(os.path.abspath(__file__))
print __file__
print __icon_path__
print os.path.abspath(__file__)

class DockWidgetTitleBar(QWidget):

    
    def __init__(self, dockWidget):
        QWidget.__init__(self, dockWidget)
        self.openIcon = QIcon(os.path.join(__icon_path__, "arrow-down.png"))
        self.closeIcon = QIcon(os.path.join(__icon_path__, "arrow-right.png"))
        q = dockWidget
        
        self.collapseButton = DockWidgetTitleBarButton(self)
        self.collapseButton.setIcon(self.openIcon)
        self.connect(self.collapseButton, SIGNAL("clicked()"),
                     self.toggleCollapsed)
        self.collapseButton.setVisible(True)


    def minimumSizeHint(self):
        return self.sizeHint()


    def sizeHint(self):
        q = self.parentWidget()
        mw = q.style().pixelMetric(QStyle.PM_DockWidgetTitleMargin, None, q)
        fw = q.style().pixelMetric(QStyle.PM_DockWidgetFrameWidth, None, q)
        return QSize(21 + 21 + 4 * mw + 2 * fw, 21)

    def setCollapsed(self, collapsed):
        q = self.parentWidget()
        if q and q.widget() and q.widget().isHidden() != collapsed:
            self.toggleCollapsed()


    def toggleCollapsed(self):
        q = self.parentWidget()
        if not q:
            return
        q.toggleCollapsed()
        self.collapseButton.setIcon(q.isCollapsed() and self.openIcon or self.closeIcon)


class DockMainWidgetWrapper(QWidget):


    def __init__(self, dockwidget):
        QWidget.__init__(self, dockwidget)
        self.widget = None
        self.widget_height = 0
        self.hlayout = QHBoxLayout(self)
        self.setLayout(self.hlayout)

        
    def setWidget(self, widget):
        self.widget = widget
        self.widget_height = widget.height
        self.layout().addWidget(widget)


    def isCollapsed(self):
        return self.widget.isVisible()


    def setCollapsed(self, flag):
        if not flag:
            self.widget_height = self.widget.height()
            self.setFixedHeight(0)
            self.widget.setVisible(False)
            print self.widget.size()
            print 'visible False'
        else:
            self.setFixedHeight(self.widget_height)            
            self.widget.setVisible(True)
            self.setMinimumHeight(0)
            self.setMaximumHeight(2048)
            print self.widget.size()
            print 'visible True'


class DockWidget(QDockWidget):


    def __init__(self, *args):
        QDockWidget.__init__(self, *args)
        self.titleBar = DockWidgetTitleBar(self)
        self.setTitleBarWidget(self.titleBar)
        self.mainWidget = None


    def setWidget(self, widget):
        self.mainWidget = DockMainWidgetWrapper(self)
        self.mainWidget.setWidget(widget)
        QDockWidget.setWidget(self, self.mainWidget)
    

    def setCollapsed(self, flag):
        self.mainWidget.setCollapsed(flag)


    def isCollapsed(self):
        return self.mainWidget.isCollapsed()


    def toggleCollapsed(self):
        self.setCollapsed(not self.isCollapsed())



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    ##dock1 = DockWidget("1st dockwidget", win)
    ##combo =  QComboBox(dock1)
    ##dock1.setWidget(combo)
    #win.addDockWidget(Qt.LeftDockWidgetArea, dock1)
    dock2 = DockWidget("2nd dockwidget")
    button = QPushButton("Hello, world!", dock2)
    dock2.setWidget(button)
    win.addDockWidget(Qt.TopDockWidgetArea, dock2)
    edit = QTextEdit(win)
    win.setCentralWidget(edit)
    win.resize(640, 480)
    win.show()
    app.exec_()
