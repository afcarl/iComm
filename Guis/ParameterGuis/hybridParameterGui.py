# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hybridParameterGui.ui'
#
# Created: Mon Nov 28 11:44:55 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(259, 189)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title = QtGui.QLabel(Form)
        self.title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title.setText(QtGui.QApplication.translate("Form", "Element", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName(_fromUtf8("title"))
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.idLabel = QtGui.QLabel(Form)
        self.idLabel.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\'; font-size:9pt; color:#000000;\">ID is a unique ID that is auto assigned to the element for searching purposes; however, the ID can be overwritten to a user specified ID so long as the ID is unique.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.idLabel.setText(QtGui.QApplication.translate("Form", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.idLabel.setObjectName(_fromUtf8("idLabel"))
        self.horizontalLayout.addWidget(self.idLabel)
        self.id = QtGui.QLineEdit(Form)
        self.id.setObjectName(_fromUtf8("id"))
        self.horizontalLayout.addWidget(self.id)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 10)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rdLabel = QtGui.QLabel(Form)
        self.rdLabel.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\'; font-size:9pt; color:#000000;\">Reference designation of the element without the -JN</span><span style=\" font-family:\'arial\'; font-size:10pt; color:#000000; vertical-align:super;\">0</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.rdLabel.setText(QtGui.QApplication.translate("Form", "RD", None, QtGui.QApplication.UnicodeUTF8))
        self.rdLabel.setObjectName(_fromUtf8("rdLabel"))
        self.horizontalLayout_2.addWidget(self.rdLabel)
        self.rd = QtGui.QLineEdit(Form)
        self.rd.setObjectName(_fromUtf8("rd"))
        self.horizontalLayout_2.addWidget(self.rd)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 10)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.blockFromSearch = QtGui.QCheckBox(Form)
        self.blockFromSearch.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\'; font-size:9pt; color:#000000;\">If selected, removes element from searching algorithms. Useful for missing elements.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.blockFromSearch.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.blockFromSearch.setText(QtGui.QApplication.translate("Form", "Block From Search", None, QtGui.QApplication.UnicodeUTF8))
        self.blockFromSearch.setObjectName(_fromUtf8("blockFromSearch"))
        self.verticalLayout.addWidget(self.blockFromSearch)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.Save = QtGui.QPushButton(Form)
        self.Save.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\'; font-size:9pt; color:#000000;\">Save entered data to element object.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Save.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.Save.setObjectName(_fromUtf8("Save"))
        self.horizontalLayout_3.addWidget(self.Save)
        self.Clear = QtGui.QPushButton(Form)
        self.Clear.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\'; font-size:9pt; color:#000000;\">Set fields to default state. This will your custom ID, if set, to default.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Clear.setText(QtGui.QApplication.translate("Form", "&Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.Clear.setObjectName(_fromUtf8("Clear"))
        self.horizontalLayout_3.addWidget(self.Clear)
        self.Delete = QtGui.QPushButton(Form)
        self.Delete.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'arial\'; font-size:9pt;large; color:#000000;\">Delete element from graph.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Delete.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.Delete.setObjectName(_fromUtf8("Delete"))
        self.horizontalLayout_3.addWidget(self.Delete)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.idLabel.setBuddy(self.id)
        self.rdLabel.setBuddy(self.rd)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.id, self.rd)
        Form.setTabOrder(self.rd, self.blockFromSearch)
        Form.setTabOrder(self.blockFromSearch, self.Save)
        Form.setTabOrder(self.Save, self.Clear)
        Form.setTabOrder(self.Clear, self.Delete)

    def retranslateUi(self, Form):
        pass

