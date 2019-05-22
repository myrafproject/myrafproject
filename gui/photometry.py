# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'photometry.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(636, 467)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.photometry_display = gingaWidget(self.groupBox)
        self.photometry_display.setMinimumSize(QtCore.QSize(421, 358))
        self.photometry_display.setObjectName("photometry_display")
        self.gridLayout.addWidget(self.photometry_display, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMinimumSize(QtCore.QSize(171, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(171, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.photometry_coordinates = QtWidgets.QListWidget(self.groupBox_2)
        self.photometry_coordinates.setMinimumSize(QtCore.QSize(151, 0))
        self.photometry_coordinates.setMaximumSize(QtCore.QSize(151, 16777215))
        self.photometry_coordinates.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.photometry_coordinates.setObjectName("photometry_coordinates")
        self.gridLayout_2.addWidget(self.photometry_coordinates, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.photometry_annotation = QtWidgets.QLabel(Form)
        self.photometry_annotation.setText("")
        self.photometry_annotation.setObjectName("photometry_annotation")
        self.gridLayout_3.addWidget(self.photometry_annotation, 0, 0, 1, 1)
        self.photometry_progress = QtWidgets.QProgressBar(Form)
        self.photometry_progress.setProperty("value", 24)
        self.photometry_progress.setObjectName("photometry_progress")
        self.gridLayout_3.addWidget(self.photometry_progress, 1, 0, 1, 1)
        self.photometry_go = QtWidgets.QPushButton(Form)
        self.photometry_go.setMinimumSize(QtCore.QSize(50, 50))
        self.photometry_go.setMaximumSize(QtCore.QSize(50, 50))
        self.photometry_go.setObjectName("photometry_go")
        self.gridLayout_3.addWidget(self.photometry_go, 0, 1, 2, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Photometry"))
        self.groupBox.setTitle(_translate("Form", "Display"))
        self.groupBox_2.setTitle(_translate("Form", "Coodinates"))
        self.photometry_go.setText(_translate("Form", ":go"))


from gingawidgetFile import gingaWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
