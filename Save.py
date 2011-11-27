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
                self.obj2Id(element, lookup)
                
                
    def obj2Id(self, obj, lookup):
        for port in obj.connections:
            elem   = obj.connections[port][0]
            link   = obj.connections[port][2]
            elemId = lookup[elem]
            linkId = lookup[link]
            obj.connections[port][0] = elemId
            obj.connections[port][2] = linkId
            
