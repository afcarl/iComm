import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

class LinkFactory(QGraphicsLineItem):

    # This class allows us to init a class from a string
    def __init__(self, parent, element, start, stop):
        # remove all marks and "_" because our classes do not have these chars.
        # check for the instance in __main__
        self.__class__ = getattr(sys.modules[__name__], element)
        self.__class__.__init__(self, parent, element, start, stop)

class BaseLink(QGraphicsLineItem):

    def __init__(self, parent, element, start, stop):

        self.start         = QPointF(start)
        self.stop          = QPointF(stop)
        self.line = QLineF(self.start, self.stop)

        super(BaseLink, self).__init__(self.line)

        self.eId           = None
        self.rd            = ''
        self.parent        = parent
        self.isHighlighted = True

        self.color = Qt.white

        self.setFlags(QGraphicsItem.ItemIsSelectable|
                      QGraphicsItem.ItemIsMovable|
                      QGraphicsItem.ItemSendsScenePositionChanges)

        self.setZValue(-1)
        

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.line)

    def itemChange(self, change, value):
        # whenever an item has changed we need to take now and update the position
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.position = value.toPoint()
        return QGraphicsItem.itemChange(self, change, value)

    def setImageHighlighting(self, condition, color=Qt.green):
        self.isHighlighted = condition
        if condition:
            self.color = color
            self.update()
        else:
            self.color = Qt.white
            self.update()
        
class Coax(BaseLink):
    print 'Making coax link'
    pass

class Waveguide(BaseLink):
    print 'Making waveguid link'
    pass
