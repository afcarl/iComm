import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from Guis.ParameterGuis import hybridParameterGui

class ElementFactory(QGraphicsSvgItem):

    # This class allows us to init a class from a string
    def __init__(self, parent, element, pos):
        # parent  := parent obj which is always QGraphicsView for iComm
        # element := string of the element class that we want to initilize
        # pos     := element pos in QPointF form
        element = re.sub('(-|_)', '', element)
        self.__class__ = getattr(sys.modules[__name__], element)
# ------------------------------------------------------------------------------ remove when element images are made
        # For testing only
        element = 'test'
        # For testing only
# ------------------------------------------------------------------------------ remove when element images are made
        self.__class__.__init__(self, parent, element, pos)


class BaseElement(QGraphicsSvgItem):

    def __init__(self, parent, element, position):
        self.image = os.path.join('Images', element.lower(), 'drawing.svg')
        super(BaseElement, self).__init__(self.image)
        self.setImageColor('green')     # set element selected color

        self.parent        = parent     #                                        do I really need this?
        self.ueId          = None       # unique ID assigned by the program
        self.eId           = self.ueId  # custom ID assigned by the user
        self.linksFrom     = set()      # RDs of elements upstream w/-J#
        self.linksTo       = set()      # RDs of elements downstream w/-J#
        self.rd            = ''         # RD in parent form
        self.enteredDict   = {'id': self.eId} # gui widget entries
        self.position      = self.setImageCenter(position)

        self.outerLinks    = [] # link object refgerance between elements

        # Monitor these flags
        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable|
                      QGraphicsItem.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)
        # map to local coordinates
        self.setPos(parent.mapToScene(self.position))

#------------------------------------------------------------------------------- Overrides
    def hoverEnterEvent(self, event):
        # when mouse enters element change color
        self.setImageColor('green')

    def hoverLeaveEvent(self, event):
        # when mouse leaves element change color back to normal
        self.setImageColor('black')
#------------------------------------------------------------------------------- Overrides
#                                                                                ---------
#------------------------------------------------------------------------------- Sets
    def setImageColor(self, color):
        self.setElementId(QString(color))

    def setObjectGui(self, parent):
        self.gui = ParameterInputGui(self, parent, self.guiModule)
        self.freshGui = False
        return self.gui

    def setImageCenter(self, pos):
        # when we place an image, I want the center to be where the point of the
        # mouse was and not the top left of the image.
        self.x = pos.x() - self.boundingRect().width()/2
        self.y = pos.y() - self.boundingRect().height()/2
        return QPoint(self.x, self.y)
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
            self.updateLinkPositions(value)
            self.position = value.toPoint()
        return QGraphicsItem.itemChange(self, change, value)

    def updateLinkPositions(self, value):

        self.tValue = value     #----------------------------------------------- TESTING

        valuePoint = value.toPointF()
        dx = valuePoint.x() - self.position.x()
        dy = valuePoint.y() - self.position.y()
        delta = QPointF(dx, dy)


        for side, link in self.outerLinks:

            self.tlink = link   #----------------------------------------------- TESTING

            linePoint = getattr(link.line, side.lower()).__call__()
            newPoint = linePoint + delta
            getattr(link.line, 'set' + side).__call__(newPoint)
            link.setLine(link.line)

#-------------------------------------------------------------------------------               Move to another module? v
class ParameterInputGui(QWidget):

    def __init__(self, caller, parent, guiModule):
        # caller    := object calling this class
        # parent    := referance to objInspect
        # guiModule := gui module that is associated with caller
        super(ParameterInputGui, self).__init__()
        self.caller = caller # referance to the class calling
        self.ui     = guiModule.Ui_Form()
        self.ui.setupUi(self)
        # set widget to layout to allow for widget resizing
        parent.layout().addWidget(self)

        self.ui.Save.clicked.connect(self.clickedSave)
        self.ui.Clear.clicked.connect(self.clickedClear)
        self.ui.Delete.clicked.connect(self.clickedDelete)

        if caller.freshGui:
            # if this is the first time we're placing the gui for this element
            # we will clear the fields to build dict otherwise we'll set data
            self.clearFields()
        self.setData()
        self.show()

    def buildDict(self):
        pass

#------------------------------------------------------------------------------- Clicks
    def clickedSave(self):
        dataDict = self.getData()
        self.caller.updateEnteredDict(dataDict)

    def clickedClear(self):
        dataDict = self.clearFields()
        self.caller.updateEnteredDict(dataDict)

    def clickedDelete(self):
        self.caller.userInputData('Delete')
#------------------------------------------------------------------------------- Clicks
#                                                                                -------------
#------------------------------------------------------------------------------- Data handlers
    def setData(self):
        d = self.caller.enteredDict
        print d
        for child in self.children():
            if str(child.__class__.__name__) == 'QLineEdit':
                child.setText(QString(d[str(child.objectName())]))

            if str(child.__class__.__name__) == 'QCheckBox':
                child.setChecked(d[str(child.objectName())])

    def clearFields(self):
        dataDict = {}
        for child in self.children():
            if str(child.__class__.__name__) == 'QLineEdit':
                child.setText(QString(''))
                dataDict[str(child.objectName())] = ''

            if str(child.objectName()) == 'id':
                child.setText(QString(self.caller.eId))
                dataDict['id'] = self.caller.eId

            if str(child.objectName()) == 'blockFromSearch':
                child.setChecked(False)
                dataDict[str(child.objectName())] = False
        self.caller.updateEnteredDict(dataDict)
        return dataDict

    def getData(self):
        dataDict   = {}
        for child in self.children():
            if child.__class__.__name__ == 'QLineEdit':
                dataDict[str(child.objectName())] = str(child.text())

            if child.__class__.__name__ == 'QCheckBox':
                dataDict[str(child.objectName())] = child.isChecked()
        self.caller.updateEnteredDict(dataDict)
        return dataDict
#-------------------------------------------------------------------------------               Move to another module? ^


class Mux(BaseElement):
    pass

class Hybrids(BaseElement):

    def __init__(self, *args):
        super(Hybrids, self).__init__(args[0], args[1], args[2])
        self.guiModule = hybridParameterGui
        self.freshGui = True

    def updateEnteredDict(self, data):
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
