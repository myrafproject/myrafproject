# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_astrometrynet.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(334, 200)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.setting_astrometry_online = QtWidgets.QGroupBox(Form)
        self.setting_astrometry_online.setMaximumSize(QtCore.QSize(16777215, 142))
        self.setting_astrometry_online.setCheckable(True)
        self.setting_astrometry_online.setObjectName("setting_astrometry_online")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.setting_astrometry_online)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.label_73 = QtWidgets.QLabel(self.setting_astrometry_online)
        self.label_73.setObjectName("label_73")
        self.gridLayout_21.addWidget(self.label_73, 1, 0, 1, 1)
        self.setting_astrometry_online_server = QtWidgets.QLineEdit(self.setting_astrometry_online)
        self.setting_astrometry_online_server.setObjectName("setting_astrometry_online_server")
        self.gridLayout_21.addWidget(self.setting_astrometry_online_server, 0, 1, 1, 1)
        self.label_72 = QtWidgets.QLabel(self.setting_astrometry_online)
        self.label_72.setObjectName("label_72")
        self.gridLayout_21.addWidget(self.label_72, 0, 0, 1, 1)
        self.setting_astrometry_online_apikey = QtWidgets.QLineEdit(self.setting_astrometry_online)
        self.setting_astrometry_online_apikey.setObjectName("setting_astrometry_online_apikey")
        self.gridLayout_21.addWidget(self.setting_astrometry_online_apikey, 1, 1, 1, 1)
        self.setting_astrometry_online_compress = QtWidgets.QCheckBox(self.setting_astrometry_online)
        self.setting_astrometry_online_compress.setObjectName("setting_astrometry_online_compress")
        self.gridLayout_21.addWidget(self.setting_astrometry_online_compress, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.setting_astrometry_online, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 9, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(170, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.setting_astrometry_save = QtWidgets.QPushButton(Form)
        self.setting_astrometry_save.setMinimumSize(QtCore.QSize(72, 0))
        self.setting_astrometry_save.setMaximumSize(QtCore.QSize(72, 16777215))
        self.setting_astrometry_save.setObjectName("setting_astrometry_save")
        self.gridLayout.addWidget(self.setting_astrometry_save, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Astrometry.net Settings"))
        self.setting_astrometry_online.setTitle(_translate("Form", "&Go Online"))
        self.label_73.setText(_translate("Form", "Api Key"))
        self.setting_astrometry_online_server.setText(_translate("Form", "http://nova.astrometry.net/api/"))
        self.label_72.setText(_translate("Form", "Server"))
        self.setting_astrometry_online_compress.setText(_translate("Form", "Compress before upload"))
        self.setting_astrometry_save.setText(_translate("Form", "Save"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
