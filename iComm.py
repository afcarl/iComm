#!/usr/bin/python

import sys
import os
import myPickle as Pickle
import Plugins


from PyQt4.QtCore  import *
from PyQt4.QtGui   import *
from Guis.iCommGui import Ui_MainWindow

class iComm(QMainWindow):

    def __init__(self):
        super(iComm, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.elementClass = None

        # make connection with menuElements and function handler
        self.menubar = self.ui.menubar
        self.ui.menuElements.triggered.connect(self.onElementsTriggered)
        self.ui.menuView.triggered.connect(self.onViewTriggered)
        self.ui.menuFile.triggered.connect(self.onFileTriggered)
        self.setUpPluginsMenu()

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

        self.setToCenter()
        self.setMode("free")
# ---------------------------------------------------------------------------- #
#
# ---------------------------------------------------------------------------- #
    def setUpPluginsMenu(self):
        menu = self.menubar.addMenu("Plugins")
        for name in self.getListOfPlugins():
            menu.addAction(name)
        menu.triggered.connect(self.onPluginsTriggered)

    def getListOfPlugins(self):
        dirs = os.listdir(Plugins.__path__[0])
        dirs = filter(lambda x: ".py" not in x, dirs)
        dirs = filter(lambda x: x[0] != "_", dirs)
        dirs.sort()
        for d in dirs:
            string = "Plugins." + d + ".info"
            __import__(string)
            yield sys.modules[string].info["menu name"]
# ---------------------------------------------------------------------------- #
# ------------------------------ Menu Handlers ------------------------------- #
# ---------------------------------------------------------------------------- # File
    def onFileTriggered(self, event):
        if str(event.text()) == "Save":
            Pickle.dump(self.view, "current.pkl")

        if str(event.text()) == "Open":
            self.view.scene.clear()
            self.setMode("free")
            Pickle.load(self.view, "current.pkl")
    # ------------------------------------------------------------------------ # View
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
    # ------------------------------------------------------------------------ # Elements
    def onElementsTriggered(self, event):
        # when any menu selection under Elements has been selected, change
        # the current active element to the selected element.
        # self.elementClass = str(event.text())
        self.elementClass = self.getMenuBacktrack(event)
        if "Waveguide" in self.elementClass or "Coax" in self.elementClass:
            self.mode = "link"
        else:
            self.mode = "draw"
    # ------------------------------------------------------------------------ # Plugins
    def onPluginsTriggered(self, event):
        print event.text()
    # ------------------------------------------------------------------------ # getMenuBacktrack
    def getMenuBacktrack(self, event):
        # take the event and backtrack through parents getting the title
        # along the way to get list of sub menus used.
        backtrack = [str(event.text())]
        previousWidget = event.associatedWidgets()[0]
        while previousWidget.__class__.__name__ != "QMenuBar":
            backtrack.append(str(previousWidget.title()))
            previousWidget = previousWidget.parent()
        backtrack.pop()
        return backtrack
# ---------------------------------------------------------------------------- #
#
# ---------------------------------------------------------------------------- #
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.mode:
            if self.mode == "link":
                pass
            self.elementClass = None
            self.setMode("free")
        elif event.key() == Qt.Key_Escape and not self.mode:
            sys.exit(1)
    # ------------------------------------------------------------------------ # Testing
        if event.key() == Qt.Key_S:
            self.elementClass = "Hybrid"
            self.setMode("draw")
            self.setMovabilityFlag(True)

        if event.key() == Qt.Key_C:
            self.elementClass = "Coax"
            self.setMode("link")
            self.setMovabilityFlag(False)
# ---------------------------------------------------------------------------- #
# ------------------------------------Sets------------------------------------ #
# ---------------------------------------------------------------------------- #
    def setMovabilityFlag(self, bool):
        # toggle the movability of elements
        # we don't want elements to be moved when in link mode
        items = self.view.scene.items()
        items = filter(lambda x: x.__module__ == "elements", items)
        map(lambda x: x.setFlag(QGraphicsItem.ItemIsMovable, bool), items)

    def setToCenter(self):
        resolution = QDesktopWidget().screenGeometry()
        x = resolution.width() / 2 - self.frameSize().width() / 2
        y = resolution.height()/ 2 - self.frameSize().height()/ 2
        self.move(x, y)

    def setMode(self, mode):
        self.mode = mode
        string = "Mode: " + mode.capitalize()
        self.statusBar.showMessage(string)
# ---------------------------------------------------------------------------- #
# -----------------------------------Runner----------------------------------- #
# ---------------------------------------------------------------------------- #
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
