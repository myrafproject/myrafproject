# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'psf.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(626, 470)
        self.gridLayout_5 = QtWidgets.QGridLayout(Form)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.psf_display = gingaWidget(self.groupBox)
        self.psf_display.setMinimumSize(QtCore.QSize(421, 358))
        self.psf_display.setObjectName("psf_display")
        self.gridLayout.addWidget(self.psf_display, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 2, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMinimumSize(QtCore.QSize(171, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(171, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.psf_coordinates = QtWidgets.QListWidget(self.groupBox_2)
        self.psf_coordinates.setMinimumSize(QtCore.QSize(151, 0))
        self.psf_coordinates.setMaximumSize(QtCore.QSize(151, 16777215))
        self.psf_coordinates.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.psf_coordinates.setObjectName("psf_coordinates")
        self.gridLayout_2.addWidget(self.psf_coordinates, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.psf_annotation = QtWidgets.QLabel(Form)
        self.psf_annotation.setText("")
        self.psf_annotation.setObjectName("psf_annotation")
        self.gridLayout_3.addWidget(self.psf_annotation, 0, 0, 1, 1)
        self.psf_progress = QtWidgets.QProgressBar(Form)
        self.psf_progress.setProperty("value", 24)
        self.psf_progress.setObjectName("psf_progress")
        self.gridLayout_3.addWidget(self.psf_progress, 1, 0, 1, 1)
        self.psf_go = QtWidgets.QPushButton(Form)
        self.psf_go.setMinimumSize(QtCore.QSize(50, 50))
        self.psf_go.setMaximumSize(QtCore.QSize(50, 50))
        self.psf_go.setObjectName("psf_go")
        self.gridLayout_3.addWidget(self.psf_go, 0, 1, 2, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 2, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PSF"))
        self.groupBox.setTitle(_translate("Form", "Display"))
        self.groupBox_2.setTitle(_translate("Form", "Coodinates"))
        self.psf_go.setText(_translate("Form", ":go"))


from gingawidgetFile import gingaWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
