#~ from PyQt4.QtCore import *
#~ from PyQt4.QtGui  import *
#~ from PyQt4.QtSvg  import *

import pickle

class Pickle(object):

    def dump(self, view, filename="current.pkl"):

        lookup = view.lookupObj2Id
        idList = view.idList

        dumpDict = {}

        for element in view.scene.items():
            if element.__module__ == "elements":
                connections  = self.obj2Id(element, lookup)
                position     = element.pos()
                entries      = element.enteredDict
                ID           = element.eId
                elementType  = element.element
                mock         = MockElement(connections,
                                           position,
                                           entries,
                                           elementType)
                dumpDict[ID] = mock

            elif element.__module__ == "links":
                print "links"

        dumpfile = open(filename, "wb")
        pickle.dump(dumpDict, dumpfile)
        dumpfile.close()

        print "Saved"

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


class MockElement(object):

    def __init__(self, connections, position, entries, element):

        self.connections = connections
        self.potition    = position
        self.entries     = entries
        self.element     = element
