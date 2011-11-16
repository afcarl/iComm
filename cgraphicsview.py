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
        self.mousePressPosition = None
        self.mouseReleasePosition = None
        # keeps a list of selectedItems which is populated with
        # self.scene.selectedItems().  We save this number for this case: if we
        # have a group of selected items and click in an empty spot we want to
        # deselect the group and not place an image down.  This makes the
        # program more transparent to other programs deselection process.
        self.selectedItemHistory = []
        self.startElement = None
        self.stopElement = None

        self.guiInInspector = None

    def mousePressEvent(self, event):
        if iCommGlobals.mode == 'draw':
            super(CGraphicsView, self).mousePressEvent(event)
            self.mousePressPosition = event.pos()
        elif iCommGlobals.mode == 'link':

            if self.scene.items(QPointF(event.pos())):
                self.startElement = self.scene.items(QPointF(event.pos()))[0]
            else:
                self.startElement = None


    def mouseReleaseEvent(self, event):
        if iCommGlobals.mode == 'draw':
            super(CGraphicsView, self).mouseReleaseEvent(event)
            self.mouseReleasePosition = event.pos()
            self.imageControl()
            self.selectedItemHistory = self.scene.selectedItems()

        elif iCommGlobals.mode == 'link':
            if self.startElement and self.scene.items(QPointF(event.pos())):
                self.stopElement = self.scene.items(QPointF(event.pos()))[0]
            else:
                return None

            linePoints = self.setLineToImagePortPosition()
            self.setElementLinks()
            link = links.LinkFactory(self,
                              iCommGlobals.elementClass,
                              linePoints['Start'],
                              linePoints['Stop'])
            self.scene.addItem(link)

    def setElementLinks(self):

        self.startElement.updateLinksTo(self.stopElement.eId)
        self.stopElement.updateLinksFrom(self.startElement.eId)

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
