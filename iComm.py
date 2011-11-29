#!/usr/bin/python

import sys
import os
import myPickle as Pickle

from PyQt4.QtCore  import *
from PyQt4.QtGui   import *
from Guis.iCommGui import Ui_MainWindow

class iComm(QMainWindow):

    def __init__(self):
        super(iComm, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mode         = None
        self.elementClass = None

        # make connection with menuElements and function handler
        self.ui.menuElements.triggered.connect(self.onElementsTriggered)
        self.ui.menuView.triggered.connect(self.onViewTriggered)
        self.ui.menuFile.triggered.connect(self.onFileTriggered)

        self.view       = self.ui.GraphicsView
        self.objInspect = self.ui.Inspector     # dock for obj inspection
        self.pyDock     = self.ui.Python        # dockWid that holds interp
        self.pyInterp   = self.ui.PyInterp      # interpreter
        self.statusBar  = self.ui.statusbar

        self.objInspect.hide()

        # pass locals from objects to interpreter to be in scope
        self.pyInterp.initInterpreter(locals())
        self.pyInterp.updateInterpreterLocals(self.view, "view")
        self.pyInterp.updateInterpreterLocals(self.objInspect, "inspector")
        self.pyInterp.updateInterpreterLocals(self.pyDock, "pythonDock")

        self.centerOnScreen()

        self.statusBar.showMessage(QString("Mode: Free"))

    def onFileTriggered(self, event):
        if str(event.text()) == "Save":
            Pickle.dump(self.view, "current.pkl")
        if str(event.text()) == "Open":
           
            self.view.scene.clear()
            self.mode = None
            self.statusBar.showMessage(QString("Mode: Free"))
            Pickle.load(self.view, "current.pkl")

    def onViewTriggered(self, event):

        if str(event.text()) == "Python Console":
            if self.pyDock.isVisible():
                self.pyDock.hide()
            else:
                self.pyDock.show()

        if str(event.text()) == "Object Inspector":
            if self.objInspect.isVisible():
                self.objInspect.hide()
            else:
                self.objInspect.show()

    def getMenuBacktrack(self, event):
        # take the event and backtrack through parents getting the title
        # along the way to get list of sub menus used.
        backtrack = [str(event.text())]
        previousWidget = event.associatedWidgets()[0]
        while previousWidget.__class__.__name__ != "QMenuBar":
            backtrack.append(str(previousWidget.title()))
            previousWidget = previousWidget.parent()
        return backtrack

    def onElementsTriggered(self, event):

        print self.getMenuBacktrack(event)

        # when any menu selection under Elements has been selected, change
        # the current active element to the selected element.
        self.elementClass = str(event.text())
        if filter(lambda x: x == self.elementClass, ["Waveguide", "Coax"]):
            self.mode = "link"
        else:
            self.mode = "draw"

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.mode:
            if self.mode == "link":
                pass
            self.mode = None
            self.elementClass = None
            self.statusBar.showMessage(QString("Mode: Free"))
        elif event.key() == Qt.Key_Escape and not self.mode:
            sys.exit(1)

#------------------------------------------------------------------------------- Testing
        if event.key() == Qt.Key_S:
            self.elementClass = "Hybrid"
            self.mode = "draw"
            self.statusBar.showMessage(QString("Mode: Edit"))
            self.setMovabilityFlag(True)

        if event.key() == Qt.Key_C:
            self.elementClass = "Coax"
            self.mode = "link"
            self.statusBar.showMessage(QString("Mode: Link"))
            self.setMovabilityFlag(False)
#------------------------------------------------------------------------------- Testing

    def setMovabilityFlag(self, bool):
        # toggle the movability of elements
        # we don't want elements to be moved when in link mode
        items = self.view.scene.items()
        items = filter(lambda x: x.__module__ == "elements", items)
        map(lambda x: x.setFlag(QGraphicsItem.ItemIsMovable, bool), items)

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width()  / 2) - (self.frameSize().width()  / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

class RunGui():

    def __init__(self):
        app = QApplication(sys.argv)
        myapp = iComm()
        myapp.show()
        if sys.platform != "linux2":
            app.setStyle(QStyleFactory.create("plastique"))
        sys.exit(app.exec_())

if __name__ == "__main__":
    RunGui()
