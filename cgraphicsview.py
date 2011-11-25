import os
import time
import links
import elements

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4.QtSvg  import *

class CGraphicsView(QGraphicsView):
    # graphicsView
    def __init__(self, parent):
        super(CGraphicsView, self).__init__(parent)
        self.parent = parent
        self.scene = QGraphicsScene(parent)
        self.scene.setSceneRect(0.0, 0.0, 250.0, 250.0)
        self.setScene(self.scene)
        self.iComm = self.parent.parent()
        # These two vars are used to detect mouse dragging.  Initially if we
        # click to drag, we would have placed an image on the screen.  Now we
        # check to see if the two positions are == and if so then place the
        # image otherwise don't an allow dragging.
        self.mousePressPosition   = None
        self.mouseReleasePosition = None
        # keeps a list of selectedItems which is populated with
        # self.scene.selectedItems().  We save this number for this case: if we
        # have a group of selected items and click in an empty spot we want to
        # deselect the group and not place an image down.  This makes the
        # program more transparent to other programs deselection process.
        self.selectedItemHistory = []
        self.startElement        = None
        self.stopElement         = None
        self.guiInInspector      = None
        # used for click-move-click with links insted of click-drag-release
        # Theory:
        #       "Click"   if 0 build link set to 1
        #       "Move"    if 1 update link P2
        #       "Click"   if 1 set to 2
        #       "Release" if 2 make sure it's a valid location set to 0
        self.clickPhase = 0                                                    # Needs to be reset when changing modes
        
        # data for saving files                                                 
        self.lookupObj2Id = {}
        self.idList       = []

#------------------------------------------------------------------------------# mousePressEvent
    def mousePressEvent(self, event):
        super(CGraphicsView, self).mousePressEvent(event)
        if iCommGlobals.mode == "draw":
            self.mousePressEvent_Draw(event)
        elif iCommGlobals.mode == "link":
            self.mousePressEvent_Link(event)

    def mousePressEvent_Draw(self, event):
        self.mousePressPosition = event.pos()

    def mousePressEvent_Link(self, event):

        pos = QPointF(event.pos())
        try:
            item = self.scene.items(pos)[0]            
        except IndexError:
            return
        if item and item.currentPort and self.clickPhase == 0:
            
            self.line              = self.makeLine(pos)
            self.line.startElement = item
            self.line.startRect    = item.portRect
            self.line.centerLinkToPort("P1")
            self.clickPhase        = 1
            self.startElement      = item
            
        elif self.clickPhase == 1:
            self.clickPhase = 2
        else:
            self.startElement = None
#------------------------------------------------------------------------------# mousePressEvent
#                                                                              # ---------------
#------------------------------------------------------------------------------# mouseMoveEvent
    def mouseMoveEvent(self, event):
        super(CGraphicsView, self).mouseMoveEvent(event)
        if self.startElement and self.clickPhase == 1:
            x2 = event.pos().x()
            y2 = event.pos().y()
            self.line.update(QPointF(x2, y2), "P2")
            return None
#------------------------------------------------------------------------------# mouseMoveEvent
#                                                                              # -----------------
#------------------------------------------------------------------------------# mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        super(CGraphicsView, self).mouseReleaseEvent(event)
        if iCommGlobals.mode == "draw":
            self.mouseReleaseEvent_Draw(event)
        elif iCommGlobals.mode == "link":
            self.mouseReleaseEvent_Link(event)

    def mouseReleaseEvent_Draw(self, event):
        self.mouseReleasePosition = event.pos()
        self.imageControl()
        self.selectedItemHistory = self.scene.selectedItems()

    def mouseReleaseEvent_Link(self, event):

        if self.clickPhase != 2:
            # this is the first mouse release of the link build step, skip it
            return
        # attempted to make a link from nothing to somehting/nothing
        # can't be done, must start from an element

        pos = QPointF(event.pos())

        try:
            self.stopElement = self.scene.items(pos)[0]
            module = self.stopElement.__module__
        except IndexError ("No Element at that event."):
            return

        # link went to same element, remove it
        if self.startElement == self.stopElement:
            self.scene.removeItem(self.line)
            self.line         = None
            self.startElement = None

        # link started from an element and went to another element.
        elif module == "elements":
            self.stopElement      = self.scene.items(pos)[0]
            self.line.stopElement = self.stopElement
            self.line.stopRect    = self.stopElement.portRect
            self.line.centerLinkToPort("P2")
            
            self.setElementLinks()
            self.assignId(self.line)
            self.startElement.setPortConnection(self.stopElement)
            self.stopElement.setPortConnection(self.startElement)
            
            self.line         = None
            self.startElement = None

        # link ended on link element, remove it
        elif module == "links":
            self.scene.removeItem(self.line)
            self.startElement = None

        self.clickPhase = 0
#------------------------------------------------------------------------------# mouseReleaseEvent

    def setElementLinks(self):
        self.startElement.updateLinksTo(self.stopElement.eId)
        self.startElement.outerLinks.append(("P1", self.line))
        self.stopElement.updateLinksFrom(self.startElement.eId)
        self.stopElement.outerLinks.append(("P2", self.line))

    def makeLine(self, p1):
        line = links.LinkFactory(self, iCommGlobals.elementClass, p1)
        self.scene.addItem(line)
        return line

    def clickDragThreshold(self):
        tolerance = 5 # pixels
        # allow the mouse to move slightly on element placing for shakey hands
        xDelta = self.mousePressPosition.x() - self.mouseReleasePosition.x()
        yDelta = self.mousePressPosition.y() - self.mouseReleasePosition.y()
        if abs(xDelta) < tolerance and abs(yDelta) < tolerance:
            return True
        else:
            return False

    def imageControl(self):
        # if the positions are not == then this means we're draggin and we don't
        # want to place an image the start of the dragging point.
        if not self.clickDragThreshold():
            # we have made a selection box, if any elements are in that box
            # set the selection color.
            map(lambda x: x.update(), self.scene.selectedItems())
            return None

        if iCommGlobals.elementClass:
            newImage = elements.ElementFactory(self,
                                               iCommGlobals.elementClass,
                                               self.mousePressPosition)
        else:
            return None
        # check if new image will collide with other images.  there should be
        # a better way of doing this section.
        collisionTest = self.checkForCollision(newImage)

        if collisionTest and collisionTest.__module__ != 'elements':
            return None
            
        elif collisionTest:
            self.scene.clearSelection()
            collisionTest.setSelected(True)
            self.setParameterInputGui(collisionTest)
            return None

        elif (not collisionTest) and (len(self.selectedItemHistory) >= 2):
            self.scene.clearSelection()
            return None

        elif (not collisionTest) and (len(self.selectedItemHistory) == 1):
            self.scene.clearSelection()

        newImage.setSelected(True)
        newImage = self.assignId(newImage)
        self.scene.addItem(newImage)
        self.setParameterInputGui(newImage)
        
        self.updateLookup(newImage)

    def updateLookup(self, obj):
        self.lookupObj2Id[obj] = obj.eId
        self.idList.append(obj.eId)
        print obj.eId


    def setParameterInputGui(self, image):

        if self.guiInInspector:
            # clear the gui that's in Inspector
            self.guiInInspector.getData()
            self.guiInInspector.setParent(None)

        gui = image.setObjectGui(self.iComm.ui.Stack)
        gui.setData()
        self.guiInInspector = gui
        self.iComm.ui.Inspector.setFixedWidth(gui.size().width())

    def assignId(self, element):
        element.eId = str(time.time())
        return element

    def checkForCollision(self, newImage):
        # look for a way that bundles for loop with image collision.  There
        # should be something with Qt that allows this in C and not python
        for item in self.scene.items():
            if item.collidesWithItem(newImage):
                # if we had a collision, return the image, True
                return item
        # return False for no image collision
        return False
