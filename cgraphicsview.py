import os
import links
import elements

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

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

#------------------------------------------------------------------------------# mousePressEvent
    def mousePressEvent(self, event):
        super(CGraphicsView, self).mousePressEvent(event)
        if iCommGlobals.mode == 'draw':
            self.mousePressEvent_Draw(event)
        elif iCommGlobals.mode == 'link':
            self.mousePressEvent_Link(event)

    def mousePressEvent_Draw(self, event):
        self.mousePressPosition = event.pos()        

    def mousePressEvent_Link(self, event):
        if self.scene.items(QPointF(event.pos())):
            self.p1 = QPointF(event.pos())
            self.x1 = event.pos().x()
            self.y1 = event.pos().y()
            self.startElement = self.scene.items(self.p1)[0]
            self.line = self.makeLine()
        else:
            self.startElement = None
#------------------------------------------------------------------------------# mousePressEvent
#       
#------------------------------------------------------------------------------# mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        super(CGraphicsView, self).mouseReleaseEvent(event)
        if iCommGlobals.mode == 'draw':
            self.mouseReleaseEvent_Draw(event)
        elif iCommGlobals.mode == 'link':
            self.mouseReleaseEvent_Link(event)
        
    def mouseReleaseEvent_Draw(self, event):
        self.mouseReleasePosition = event.pos()
        self.imageControl()
        self.selectedItemHistory = self.scene.selectedItems()

    def mouseReleaseEvent_Link(self, event):
        # attempted to make a link from nothing to somehting/nothing
        # can't be done, must start from an element
        try:
            module = self.scene.items(QPointF(event.pos()))[0].__module__
            self.stopElement = self.scene.items(QPointF(event.pos()))[0]
        except IndexError:
            return
        # link started from an element and went to another element.
        if module == 'elements' and self.startElement != self.stopElement:
            self.stopElement  = self.scene.items(QPointF(event.pos()))[0]
            self.setElementLinks()
            self.line         = None
            self.startElement = None
            
        # link ended on link element, remove it
        elif module == 'links':
            self.scene.removeItem(self.line)
            self.startElement = None
        # link went to same element, remove it
        elif self.startElement == self.stopElement:
            self.scene.removeItem(self.line)
            
#------------------------------------------------------------------------------# mouseReleaseEvent
#
#------------------------------------------------------------------------------# mouseMoveEvent
    def mouseMoveEvent(self, event):
        if self.startElement:            
            x2 = event.pos().x()
            y2 = event.pos().y()
            self.line.setLine(self.x1, self.y1, x2, y2)
            return None
        super(CGraphicsView, self).mouseMoveEvent(event)
#------------------------------------------------------------------------------# mouseMoveEvent

    def setElementLinks(self):
        self.startElement.updateLinksTo(self.stopElement.eId)
        self.startElement.outerLinks.append(('P1', self.line))
        self.stopElement.updateLinksFrom(self.startElement.eId)
        self.stopElement.outerLinks.append(('P2', self.line))

#------------------------------------------------------------------------------# Move to links.py
    def setLineToImagePortPosition(self):
        # this function will set the line to the J port wanted but for now
        # will set to center

        def newPoints(elem):
            centerX = elem.boundingRect().center().x()
            centerY = elem.boundingRect().center().y()
            posX    = elem.pos().x()
            posY    = elem.pos().y()
            return QPointF(posX + centerX, posY + centerY)
#------------------------------------------------------------------------------# Move to links.py

        points = [newPoints(x) for x in (self.startElement, self.stopElement)]
        return dict(zip(('Start', 'Stop'), points))

    def makeLine(self):
        #linePoints = self.setLineToImagePortPosition()
        line = links.LinkFactory(self, iCommGlobals.elementClass, self.p1)
        self.scene.addItem(line)
        return line

    def mousePositionTolerance(self):
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
        if not self.mousePositionTolerance():
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

        if collisionTest:
            self.scene.clearSelection()
            collisionTest.setSelected(True)
            self.setParameterInputGui(collisionTest)
            return None

        if (not collisionTest) and (len(self.selectedItemHistory) >= 2):
            self.scene.clearSelection()
            return None

        if (not collisionTest) and (len(self.selectedItemHistory) == 1):
            self.scene.clearSelection()

        newImage.setSelected(True)
        newImage = self.setElementId(newImage)
        self.scene.addItem(newImage)
        self.setElementId(newImage)
        self.setParameterInputGui(newImage)

    def setParameterInputGui(self, image):

        if self.guiInInspector:
            # clear the gui that's in Inspector
            self.guiInInspector.getData()
            self.guiInInspector.setParent(None)

        gui = image.setObjectGui(self.iComm.ui.Stack)
        gui.setData()
        self.guiInInspector = gui
        self.iComm.ui.Inspector.setFixedWidth(gui.size().width())

    def setElementId(self, element):
        # set the eId of the element
        element.eId = str(len(self.scene.items()))
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
