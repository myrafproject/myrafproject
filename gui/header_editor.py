# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'header_editor.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(588, 580)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_8 = QtWidgets.QGroupBox(Form)
        self.groupBox_8.setMinimumSize(QtCore.QSize(571, 361))
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_29 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.header_hlist = QtWidgets.QListWidget(self.groupBox_8)
        self.header_hlist.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.header_hlist.setObjectName("header_hlist")
        self.gridLayout_29.addWidget(self.header_hlist, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_8, 0, 0, 1, 1)
        self.groupBox_9 = QtWidgets.QGroupBox(Form)
        self.groupBox_9.setMaximumSize(QtCore.QSize(16777215, 143))
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_30 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.label_15 = QtWidgets.QLabel(self.groupBox_9)
        self.label_15.setObjectName("label_15")
        self.gridLayout_30.addWidget(self.label_15, 0, 0, 1, 1)
        self.header_field = QtWidgets.QLineEdit(self.groupBox_9)
        self.header_field.setEnabled(True)
        self.header_field.setMaxLength(8)
        self.header_field.setObjectName("header_field")
        self.gridLayout_30.addWidget(self.header_field, 0, 1, 1, 1)
        self.header_useExisting = QtWidgets.QCheckBox(self.groupBox_9)
        self.header_useExisting.setObjectName("header_useExisting")
        self.gridLayout_30.addWidget(self.header_useExisting, 0, 2, 1, 2)
        self.label_16 = QtWidgets.QLabel(self.groupBox_9)
        self.label_16.setObjectName("label_16")
        self.gridLayout_30.addWidget(self.label_16, 1, 0, 1, 1)
        self.header_value = QtWidgets.QLineEdit(self.groupBox_9)
        self.header_value.setObjectName("header_value")
        self.gridLayout_30.addWidget(self.header_value, 1, 1, 1, 1)
        self.header_listOfExisting = QtWidgets.QComboBox(self.groupBox_9)
        self.header_listOfExisting.setEnabled(False)
        self.header_listOfExisting.setObjectName("header_listOfExisting")
        self.gridLayout_30.addWidget(self.header_listOfExisting, 1, 2, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(293, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_30.addItem(spacerItem, 2, 0, 1, 2)
        self.header_delete = QtWidgets.QPushButton(self.groupBox_9)
        self.header_delete.setMinimumSize(QtCore.QSize(100, 25))
        self.header_delete.setMaximumSize(QtCore.QSize(100, 25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../.designer/.designer/.designer/backup/img/rem.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.header_delete.setIcon(icon)
        self.header_delete.setObjectName("header_delete")
        self.gridLayout_30.addWidget(self.header_delete, 2, 2, 1, 1)
        self.header_insert_update = QtWidgets.QPushButton(self.groupBox_9)
        self.header_insert_update.setMinimumSize(QtCore.QSize(130, 25))
        self.header_insert_update.setMaximumSize(QtCore.QSize(130, 25))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../../../.designer/.designer/.designer/backup/img/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.header_insert_update.setIcon(icon1)
        self.header_insert_update.setObjectName("header_insert_update")
        self.gridLayout_30.addWidget(self.header_insert_update, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_9, 1, 0, 1, 1)
        self.gridLayout_27 = QtWidgets.QGridLayout()
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.header_progress = QtWidgets.QProgressBar(Form)
        self.header_progress.setProperty("value", 24)
        self.header_progress.setObjectName("header_progress")
        self.gridLayout_27.addWidget(self.header_progress, 1, 0, 1, 1)
        self.header_annotation = QtWidgets.QLabel(Form)
        self.header_annotation.setText("")
        self.header_annotation.setObjectName("header_annotation")
        self.gridLayout_27.addWidget(self.header_annotation, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_27, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Header Editor"))
        self.groupBox_8.setTitle(_translate("Form", "Header"))
        self.groupBox_9.setTitle(_translate("Form", "Operations:"))
        self.label_15.setText(_translate("Form", "Field:"))
        self.header_useExisting.setText(_translate("Form", "Use value from an existing field"))
        self.label_16.setText(_translate("Form", "Value:"))
        self.header_delete.setText(_translate("Form", "Delete"))
        self.header_insert_update.setText(_translate("Form", "Insert/Update"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
