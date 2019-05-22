# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(583, 654)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(471, 111))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 182))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(50, 20))
        self.label.setMaximumSize(QtCore.QSize(50, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.display_file_name = QtWidgets.QLineEdit(self.groupBox)
        self.display_file_name.setEnabled(False)
        self.display_file_name.setObjectName("display_file_name")
        self.gridLayout_2.addWidget(self.display_file_name, 0, 1, 1, 1)
        self.display_export = QtWidgets.QPushButton(self.groupBox)
        self.display_export.setMinimumSize(QtCore.QSize(51, 23))
        self.display_export.setMaximumSize(QtCore.QSize(51, 23))
        self.display_export.setObjectName("display_export")
        self.gridLayout_2.addWidget(self.display_export, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(50, 20))
        self.label_2.setMaximumSize(QtCore.QSize(50, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(50, 20))
        self.label_3.setMaximumSize(QtCore.QSize(50, 20))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setMinimumSize(QtCore.QSize(50, 20))
        self.label_4.setMaximumSize(QtCore.QSize(50, 20))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.display_x = QtWidgets.QLineEdit(self.groupBox)
        self.display_x.setEnabled(False)
        self.display_x.setObjectName("display_x")
        self.gridLayout_2.addWidget(self.display_x, 1, 1, 1, 2)
        self.display_y = QtWidgets.QLineEdit(self.groupBox)
        self.display_y.setEnabled(False)
        self.display_y.setObjectName("display_y")
        self.gridLayout_2.addWidget(self.display_y, 2, 1, 1, 2)
        self.display_value = QtWidgets.QLineEdit(self.groupBox)
        self.display_value.setEnabled(False)
        self.display_value.setObjectName("display_value")
        self.gridLayout_2.addWidget(self.display_value, 3, 1, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.display_display = gingaWidget(self.groupBox_2)
        self.display_display.setMinimumSize(QtCore.QSize(519, 412))
        self.display_display.setObjectName("display_display")
        self.gridLayout.addWidget(self.display_display, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Display"))
        self.groupBox.setTitle(_translate("Form", "Information"))
        self.label.setText(_translate("Form", "File"))
        self.display_export.setText(_translate("Form", "Export"))
        self.label_2.setText(_translate("Form", "X"))
        self.label_3.setText(_translate("Form", "Y"))
        self.label_4.setText(_translate("Form", "Value"))
        self.groupBox_2.setTitle(_translate("Form", "Image"))


from gingawidgetFile import gingaWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
