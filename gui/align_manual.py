# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'align_manual.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(547, 524)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.manualAlign_display = gingaWidget(self.groupBox_2)
        self.manualAlign_display.setMinimumSize(QtCore.QSize(519, 412))
        self.manualAlign_display.setObjectName("manualAlign_display")
        self.gridLayout_2.addWidget(self.manualAlign_display, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.manualAlign_x = QtWidgets.QLineEdit(Form)
        self.manualAlign_x.setEnabled(False)
        self.manualAlign_x.setMaximumSize(QtCore.QSize(16777215, 20))
        self.manualAlign_x.setObjectName("manualAlign_x")
        self.gridLayout.addWidget(self.manualAlign_x, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.manualAlign_update_x = QtWidgets.QLineEdit(Form)
        self.manualAlign_update_x.setEnabled(False)
        self.manualAlign_update_x.setMaximumSize(QtCore.QSize(16777215, 20))
        self.manualAlign_update_x.setObjectName("manualAlign_update_x")
        self.gridLayout.addWidget(self.manualAlign_update_x, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        self.manualAlign_y = QtWidgets.QLineEdit(Form)
        self.manualAlign_y.setEnabled(False)
        self.manualAlign_y.setMaximumSize(QtCore.QSize(16777215, 20))
        self.manualAlign_y.setObjectName("manualAlign_y")
        self.gridLayout.addWidget(self.manualAlign_y, 0, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 6, 1, 1)
        self.manualAlign_update_y = QtWidgets.QLineEdit(Form)
        self.manualAlign_update_y.setEnabled(False)
        self.manualAlign_update_y.setMaximumSize(QtCore.QSize(16777215, 20))
        self.manualAlign_update_y.setObjectName("manualAlign_update_y")
        self.gridLayout.addWidget(self.manualAlign_update_y, 0, 7, 1, 1)
        self.manualAlign_go = QtWidgets.QPushButton(Form)
        self.manualAlign_go.setMinimumSize(QtCore.QSize(50, 50))
        self.manualAlign_go.setMaximumSize(QtCore.QSize(50, 50))
        self.manualAlign_go.setObjectName("manualAlign_go")
        self.gridLayout.addWidget(self.manualAlign_go, 0, 8, 2, 1)
        self.manualAlign_progress = QtWidgets.QProgressBar(Form)
        self.manualAlign_progress.setMaximumSize(QtCore.QSize(16777215, 21))
        self.manualAlign_progress.setProperty("value", 24)
        self.manualAlign_progress.setObjectName("manualAlign_progress")
        self.gridLayout.addWidget(self.manualAlign_progress, 1, 0, 1, 8)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Manual Align"))
        self.groupBox_2.setTitle(_translate("Form", "Image"))
        self.label_2.setText(_translate("Form", "X"))
        self.label.setText(_translate("Form", "->"))
        self.label_3.setText(_translate("Form", "Y"))
        self.label_4.setText(_translate("Form", "->"))
        self.manualAlign_go.setText(_translate("Form", ":go"))


from gingawidgetFile import gingaWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
