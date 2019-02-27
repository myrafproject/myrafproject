# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:57:43 2018

@author: mshem
"""

from math import ceil as mceil
try:
    from PyQt5 import QtWidgets
except Exception as e:
    print("{}. PyQt5 is not installed?".format(e))
    exit(0)

def save_directory(self):
    dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
    return(dir)

def save_file(self):
    filename = QtWidgets.QFileDialog.getSaveFileName(self,
            "Output file", "", ("FITS file (*.fit);;"))[0]
    
    return(filename)
    
def save_file_other(self):
    filename = QtWidgets.QFileDialog.getSaveFileName(self,
            "Output file", "", ("All files (*.*);;"))[0]
    
    return(filename)

def get_graph_file_path(self):
    filename = QtWidgets.QFileDialog.getOpenFileName(
            self ,"Graph file","",("MY file (*.my);;"))[0]
    return(filename)
    
def get_file_path(self):
    filename = QtWidgets.QFileDialog.getOpenFileName(
            self ,"Graph file","",("All files (*);;"))[0]
    return(filename)

def add_files(self, flist):
    filename = QtWidgets.QFileDialog.getOpenFileNames(
            self ,"Images...","",("fits, fit or fts (*.fits *.fit *.fts)"))[0]
    it = flist.count() - 1
    for x in filename:
        it = it+1
        item = QtWidgets.QListWidgetItem()
        flist.addItem(item)
        item = flist.item(it)
        item.setText(QtWidgets.QApplication.translate("Form", x, None))

def c_add(self, fcomb, the_list):
    for i in the_list:
        fcomb.addItem(i)

def c_replace_list_con(self, fcomb, lst):
    rm_all(self, fcomb)
    c_add(self, fcomb, lst)

def add(self, flist, the_list):
    it = flist.count() - 1
    for x in the_list:
        it = it+1
        item = QtWidgets.QListWidgetItem()
        flist.addItem(item)
        item = flist.item(it)
        item.setText(QtWidgets.QApplication.translate("Form", x, None))

def add_line_by_line(self, flist, file_name):
    the_f = open(file_name, "r")
    it = flist.count() - 1
    line_numbre = 0
    for x in the_f:
        line_numbre += 1
        ln = x.replace("\n", "")
        it = it+1
        item = QtWidgets.QListWidgetItem()
        flist.addItem(item)
        item = flist.item(it)
        item.setText(QtWidgets.QApplication.translate(
                "Form", "({:06d})  {}".format(line_numbre, ln), None))

def replace_list_con(self, flist, lst):
    rm_all(self, flist)
    add(self, flist, lst)

def question(self, question):
    answ = QtWidgets.QMessageBox.question(self, "MYRaf", question,
                                          QtWidgets.QMessageBox.Yes,
                                          QtWidgets.QMessageBox.No)
    return(answ)

def rm(self, flist):
    for x in flist.selectedItems():
        flist.takeItem(flist.row(x))

def save_log_file(self):
    ofile = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save Log File', 'log.myl', 'myl (*.myl)')
    return(ofile[0])

def rm_all(self, flist):
    flist.clear()
        
def list_lenght(self, flist):
    return(flist.count())
    
def is_list_empty(self, flist):
    return(list_lenght(self, flist) == 0)
    
def list_of_list(self, flist):
    ret = []
    for x in range(flist.count()):
        ret.append(flist.item(x).text())
        
    return(ret)

def list_of_selected(self, flist):
    ret = []
    for x in flist.selectedItems():
        ret.append(x.text())
    return(ret)
    
def proc(self, proc_dev, perc):
    proc_dev.setProperty("value", mceil(100*perc))
    
def is_checked_t(self, dev):
    if dev.isChecked():
        return("YES")
    else:
        return("NO")
        