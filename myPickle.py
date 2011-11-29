#~ from PyQt4.QtCore import *
#~ from PyQt4.QtGui  import *
#~ from PyQt4.QtSvg  import *

import pickle
from   links    import *
from   elements import *

class dump(object):

    def __init__(self, view, filename="current.pkl"):

        dumpDict = {}
        for element in view.scene.items():

            if element.__module__ == "elements":
                connections  = self.obj2Id(element)
                # because Qt uses top right for position we need to shift elem
                # back from center to top right.  This will take the current pos
                # and shift if off by center.  When the element is rebuilt
                # the element is shifted back by rect.center.
                position     = element.pos() + element.boundingRect().center()
                entries      = element.enteredDict
                ID           = element.eId
                module       = element.__module__
                elementType  = element.element
                mock         = MockElement(connections,
                                           position,
                                           entries,
                                           elementType,
                                           module)
                dumpDict[ID] = mock

            elif element.__module__ == "links":
                ID           = element.eId
                module       = element.__module__
                line         = element.line
                elementType  = element.element

                mock              = MockLink(line, elementType, module)
                mock.startElement = element.startElement.eId
                mock.stopElement  = element.stopElement.eId
                mock.startRect    = element.startRect
                mock.stopRect     = element.stopRect

                dumpDict[ID] = mock

        dumpfile = open(filename, "wb")
        pickle.dump(dumpDict, dumpfile)
        dumpfile.close()

    def obj2Id(self, obj):
        copy = {}
        for port in obj.connections:
            connections = obj.connections[port][:]

            try:
                elemId = connections[0].eId
            except:
                elemId = None

            try:
                linkId = connections[2].eId
            except:
                linkId = None

            connections[0] = elemId
            connections[2] = linkId
            copy[port]     = connections
        return copy

class load(object):

    def __init__(self, view, filename="current.pkl"):

        self.view  = view
        self.scene = view.scene

        fileload = open(filename, "rb")
        items    = pickle.load(fileload)

        lookup, elemList = self.buildElements(items)
        self.setConnections(lookup)
        self.setElementsToScene(elemList)

    def setElementsToScene(self, elemList):
        for elem in elemList:
            self.view.scene.addItem(elem)

    def buildElements(self, items):

        lookup = {None: None}
        elemList = []

        for ID in items:
            obj = items[ID]
            if obj.module == "elements":
                element  = obj.element
                position = obj.position
                elem     = ElementFactory(self.view, element, position)

                elem.eId         = ID
                elem.connections = obj.connections
                elem.enteredDict = obj.entries
                lookup[ID] = elem
                self.view.scene.addItem(elem)

            elif obj.module == "links":
                element    = obj.element
                start      = obj.line.p1()
                stop       = obj.line.p2()
                link       = LinkFactory(self.view, element, start, stop)
                link.eId   = ID

                link.startElement = obj.startElement
                link.stopElement  = obj.stopElement
                link.startRect    = obj.startRect
                link.stopRect     = obj.stopRect
                lookup[ID]        = link
                self.view.scene.addItem(link)
            else:
                return
        return lookup, elemList

    def setConnections(self, lookup):

        for item in self.scene.items():
            if item.__module__ == "elements":
                self.id2Obj(item, lookup)
            elif item.__module__ == "links":
                item.startElement = lookup[item.startElement]
                item.stopElement  = lookup[item.stopElement]

    def id2Obj(self, obj, lookup):
        for port in obj.connections:
            current = obj.connections[port]
            element = current[0]
            link    = current[2]
            current[0] = lookup[element]
            current[2] = lookup[link]

class MockLink(object):

    def __init__(self, line, element, module):

        self.element = element
        self.module  = module

        self.line    = line


class MockElement(object):

    def __init__(self, connections, position, entries, element, module):

        self.element = element
        self.module  = module

        self.connections = connections
        self.position    = position
        self.entries     = entries

