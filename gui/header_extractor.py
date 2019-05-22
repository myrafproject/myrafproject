# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'header_extractor.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(449, 397)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_24 = QtWidgets.QGroupBox(Form)
        self.groupBox_24.setMinimumSize(QtCore.QSize(431, 321))
        self.groupBox_24.setObjectName("groupBox_24")
        self.gridLayout_79 = QtWidgets.QGridLayout(self.groupBox_24)
        self.gridLayout_79.setObjectName("gridLayout_79")
        self.hex_header_list = QtWidgets.QListWidget(self.groupBox_24)
        self.hex_header_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.hex_header_list.setObjectName("hex_header_list")
        self.gridLayout_79.addWidget(self.hex_header_list, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_24, 0, 0, 1, 1)
        self.gridLayout_81 = QtWidgets.QGridLayout()
        self.gridLayout_81.setObjectName("gridLayout_81")
        self.hex_annotation = QtWidgets.QLabel(Form)
        self.hex_annotation.setText("")
        self.hex_annotation.setObjectName("hex_annotation")
        self.gridLayout_81.addWidget(self.hex_annotation, 0, 0, 1, 1)
        self.hex_go = QtWidgets.QPushButton(Form)
        self.hex_go.setMinimumSize(QtCore.QSize(50, 50))
        self.hex_go.setMaximumSize(QtCore.QSize(50, 50))
        self.hex_go.setObjectName("hex_go")
        self.gridLayout_81.addWidget(self.hex_go, 0, 1, 2, 1)
        self.hex_progress = QtWidgets.QProgressBar(Form)
        self.hex_progress.setProperty("value", 24)
        self.hex_progress.setObjectName("hex_progress")
        self.gridLayout_81.addWidget(self.hex_progress, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_81, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Header Extractor"))
        self.groupBox_24.setTitle(_translate("Form", "Header"))
        self.hex_go.setText(_translate("Form", ":go"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
