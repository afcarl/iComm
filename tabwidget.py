from PyQt4.QtGui  import *
from PyQt4.QtCore import *

import sys


class Main(QWidget):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.widgetBox = QHBoxLayout(self)
        self.tabs = CTabWidget()
        self.widgetBox.addWidget(self.tabs)
        self.setLayout(self.widgetBox)


class CTabWidget(QTabWidget):

    def __init__(self, parent=None):
        super(CTabWidget, self).__init__(parent)
        self.tabBar = CTabBar(self)
        self.setTabBar(self.tabBar)
        self.setTabPosition(QTabWidget.South)

        self.tab1 = QTextEdit(self)
        self.tab2 = QWidget(self)

        self.addTab(self.tab1, "Foo")
        self.addTab(self.tab2, "Bar")



class CTabBar(QTabBar):

    def __init__(self, parent=None):
        super(CTabBar, self).__init__(parent)
        self.setMovable(True)

    def mouseDoubleClickEvent(self, event):

        self.changeName = CDialog(None, self)
        self.changeName.show()


class CDialog(QDialog):

    def __init__(self, parent, tabs):
        self.tabs = tabs
        super(CDialog, self).__init__(parent)
        self.topLayout = QVBoxLayout(self)
        self.topLayout.addWidget(QLabel(QString("Change name to:")))
        self.lineEdit = QLineEdit(self)
        self.topLayout.addWidget(self.lineEdit)

        self.set  = QPushButton(QString("Set"), self)
        self.quit = QPushButton(QString("Quit"), self)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.set)
        self.buttonLayout.addWidget(self.quit)

        self.topLayout.addLayout(self.buttonLayout)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setModal(True)

        self.set.clicked.connect(self.setClicked)
        self.quit.clicked.connect(self.quitClicked)


    def setClicked(self):
        index = self.tabs.currentIndex()
        text  = str(self.lineEdit.text()).rstrip().lstrip()
        if len(text):
            self.tabs.setTabText(index, QString(text))
        self.done(1)

    def quitClicked(self):
        self.done(1)


class Run(object):

    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle(QStyleFactory.create("plastique"))
        main = Main()
        main.show()
        sys.exit(app.exec_())


Run()
