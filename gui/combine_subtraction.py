# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\msh\OneDrive\Belgeler\the_myraf\gui\combine_subtraction.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(369, 163)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setEnabled(False)
        self.textEdit.setMinimumSize(QtCore.QSize(351, 31))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 31))
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(41, 16))
        self.label.setMaximumSize(QtCore.QSize(41, 16))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.subtract_image1 = QtWidgets.QComboBox(Form)
        self.subtract_image1.setObjectName("subtract_image1")
        self.gridLayout.addWidget(self.subtract_image1, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(41, 16))
        self.label_2.setMaximumSize(QtCore.QSize(41, 16))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.subtract_image2 = QtWidgets.QComboBox(Form)
        self.subtract_image2.setObjectName("subtract_image2")
        self.gridLayout.addWidget(self.subtract_image2, 2, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.subtract_go = QtWidgets.QPushButton(Form)
        self.subtract_go.setMinimumSize(QtCore.QSize(50, 50))
        self.subtract_go.setMaximumSize(QtCore.QSize(50, 50))
        self.subtract_go.setObjectName("subtract_go")
        self.gridLayout.addWidget(self.subtract_go, 4, 2, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(292, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Subtraction"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Result = Image1 - Image2</span></p></body></html>"))
        self.label.setText(_translate("Form", "Image 1"))
        self.label_2.setText(_translate("Form", "Image 2"))
        self.subtract_go.setText(_translate("Form", ":g..."))

