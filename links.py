import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

class LinkFactory(QGraphicsLineItem):

    # This class allows us to init a class from a string
    def __init__(self, parent, element, start, stop=None):
        # remove all marks and "_" because our classes do not have these chars.
        # check for the instance in __main__
        self.__class__ = getattr(sys.modules[__name__], element)
        self.__class__.__init__(self, parent, element, start, stop)

class BaseLink(QGraphicsLineItem):

    def __init__(self, parent, element, start, stop):

        self.element  = element
        self.start    = QPointF(start)
        if stop:
            self.line = QLineF(self.start, stop)
        else:
            self.line = QLineF(self.start, self.start)

        super(BaseLink, self).__init__(self.line)

        self.eId           = None
        self.rd            = ''
        self.parent        = parent
        self.isHighlighted = True

        self.startElement  = None
        self.stopElement   = None
        self.startRect     = None
        self.stopRect      = None

        self.enteredDict   = {"id": self.eId}
        self.color = Qt.white
        self.setFlags(QGraphicsItem.ItemSendsScenePositionChanges)
        self.setZValue(-1)

        self._setPen(self.color, 3)

    def _setPen(self, color, width):
        brush = QBrush(color)
        pen   = QPen(brush, width)
        self.setPen(pen)

    def setImageHighlighting(self, condition, color=Qt.green):
        self.isHighlighted = condition
        if condition:
            self.color = color
            self.update()
        else:
            self.color = Qt.white
            self.update()

    def centerLinkToPort(self, side):
        if side == "P1":
            item  = self.startElement
            point = self.startRect.center()
        elif side == "P2":
            item  = self.stopElement
            point = self.stopRect.center()
        newPoint  = item.mapToScene(point)
        self.update(newPoint, side)

    def update(self, pos, side):
        getattr(self.line, "set" + side).__call__(pos)
        self.setLine(self.line)

class Coax(BaseLink):
    pass

class Waveguide(BaseLink):
    pass
