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
                self.saveElement(element, lookup)
                
                
    def saveElement(self, obj, lookup):
        print obj
        print obj.__dict__
