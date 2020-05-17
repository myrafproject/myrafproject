# -*- coding: utf-8 -*-
"""
@author: msh, yk
"""

from PyQt5 import QtWidgets, QtCore

from myraflib import env

class Files:
    def __init__(self, frame, logger):
        self.frame = frame
        self.logger = logger

    def get_files(self, file_type=None):

        if file_type is not None:
            ftype = file_type
        else:
            ftype = "fits, fit, fts (*.fits *.fit *.fts)"

        files = QtWidgets.QFileDialog.getOpenFileNames(
            self.frame, "Images...", "",
            (ftype))[0]
        return files

    def get_file(self, file_type=None):

        if file_type is not None:
            ftype = file_type
        else:
            ftype = "fits, fit, fts (*.fits *.fit *.fts)"

        files = QtWidgets.QFileDialog.getOpenFileName(
            self.frame, "File...", "",
            (ftype))[0]
        return files

    def save_file(self, file_type=None, name=None):
        if file_type is None:
            tp = "fits, fit, fts (*.fits *.fit *.fts)"
        else:
            tp = file_type

        if name is None:
            nm = ""
        else:
            nm = file_type

        files = QtWidgets.QFileDialog.getSaveFileName(
            self.frame, "Output file", nm, (tp))[0]
        return files

    def save_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self.frame, 'Select directory')
        return directory


class Devices:
    def __init__(self, frame, logger):
        self.frame = frame
        self.logger = logger

        self.fop = env.File(logger)

    def list_of_selected(self, flist):
        ret = []
        for x in flist.selectedItems():
            ret.append(x.text())
        return ret

    def c_replace_list_con(self, fcomb, lst):
        self.rm_all(fcomb)
        self.c_add(fcomb, lst)

    def replace_list_con(self, flist, lst):
        self.rm_all(flist)
        self.add(flist, lst)

    def rm_all(self, flist):
        flist.clear()

    def add(self, flist, the_list):
        it = flist.count() - 1
        for x in the_list:
            it = it + 1
            item = QtWidgets.QListWidgetItem()
            flist.addItem(item)
            item = flist.item(it)
            item.setText(QtWidgets.QApplication.translate("Form", x, None))

    def c_add(self, fcomb, the_list):
        for i in the_list:
            fcomb.addItem(str(i))

    def rm(self, flist):
        for x in flist.selectedItems():
            flist.takeItem(flist.row(x))

    def list_of_list(self, flist):
        ret = []
        for x in range(flist.count()):
            ret.append(flist.item(x).text())

        return ret

    def add_to_tree(self, images_to_add, container):
        try:
            for file in images_to_add:
                file_type = file[1]
                stats = file[2]
                file_name_layer = QtWidgets.QTreeWidgetItem(container, [self.fop.get_base_name(file[0])[1], ""])
                file_name_layer.setFirstColumnSpanned(True)

                fname = QtWidgets.QTreeWidgetItem(file_name_layer, ["Path", self.fop.get_base_name(file[0])[0]])
                dtype = QtWidgets.QTreeWidgetItem(file_name_layer, ["Data Type", file_type])
                dmin = QtWidgets.QTreeWidgetItem(file_name_layer, ["Min", str(stats["Min"])])
                dmean = QtWidgets.QTreeWidgetItem(file_name_layer, ["Mean", str(stats["Mean"])])
                dmax = QtWidgets.QTreeWidgetItem(file_name_layer, ["Max", str(stats["Max"])])
                dstdv = QtWidgets.QTreeWidgetItem(file_name_layer, ["Stdev", str(stats["Stdev"])])

                file_name_layer.setToolTip(0, file[0])
                fname.setToolTip(0, self.fop.get_base_name(file[0])[0])
                fname.setToolTip(1, self.fop.get_base_name(file[0])[0])

                fname.setFlags(QtCore.Qt.ItemIsEnabled)
                dtype.setFlags(QtCore.Qt.ItemIsEnabled)
                dmin.setFlags(QtCore.Qt.ItemIsEnabled)
                dmean.setFlags(QtCore.Qt.ItemIsEnabled)
                dmax.setFlags(QtCore.Qt.ItemIsEnabled)
                dstdv.setFlags(QtCore.Qt.ItemIsEnabled)
        except Exception as e:
            self.logger.error(e)

    def rm_from_tree(self, container):
        getSelected = container.selectedItems()
        if getSelected:
            for i in getSelected:
                ind = container.indexOfTopLevelItem(i)
                container.takeTopLevelItem(ind)

    def get_from_tree(self, container, selected=False):
        ret = []
        if selected:
            ret = []
            getSelected = container.selectedItems()
            for element in getSelected:
                ret.append(element.text(0))
        else:
            iterator = QtWidgets.QTreeWidgetItemIterator(container, QtWidgets.QTreeWidgetItemIterator.HasChildren)
            while iterator.value():
                ret.append(iterator.value().text(0))
                iterator += 1

        return ret

    def ask(self, question):
        answ = QtWidgets.QMessageBox.question(self.frame, "MYRaf", question,
                                              QtWidgets.QMessageBox.Yes |
                                              QtWidgets.QMessageBox.No,
                                              QtWidgets.QMessageBox.No)

        return answ == QtWidgets.QMessageBox.Yes

    def ask_calcel(self, question):
        answ = QtWidgets.QMessageBox.question(self.frame, "MYRaf", question,
                                              QtWidgets.QMessageBox.Yes |
                                              QtWidgets.QMessageBox.No |
                                              QtWidgets.QMessageBox.Cancel,
                                              QtWidgets.QMessageBox.Cancel)
        if answ == QtWidgets.QMessageBox.Yes:
            return "yes"
        elif answ == QtWidgets.QMessageBox.No:
            return "no"

        return "cancel"
