# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\msh\OneDrive\Belgeler\the_myraf\gui\help_help_astrometrynet.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(629, 459)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser_7 = QtWidgets.QTextBrowser(Form)
        self.textBrowser_7.setMinimumSize(QtCore.QSize(611, 441))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.gridLayout.addWidget(self.textBrowser_7, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Astrometry.net"))
        self.textBrowser_7.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'verdana,arial,Bitstream Vera Sans,helvetica,sans-serif\'; font-size:12pt; color:#000000;\">If you have astronomical imaging of the sky with celestial coordinates you do not know—or do not trust—then </span><span style=\" font-family:\'verdana,arial,Bitstream Vera Sans,helvetica,sans-serif\'; font-size:12pt; font-style:italic; color:#000000;\">Astrometry.net</span><span style=\" font-family:\'verdana,arial,Bitstream Vera Sans,helvetica,sans-serif\'; font-size:12pt; color:#000000;\"> is for you. Input an image and we\'ll give you back astrometric calibration meta-data, plus lists of known objects falling inside the field of view.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'verdana,arial,Bitstream Vera Sans,helvetica,sans-serif\'; font-size:12pt; color:#000000;\">We have built this astrometric calibration service to create correct, standards-compliant astrometric meta-data for every useful astronomical image ever taken, past and future, in any state of archival disarray. We hope this will help organize, annotate and make searchable all the world\'s astronomical information.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'verdana,arial,Bitstream Vera Sans,helvetica,sans-serif\'; font-size:12pt; color:#000000;\">http://astrometry.net/</span></p></body></html>"))

