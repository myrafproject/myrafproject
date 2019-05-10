# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\msh\OneDrive\Belgeler\the_myraf\gui\help_logger.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(639, 348)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.help_logger_list = QtWidgets.QListWidget(Form)
        self.help_logger_list.setMinimumSize(QtCore.QSize(621, 301))
        self.help_logger_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.help_logger_list.setObjectName("help_logger_list")
        self.gridLayout.addWidget(self.help_logger_list, 0, 0, 1, 4)
        self.logger_annotation = QtWidgets.QLabel(Form)
        self.logger_annotation.setText("")
        self.logger_annotation.setObjectName("logger_annotation")
        self.gridLayout.addWidget(self.logger_annotation, 1, 0, 1, 1)
        self.help_logger_reload = QtWidgets.QPushButton(Form)
        self.help_logger_reload.setMinimumSize(QtCore.QSize(72, 0))
        self.help_logger_reload.setMaximumSize(QtCore.QSize(72, 16777215))
        self.help_logger_reload.setObjectName("help_logger_reload")
        self.gridLayout.addWidget(self.help_logger_reload, 1, 1, 1, 1)
        self.help_logger_clear = QtWidgets.QPushButton(Form)
        self.help_logger_clear.setMinimumSize(QtCore.QSize(72, 0))
        self.help_logger_clear.setMaximumSize(QtCore.QSize(72, 16777215))
        self.help_logger_clear.setObjectName("help_logger_clear")
        self.gridLayout.addWidget(self.help_logger_clear, 1, 2, 1, 1)
        self.help_logger_save = QtWidgets.QPushButton(Form)
        self.help_logger_save.setMinimumSize(QtCore.QSize(72, 0))
        self.help_logger_save.setMaximumSize(QtCore.QSize(72, 16777215))
        self.help_logger_save.setObjectName("help_logger_save")
        self.gridLayout.addWidget(self.help_logger_save, 1, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Log Viewer"))
        self.help_logger_reload.setText(_translate("Form", "Reload"))
        self.help_logger_clear.setText(_translate("Form", "Clear"))
        self.help_logger_save.setText(_translate("Form", "Save"))

