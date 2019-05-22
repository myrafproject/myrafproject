# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myraf_progress.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(481, 64)
        Form.setMinimumSize(QtCore.QSize(481, 0))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(460, 23, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.progress_annotation = QtWidgets.QLabel(Form)
        self.progress_annotation.setObjectName("progress_annotation")
        self.gridLayout.addWidget(self.progress_annotation, 1, 0, 1, 1)
        self.progress_progressBar = QtWidgets.QProgressBar(Form)
        self.progress_progressBar.setProperty("value", 24)
        self.progress_progressBar.setObjectName("progress_progressBar")
        self.gridLayout.addWidget(self.progress_progressBar, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "MYRaf Progress"))
        self.progress_annotation.setText(_translate("Form", "TextLabel"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
