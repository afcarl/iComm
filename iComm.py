#!/usr/bin/python

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
        self.centerOnScreen()

        self.view           = self.ui.GraphicsView
        self.inspector      = self.ui.Inspector
        self.pythonDock     = self.ui.Python
        self.pyInterp       = self.ui.PyInterp

        self.inspector.hide()

        self.pyInterp.initInterpreter(locals())
        self.pyInterp.updateInterpreterLocals(self.view, 'view')
        self.pyInterp.updateInterpreterLocals(self.inspector, 'inspector')
        self.pyInterp.updateInterpreterLocals(self.pythonDock, 'pythonDock')


    def onViewTriggered(self, event):

        if str(event.text()) == 'Python Console':
            if self.pythonDock.isVisible():
                self.pythonDock.hide()
            else:
                self.pythonDock.show()

        if str(event.text()) == 'Object Inspector':
            if self.inspector.isVisible():
                self.inspector.hide()
            else:
                self.inspector.show()


    def onElementsTriggered(self, event):

        # when any menu selection under Elements has been selected, change
        # the current active element to the selected element.
        iCommGlobals.elementClass = str(event.text())
        if filter(lambda x: x == iCommGlobals.elementClass, ['Waveguide', 'Coax']):
            iCommGlobals.mode = 'link'
        else:
            iCommGlobals.mode = 'draw'

    def keyPressEvent(self, event):
        if event.text() == 'q':
            print 'kill self...'
            sys.exit(1)

#------------------------------------------------------------------------------- Testing
        if event.text() == 'e':
            for x in self.elements():
                print x.__class__.__name__, x.eId
            print '\n-------------'

        if event.text() == 't':
            tree = []
            for x in self.elements():
                if not x.__class__.__name__ == 'Coax':
                    t = [(x.eId, y) for y in x.linksTo]
                    f = [(y, x.eId) for y in x.linksFrom]
                    tree.extend(t + f)
            tree = list(set(tree))
            tree.sort(key=lambda x: x[0])
            for x in tree:
                print x

        if event.key() == Qt.Key_S:
            iCommGlobals.elementClass = 'Hybrids'
            iCommGlobals.mode = 'draw'

        if event.key() == Qt.Key_C:
            iCommGlobals.elementClass = 'Coax'
            iCommGlobals.mode = 'link'

        if event.key() == Qt.Key_F1:
            print 'test F1'
#------------------------------------------------------------------------------- Testing

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width()  / 2) - (self.frameSize().width()  / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

class RunGui():

    def __init__(self):
        app = QApplication(sys.argv)
        myapp = iComm()
        myapp.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    RunGui()
