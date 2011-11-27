from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4.QtSvg  import *

import pickle

class Pkl(object):

    def dump(self, view, filename='current.pkl'):
        
        lookup = view.lookupObj2Id
        idList = view.idList
        
        for element in view.scene.items():
            if element.__module__ == 'elements':
                connections = self.obj2Id(element, lookup)
                position    = element.pos()
                
                
    def obj2Id(self, obj, lookup):
        copy = {}
        for port in obj.connections:
            connections    = obj.connections[port][:]
            elemId         = lookup[connections[0]]
            linkId         = lookup[connections[2]]
            connections[0] = elemId
            connections[2] = linkId
            copy[port]     = connections
        return copy
