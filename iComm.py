#!/usr/bin/python

import Save


import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Guis.iCommGui import Ui_MainWindow

import icommglobals

# make an instance of icommglobals.Globas in __builtins__ to allow all modules
# access to my custom class.  Probably should do this with Qt.emit() but this
# way appears to be much cleaner and nicer for my needs.  Also I'm not affraid
# of python ever coming up with the builtin function name iCommGlobals
__builtins__.iCommGlobals = icommglobals.Globals()

class iComm(QMainWindow):

    def __init__(self):
        super(iComm, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # make connection with menuElements and function handler
        self.ui.menuElements.triggered.connect(self.onElementsTriggered)
        self.ui.menuView.triggered.connect(self.onViewTriggered)
        self.ui.menuFile.triggered.connect(self.onFiletriggered)
        
        self.centerOnScreen()

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

    def onFiletriggered(self, event):
        if str(event.text()) == "Save":
            print 'save'
            Save.Pkl().dump(self.view, 'AAA.pkl')

    def onViewTriggered(self, event):

        # toggle between viewing object inspector and python interpreter
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
        iCommGlobals.elementClass = str(event.text())
        if filter(lambda x: x == iCommGlobals.elementClass, ["Waveguide", "Coax"]):
            iCommGlobals.mode = "link"
        else:
            iCommGlobals.mode = "draw"

    def keyPressEvent(self, event):
        if event.text() == "q":
            sys.exit(1)

#------------------------------------------------------------------------------- Testing
        if event.text() == "e":
            for x in self.elements():
                print x.__class__.__name__, x.eId
            print "\n-------------"

        if event.text() == "t":
            tree = []
            for x in self.view.scene.items():
                if not x.__class__.__name__ == "Coax":
                    t = [(x.eId, y) for y in x.linksTo]
                    f = [(y, x.eId) for y in x.linksFrom]
                    tree.extend(t + f)
            tree = list(set(tree))
            tree.sort(key=lambda x: x[0])
            for x in tree:
                print x

        if event.key() == Qt.Key_S:
            iCommGlobals.elementClass = "Hybrids"
            iCommGlobals.mode = "draw"
            self.statusBar.showMessage(QString("Mode: Edit"))
            self.setMovabilityFlag(True)

        if event.key() == Qt.Key_C:
            iCommGlobals.elementClass = "Coax"
            iCommGlobals.mode = "link"
            self.statusBar.showMessage(QString("Mode: Link"))
            self.setMovabilityFlag(False)

        if event.key() == Qt.Key_F1:
            print "test F1"
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
        app.setStyle(QStyleFactory.create("plastique"))
        sys.exit(app.exec_())

if __name__ == "__main__":
    RunGui()
