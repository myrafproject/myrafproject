# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\msh\OneDrive\Belgeler\the_myraf\gui\help_help_alipy.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(702, 509)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser_5 = QtWidgets.QTextBrowser(Form)
        self.textBrowser_5.setMinimumSize(QtCore.QSize(684, 491))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.gridLayout.addWidget(self.textBrowser_5, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Alipy"))
        self.textBrowser_5.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349; background-color:#ffffff;\">This is a python package to quickly, automatically, and robustly identify geometrical transforms between optical astronomical images, using only field stars. The images can have different pixel sizes, orientations, pointings and filters.</span></p>\n"
"<p style=\" margin-top:10px; margin-bottom:5px; margin-left:0px; margin-right:10px; -qt-block-indent:0; text-indent:0px; background-color:#eeeeee;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; font-weight:600; color:#3e4349;\">Note</span><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\">alipy is personal code, and work in progress... The package is already very useful for me, and I hope it will be for you, but don’t expect </span><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; font-style:italic; color:#3e4349;\">too</span><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\"> much neither. Any feedback and wishlists are highly welcome !</span></p>\n"
"<p style=\" margin-top:8px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\">Summary of what alipy does for you :</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\" style=\" margin-top:3px; margin-bottom:0px; margin-left:30px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Run SExtractor (see Installation) on the images to get individual source catalogs.</li>\n"
"<li style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:30px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Identify corresponding asterisms, roughly following Lang et al. (2010) aka astrometry.net.</li>\n"
"<li style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\" style=\" margin-top:0px; margin-bottom:10px; margin-left:30px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Use this identification to match catalogs, align the images (either directly with scipy, or pyraf geomap/gregister), ...</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349; background-color:#ffffff;\">Next stop : a quick look at the</span><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349;\"> </span><span style=\" font-size:12pt;\">Tutorial.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349; background-color:#ffffff;\">Last build of this documentation : April 09, 2013.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:12pt; color:#3e4349; background-color:#ffffff;\">https://obswww.unige.ch/~tewes/alipy/</span></p></body></html>"))

