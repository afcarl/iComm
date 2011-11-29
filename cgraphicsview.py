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
        
        self.iComm                = parent.parent()
        self.mousePressPosition   = None
        self.mouseReleasePosition = None
        self.selectedItemHistory  = []
        self.startElement         = None
        self.guiInInspector       = None
        self.scene                = QGraphicsScene(parent)
        self.lookupObj2Id         = {None: None}
        self.idList               = []
        self.clickPhase           = 0                                                    # Needs to be reset when changing modes
        # used for click-move-click with links insted of click-drag-release
        # Theory:
        #       "Click"   if 0 build link set to 1
        #       "Move"    if 1 update link P2
        #       "Click"   if 1 set to 2
        #       "Release" if 2 make sure it's a valid location set to 0
        self.scene.setSceneRect(0.0, 0.0, 250.0, 250.0)
        self.setScene(self.scene)

        self.line = None
#------------------------------------------------------------------------------# mousePressEvent
    def mousePressEvent(self, event):
        super(CGraphicsView, self).mousePressEvent(event)
        if self.iComm.mode in ["draw", None]:
            self.mousePressEvent_Draw(event)
        elif self.iComm.mode == "link":
            self.mousePressEvent_Link(event)

    def mousePressEvent_Draw(self, event):
        self.mousePressPosition = event.pos()

    def mousePressEvent_Link(self, event):

        pos = QPointF(event.pos())
        try:
            item = self.scene.items(pos)[0]
            port = item.getCurrentPort(item.mapFromParent(pos))
        except IndexError:
            return
        except AttributeError:
            self.startElement = None
            self.clickPhase   = 0
            try:
                self.scene.removeItem(self.line)
            except AttributeError:
                pass
            return

        if not port:
            return
        elif item and self.clickPhase == 0:
            self.line              = self.makeLine(pos)
            self.line.startElement = item
            self.startPort         = port[0]
            self.line.startRect    = port[1]
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
        if self.iComm.mode in ["draw", None]:
            self.mouseReleaseEvent_Draw(event)
        elif self.iComm.mode == "link":
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
            item   = self.scene.items(pos)[0]
            port   = item.getCurrentPort(item.mapFromParent(pos))
            module = item.__module__
        except IndexError ("No Element at that event."):
            return
        # link went to same element, remove it
        if self.startElement == item:
            self.scene.removeItem(self.line)
            self.line         = None
            self.startElement = None
        # link started from an element and went to another element.
        elif module == "elements":
            self.line.stopElement = item
            self.line.stopRect    = port[1]
            self.line.centerLinkToPort("P2")
            self.assignId(self.line)

            args = (port[0], self.startElement, self.startPort, self.line, "P2")
            item.setPortConnection(args)

            args = (self.startPort, item, port[0], self.line, "P1")
            self.startElement.setPortConnection(args)

            self.line         = None
            self.startElement = None

        # link ended on link element, remove it
        elif module == "links":
            self.scene.removeItem(self.line)
            self.startElement = None
        self.clickPhase = 0
#------------------------------------------------------------------------------# mouseReleaseEvent
    def keyPressEvent(self, event):
        super(CGraphicsView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Escape and self.line:
            self.scene.removeItem(self.line)
            self.line = None
            self.clickPhase = 0

    def makeLine(self, p1):
        line = links.LinkFactory(self, self.iComm.elementClass, p1)
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
            
        if self.iComm.elementClass:
            newImage = elements.ElementFactory(self,
                                               self.iComm.elementClass,
                                               self.mousePressPosition)
            # check if new image will collide with other images.
            collisionTest = self.checkForCollision(newImage)
            
        elif self.iComm.mode == None:
            pos = QPointF(self.mousePressPosition)
            try:
                collisionTest = self.scene.items(pos)[0]
            except IndexError:
                # in free mode and clicked with an empty scene
                return None
        else:
            return None


        if collisionTest and collisionTest.__module__ != "elements":
            newImage.remove()
            return None

        elif collisionTest or self.iComm.mode == None:
            self.scene.clearSelection()
            collisionTest.setSelected(True)
            self.setParameterInputGui(collisionTest)
            try:
                newImage.remove()
            except UnboundLocalError:
                # in Free mode from link and clicked on an element
                pass
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
        newImage.update()

    def setParameterInputGui(self, image):
        if self.guiInInspector:
            # clear the gui that's in Inspector
            # I dont fully understand this.  For some reason, without the try

            # statment, if you reload edit, reload edit again it will error out
            # referencing a text obj that is not longer valid.  I can't find out
            # why.  This appears to fix the problem though.
            try:
                self.guiInInspector.getData()
            except:
                pass
            self.guiInInspector.setParent(None)

        gui = image.setObjectGui(self.iComm.ui.Stack)
        self.guiInInspector = gui
        self.iComm.ui.Inspector.setFixedWidth(gui.size().width())

    def assignId(self, element):
        element.eId = str(time.time())
        element.enteredDict["id"] = element.eId
        return element

    def checkForCollision(self, newImage):
        # look for a way that bundles for loop with image collision.  There
        # should be something with Qt that allows this in C and not python
        for item in self.scene.items():
            if item.collidesWithItem(newImage):
                return item
        return False

if __name__ == "__main__":
    import iComm
    iComm.RunGui()
