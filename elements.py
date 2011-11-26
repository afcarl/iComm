import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from Guis.ParameterGuis import hybridParameterGui
from rdtext import RdText

class ElementFactory(QGraphicsSvgItem):

    # This class allows us to init a class from a string
    def __init__(self, parent, element, pos):
        # parent  := parent obj which is always QGraphicsView for iComm
        # element := string of the element class that we want to initilize
        # pos     := element pos in QPointF form
        element = re.sub("(-|_)", "", element)
        self.__class__ = getattr(sys.modules[__name__], element)
# -----------------------------------------------------------------------------# remove when element images are made
        # For testing only
        element = "test_switch"
        # For testing only
# -----------------------------------------------------------------------------# remove when element images are made
        self.__class__.__init__(self, parent, element, pos)

class BaseElement(QGraphicsSvgItem):

    def __init__(self, parent, element, position):
        self.image = os.path.join("Images", element.lower(), "drawing.svg")
        super(BaseElement, self).__init__(self.image)

        self.setImageColor("green")     # set element selected color
        self.setPos(self.setImageCenter(position))


        self.parent      = parent     # referance to view
        self.ueId        = None       # unique ID assigned by the program
        self.eId         = self.ueId  # custom ID assigned by the user
        self.rd          = ""         # RD in parent form
        self.enteredDict = {"id": self.eId} # gui widget entries

        self.freshGui    = True
        self.setText()

        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable|
                      QGraphicsItem.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)
#------------------------------------------------------------------------------# Overrides
    def hoverEnterEvent(self, event):
        self.setImageColor("green")

    def hoverMoveEvent(self, event):
        point = QPointF(event.pos())
        self.getCurrentPort(point)
        
    def hoverLeaveEvent(self, event):
        self.setImageColor("black")
#------------------------------------------------------------------------------# Overrides
#                                                                              # ---------
#------------------------------------------------------------------------------# Sets
    def setPortConnection(self, element, line, side):
        connections = (element, element.currentPort, line, side)
        self.connections[self.currentPort] = connections

    def setImageColor(self, color):
        self.setElementId(QString(color))

    def setObjectGui(self, parent):
        self.gui = ParameterInputGui(self, parent, self.guiModule)
        self.freshGui = False
        return self.gui

    def setImageCenter(self, pos):
        x = pos.x() - self.boundingRect().width()/2
        y = pos.y() - self.boundingRect().height()/2
        return QPointF(x, y)

    def setText(self):
        topRight    = self.mapToScene(self.boundingRect().topRight())
        self.rdText = RdText(self.rd, topRight)
        self.parent.scene.addItem(self.rdText)
#------------------------------------------------------------------------------# Sets
#                                                                              # ------
#------------------------------------------------------------------------------# Custom

    def itemChange(self, change, value):
        # whenever an item has changed we need to update the position
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.setPos(QPointF(value.toPoint())) # update image position
            self.updateLinkPositions()
            self.updateRdTextPositions()
        return QGraphicsItem.itemChange(self, change, value)

    def updateLinkPositions(self):
        # should look into setting line as child item to element, if possible,
        # this may simplify line update.
        # go through every port of the element and update everything
        # link is the line that needs to be updated
        # side is the side of the line that need to be updated
        for port in self.connections:
            link = self.connections[port][2]
            if not link:
                continue
            side = self.connections[port][3]
            link.centerLinkToPort(side)

    def updateRdTextPositions(self):
        topRight = self.boundingRect().topRight()
        topRight = self.mapToScene(topRight)
        self.rdText.setPosition(topRight)

    def getCurrentPort(self, point):
        for port in self.portRects:
            if self.portRects[port].contains(point):
                self.setElementId(QString(port))
                return (port, self.portRects[port])
        self.setElementId(QString("center"))
        self.currentPort = None
        return None

#------------------------------------------------------------------------------#               Move to another module? v
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
        self.caller.userInputData("Delete")
#------------------------------------------------------------------------------- Clicks
#                                                                                -------------
#------------------------------------------------------------------------------- Data handlers
    def setData(self):
        d = self.caller.enteredDict
        for child in self.children():
            if str(child.__class__.__name__) == "QLineEdit":
                child.setText(QString(d[str(child.objectName())]))

            if str(child.__class__.__name__) == "QCheckBox":
                child.setChecked(d[str(child.objectName())])

    def clearFields(self):
        dataDict = {}
        for child in self.children():
            if str(child.__class__.__name__) == "QLineEdit":
                child.setText(QString(""))
                dataDict[str(child.objectName())] = ""

            if str(child.objectName()) == "id":
                child.setText(QString(self.caller.eId))
                dataDict["id"] = self.caller.eId

            if str(child.objectName()) == "blockFromSearch":
                child.setChecked(False)
                dataDict[str(child.objectName())] = False
        self.caller.updateEnteredDict(dataDict)
        return dataDict

    def getData(self):
        dataDict   = {}
        for child in self.children():
            if child.__class__.__name__ == "QLineEdit":
                dataDict[str(child.objectName())] = str(child.text())

            if child.__class__.__name__ == "QCheckBox":
                dataDict[str(child.objectName())] = child.isChecked()
        self.caller.updateEnteredDict(dataDict)
        return dataDict
#------------------------------------------------------------------------------#               Move to another module? ^

class Hybrids(BaseElement):

    def __init__(self, *args):
        super(Hybrids, self).__init__(args[0], args[1], args[2])
        self.guiModule   = hybridParameterGui
        self.portRects   = self.getPortRects()
        
        # key   == current element's J port
        # value == element connected to 
        #          port of element connnected to
        #          coax connecting them
        self.connections = {"J1" : (None, None, None, None),
                            "J2" : (None, None, None, None),
                            "J3" : (None, None, None, None),
                            "J4" : (None, None, None, None)}

    def getPortRects(self):
        # rect of the ports relative to the image in image coordinates.        # portLocations for switches (testing)
        # use QPointF because event.pos == QPointF and rect.contains needs F
        # These rects are defined when the image is made.  Must translate pos
        # from when drawing image to here.
        # this is the initial state run time the can change to represent the
        # block diagram.
        #                           x   y  w  h
        portRects = {"J1" : QRectF(10, 20, 9, 9),
                     "J2" : QRectF(20, 10, 9, 9),
                     "J3" : QRectF(10,  0, 9, 9),
                     "J4" : QRectF( 0, 10, 9, 9)}
        return portRects
#------------------------------------------------------------------------------# portLocations for switches (testing)

    def updateEnteredDict(self, data):
        self.enteredDict = data
        for attr in data:
            setattr(self, attr, data[attr])        
        self.rdText.update(self.enteredDict["rd"])


'''
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

class Mux(BaseElement):
    pass
'''
