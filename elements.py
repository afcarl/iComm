import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from Guis.ParameterInput import hybridParameterGui

class ElementFactory(QGraphicsSvgItem):

    # This class allows us to init a class from a string
    def __init__(self, parent, element, pos):
        # remove all marks and "_" because our classes do not have these chars.
        element = re.sub('(-|_)', '', element)

        # check for the instance in __main__
        self.__class__ = getattr(sys.modules[__name__], element)

        # For testing only
        element = 'test'
        # For testing only

        self.__class__.__init__(self, parent, element, pos)

class BaseElement(QGraphicsSvgItem):

    def __init__(self, parent, element, position):


        self.tintColorList = ['green',  # selected/hovering/Pri
                              'black',  # normal state
                              'yellow', # search
                              'orange', # 1st
                              'blue',   # 2nd
                              'red']    # issue

        # pri image color
        self.image = os.path.join('Images', element.lower(), 'drawing.svg')
        super(BaseElement, self).__init__(self.image)
        self.setImageColor('green')

        self.linkId        = None
        self.ueId          = None
        self.eId           = self.ueId
        self.linksFrom     = set()
        self.linksTo       = set()
        self.rd            = ''
        self.orientation   = 0
        self.parent        = parent
        self.position      = self.imageCenterToMousePosition(position)
        self.enteredDict   = {'id': self.eId}

        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable|
                      QGraphicsItem.ItemSendsScenePositionChanges)

        self.setPos(QPointF(parent.mapToScene(self.position)))
        self.setAcceptHoverEvents(True)

#------------------------------------------------------------------------------- Overrides
    def hoverEnterEvent(self, event):
        self.setImageColor('green')

    def hoverLeaveEvent(self, event):
        self.setImageColor('black')
#------------------------------------------------------------------------------- Overrides
#                                                                                ---------
#------------------------------------------------------------------------------- Sets
    def setImageColor(self, color):
        self.setElementId(QString(color))

    def setObjectGui(self, parent):
        self.gui = ParameterInputGui(self, parent, self.guiModule)
        return self.gui
#------------------------------------------------------------------------------- Sets
#                                                                                ------
#------------------------------------------------------------------------------- Custom
    def updateLinksTo(self, toEId):
        self.linksTo = set(tuple(self.linksTo) + (toEId,))

    def updateLinksFrom(self, fromEId):
        self.linksFrom = set(tuple(self.linksFrom) + (fromEId,))

    def itemChange(self, change, value):
        # whenever an item has changed we need to update the position
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.position = value.toPoint()
        return QGraphicsItem.itemChange(self, change, value)

    def imageCenterToMousePosition(self, pos):
        # when we place an image, I want the center to be where the point of the
        # mouse was and not the top left of the image.
        self.x = pos.x() - self.boundingRect().width()/2
        self.y = pos.y() - self.boundingRect().height()/2
        return QPoint(self.x, self.y)
#------------------------------------------------------------------------------- Custom

class ParameterInputGui(QWidget):

    def __init__(self, caller, parent, guiModule):

        self.caller = caller
        super(ParameterInputGui, self).__init__()
        self.ui = guiModule.Ui_Form()
        self.ui.setupUi(self)
        parent.layout().addWidget(self)

        self.ui.Save.clicked.connect(self.clickedSave)
        self.ui.Clear.clicked.connect(self.clickedClear)
        self.ui.Delete.clicked.connect(self.clickedDelete)

        self.buildDict()
        self.setData()
        self.show()


    def buildDict(self):
        self.setData()


    def clickedSave(self):
        print 'Save clicked'
        dataDict = self.getEnteredData()
        self.caller.userInputData(dataDict)


    def clickedClear(self):
        print 'Clear clicked'
        dataDict = self.clearFields()
        self.caller.userInputData(dataDict)


    def clickedDelete(self):
        print 'Delete clicked'
        self.caller.userInputData('Delete')


    def setData(self):
        d = self.caller.enteredDict
        for child in self.children():
            if str(child.__class__.__name__) == 'QLineEdit':
                child.setText(QString(d[str(child.objectName())]))
            if str(child.__class__.__name__) == 'QCheckBox':
                child.setChecked(d[str(child.objectName())])


    def clearFields(self):
        for child in self.children():
            if str(child.__class__.__name__) == 'QLineEdit':
                child.setText(QString(''))
            if str(child.objectName()) == 'id':
                child.setText(QString(str(self.caller.eId)))
            if str(child.objectName()) == 'blockFromSearch':
                child.setChecked(False)
        return self.getEnteredData()


    def getEnteredData(self):
        dataDict   = {}
        for child in self.children():
            if child.__class__.__name__ == 'QLineEdit':
                dataDict[str(child.objectName())] = str(child.text())
            if child.__class__.__name__ == 'QCheckBox':
                dataDict[str(child.objectName())] = child.isChecked()
        return dataDict


class Mux(BaseElement):
    pass


class Hybrids(BaseElement):

    def __init__(self, *args):
        super(Hybrids, self).__init__(args[0], args[1], args[2])
        self.guiModule = hybridParameterGui

    def userInputData(self, data):
        self.enteredDict = data


class LCamp(BaseElement):
    pass

class DownConverter(BaseElement):
    pass

class UpConverter(BaseElement):
    pass

class Receiver(BaseElement):
    pass

class Twt(BaseElement):
    pass

class Lna(BaseElement):
    pass

class Switch(BaseElement):
    pass

class Isolators(BaseElement):
    pass

class Circulators(BaseElement):
    pass
