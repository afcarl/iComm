# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sat Nov 12 12:08:29 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_view(object):
    def setupUi(self, view):
        view.setObjectName(_fromUtf8("view"))
        view.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(view)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphicsView = QtGui.QGraphicsView(view)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)

        self.retranslateUi(view)
        QtCore.QMetaObject.connectSlotsByName(view)

    def retranslateUi(self, view):
        view.setWindowTitle(QtGui.QApplication.translate("view", "Form", None, QtGui.QApplication.UnicodeUTF8))

