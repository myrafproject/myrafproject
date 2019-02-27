# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:54:39 2018

@author: mshem
"""
#Importing Circle to draw circles to images
try:
    from matplotlib.patches import Circle
except Exception as e:
    print("{}. Mtplotlib is not installed?".format(e))
    exit(0)

#Importing PyQt5
try:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
except Exception as e:
    print("{}. PyQt5 is not installed?".format(e))
    exit(0)
    


#Importing argv to get arguments from terminal
from sys import argv
from sys import exit as sexit

#Importing myraf's GUI
try:
    import gui as g
except Exception as e:
    print("{}. Cannot find gui.py".format(e))
    exit(0)

try:
    from fPlot import FitsPlot
except Exception as e:
    print("{}. Cannot find fPlot.py".format(e))
    exit(0)

try:
    from myraf import Ui_Form
except Exception as e:
    print("{}. Cannot find myraf.py".format(e))
    exit(0)

#Importing myraf's needed modules
try:
    from myraflib import myEnv
    
    from myraflib import myCos
except Exception as e:
    print("{}. Cannot find myraflib".format(e))

from myraflib import myAst

class MyForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, verb=True):
        super(MyForm, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.verb = verb
        
        self.etc = myEnv.etc(verb=self.verb)
        self.cnv = myEnv.converter(verb=self.verb)
        self.fop = myEnv.file_op(verb=self.verb)
        self.fit = myAst.fits(verb=self.verb)
        self.sex = myAst.sextractor(verb=self.verb)
        self.pht = myAst.phot(verb=self.verb)
        self.clc = myAst.calc(verb=self.verb)
        self.cat = myAst.cat(verb=self.verb)
        self.cal = myAst.calibration(verb=self.verb)
        self.tim = myAst.time(verb=self.verb)
        
        self.etc.log("***MyRAF STARTED***")
        
        for device in ["PHOT", "ALIGN", "ATRACK", "COSMIC"]:
            self.empty_display(device)
        
        self.first_thing_first()
        
        lfs = self.fop.get_size(self.etc.log_file) / 1048576
        mlfs = self.fop.get_size(self.etc.mini_log_file) / 1048576
        
        if lfs > 5 or mlfs > 5:
            self.etc.log("Log file is too big. Ask for deletation.")
            answ = g.question(self, "Log files are getting Huge. It'll effect the performance. Would you like to clear them?")
            if answ == QtWidgets.QMessageBox.Yes:
                self.clear_log()
                
        self.etc.log("Resetting Gui for Log tab")
        #set Log tab
        self.ui.label_19.setProperty("text",
                                     "Logs are stored in: {} & {}".format(
                                             self.etc.log_file,
                                             self.etc.mini_log_file))
        
        self.etc.log("Resetting Gui for Calibration tab")
        #set calibration tab
        self.ui.progressBar.setProperty("value", 0)
        self.ui.label_3.setProperty("text", "")
        self.ui.label_4.setProperty("text", "")
        self.ui.label_5.setProperty("text", "")
        self.ui.label_6.setProperty("text", "")
        self.ui.label.setProperty("text", "")
        self.calibration_annotation()
        
        self.etc.log("Creating triggers for Calibration tab")
        #add triggers for Calibration
        self.ui.pushButton_6.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_6),
                self.calibration_annotation()))
        self.ui.pushButton_5.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_6),
                self.calibration_annotation()))
        self.ui.listWidget_6.installEventFilter(self)
        
        self.ui.pushButton_8.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_7),
                self.calibration_annotation()))
        self.ui.pushButton_7.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_7),
                self.calibration_annotation()))
        self.ui.pushButton_37.clicked.connect(lambda: (self.zero_combine()))
        self.ui.listWidget_7.installEventFilter(self)
        
        self.ui.pushButton_10.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_8),
                self.calibration_annotation()))
        self.ui.pushButton_9.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_8),
                self.calibration_annotation()))
        self.ui.pushButton_40.clicked.connect(lambda: (self.dark_combine()))
        self.ui.listWidget_8.installEventFilter(self)
        
        self.ui.pushButton_12.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_9),
                self.calibration_annotation()))
        self.ui.pushButton_11.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_9),
                self.calibration_annotation()))
        self.ui.pushButton_41.clicked.connect(lambda: (self.flat_combine()))
        self.ui.listWidget_9.installEventFilter(self)
        
        self.ui.pushButton.clicked.connect(lambda: (self.do_calibration()))
        
        self.etc.log("Resetting Gui for Align tab")
        #set align tab
        self.ui.progressBar_2.setProperty("value", 0)
        self.ui.label_2.setProperty("text", "")
        self.align_annotation()
        
        self.etc.log("Creating triggers for Align tab")
        #add triggers for align
        self.ui.pushButton_3.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget),
                self.align_annotation()))
        self.ui.pushButton_4.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget),
                self.align_annotation(),
                self.empty_display("align")))
        
        self.ui.pushButton_2.clicked.connect(lambda: (self.do_align()))
        self.ui.listWidget.clicked.connect(lambda: (self.display_align()))
        self.ui.listWidget.installEventFilter(self)
        
        self.etc.log("Resetting Gui for Photometry tab")
        #set photometry tab
        self.ui.progressBar_4.setProperty("value", 0)
        self.ui.label_8.setProperty("text", "")
        self.ui.label_54.setProperty("text", "")
        self.phot_annotation()
        
        self.etc.log("Creating triggers for Photometry tab")
        #add triggers for photometry
        self.ui.pushButton_15.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_2),
                self.phot_annotation(), self.phot_hex()))
        self.ui.pushButton_14.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_2),
                self.phot_annotation(), self.phot_hex(),
                self.empty_display("PHOT")))
        self.ui.pushButton_36.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_14),
                self.phot_annotation()))
        
        self.ui.pushButton_35.clicked.connect(lambda: (
                self.display_coors_phot()))
        
        self.ui.disp_photometry.canvas.fig.canvas.mpl_connect(
                'button_press_event',self.mouseClick)
        
        self.ui.pushButton_51.clicked.connect(lambda: (self.phot_hex()))
        self.ui.pushButton_49.clicked.connect(lambda: (self.queue_header()))
        self.ui.pushButton_50.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_20)))
        
        self.ui.pushButton_34.clicked.connect(lambda: (self.run_sex()))
        self.ui.pushButton_16.clicked.connect(lambda: (self.do_phot()))
        self.ui.listWidget_2.clicked.connect(lambda: (self.display_phot()))
        self.ui.listWidget_14.installEventFilter(self)
        self.ui.listWidget_2.installEventFilter(self)
        self.ui.listWidget_20.installEventFilter(self)
        
        self.etc.log("Resetting Gui for A-Track tab")
        #set a-track tab
        self.ui.progressBar_7.setProperty("value", 0)
        self.ui.label_27.setProperty("text", "")
        self.atrack_annotation()
        
        self.etc.log("Creating triggers for A-Track tab")
        #add triggers for atrack
        self.ui.pushButton_33.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_13),
                self.atrack_annotation()))
        self.ui.pushButton_32.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_13),
                self.atrack_annotation(),
                self.empty_display("ATRAK")))
        
        self.ui.pushButton_43.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_15)))
        
        self.ui.listWidget_13.clicked.connect(lambda: (self.display_atrack()))
        self.ui.pushButton_42.clicked.connect(lambda: (self.a_track()))
        self.ui.listWidget_13.installEventFilter(self)
        self.ui.listWidget_15.installEventFilter(self)
        
        self.etc.log("Resetting Gui for Hedit tab")
        #set header editor tab
        self.ui.progressBar_3.setProperty("value", 0)
        self.ui.label_10.setProperty("text", "")
        self.heditor_annotation()
        
        self.etc.log("Creating triggers for Hedit tab")
        #add triggers for header editor
        self.ui.pushButton_20.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_3),
                self.heditor_annotation()))
        self.ui.pushButton_19.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_3),
                self.heditor_annotation()))
        
        self.ui.checkBox_5.clicked.connect(lambda: (
                self.use_existing_header()))
                
        
        self.ui.pushButton_39.clicked.connect(lambda: (
                self.do_hedit(update_add=True)))
        self.ui.pushButton_38.clicked.connect(lambda: (
                self.do_hedit(update_add=False)))
                
        self.ui.listWidget_3.clicked.connect(lambda: (self.header_list()))
        self.ui.listWidget_4.clicked.connect(lambda: (self.get_the_header()))
        self.ui.listWidget_3.installEventFilter(self)
        self.ui.listWidget_4.installEventFilter(self)
        
        self.etc.log("Resetting Gui for CosmicC tab")
        #set Cosmic Cleaner tab
        self.ui.progressBar_5.setProperty("value", 0)
        self.ui.label_11.setProperty("text", "")
        self.cosmicC_annotation()
        
        self.etc.log("Creating triggers for CosmicC tab")
        #add triggers for Cosmic Cleaner
        self.ui.pushButton_22.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_5),
                self.cosmicC_annotation()))
        self.ui.pushButton_21.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_5),
                self.cosmicC_annotation(),
                self.empty_display("COSMIC")))
        
        self.ui.pushButton_23.clicked.connect(lambda: (self.do_cosmicC()))
        self.ui.listWidget_5.clicked.connect(lambda: (self.display_cosmicC()))
        self.ui.listWidget_5.installEventFilter(self)
        
        
        self.etc.log("Resetting Gui for Calculator tab")
        #set Caloculator tab
        self.ui.progressBar_9.setProperty("value", 0)
        self.ui.label_49.setProperty("text", "")
        self.calculator_annotation()
        
        self.etc.log("Creating triggers for Calculator")
        #add triggers for Calculator
        self.ui.groupBox_33.clicked.connect(lambda: (
                self.calculator_annotation()))
        self.ui.groupBox_34.clicked.connect(lambda: (
                self.calculator_annotation()))
        self.ui.groupBox_35.clicked.connect(lambda: (
                self.calculator_annotation()))
        self.ui.groupBox_14.clicked.connect(lambda: (
                self.calculator_annotation()))
        
        self.ui.pushButton_47.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_16),
                self.calculator_annotation()))
        self.ui.pushButton_46.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_16),
                self.calculator_annotation()))
        
        self.ui.pushButton_48.clicked.connect(lambda: (self.do_calculator()))
        self.ui.listWidget_16.clicked.connect(lambda: (
                self.header_list_calculator()))
        self.ui.listWidget_16.installEventFilter(self)
        
        self.etc.log("Resetting Gui for WCS tab")
        #set WCS Editor tab
        self.ui.progressBar_6.setProperty("value", 0)
        self.ui.label_17.setProperty("text", "")
        self.ui.label_14.setProperty("text", "")
        self.wcs_annotation()
        
        self.etc.log("Creating triggers for WCS tab")
        #add triggers for WCS Editor
        self.ui.pushButton_24.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_11),
                self.wcs_annotation()))
        self.ui.pushButton_25.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_11),
                self.wcs_annotation()))
        
        self.ui.pushButton_26.clicked.connect(lambda: (self.do_wcs()))
        self.ui.listWidget_11.installEventFilter(self)
        
        self.etc.log("Creating triggers for Sttings tab")
        #add triggers for Settings
        self.ui.pushButton_17.clicked.connect(lambda: (self.save_settings()))
        self.ui.groupBox_5.clicked.connect(lambda: (
                self.astrometrynet_check()))
                
        self.etc.log("Creating triggers for Observatory Editor tab")
        #add triggers for Observatory Editor
        self.ui.pushButton_30.clicked.connect(lambda: (self.add_obs()))
        self.ui.pushButton_29.clicked.connect(lambda: (self.rm_obs()))
        self.ui.listWidget_12.clicked.connect(lambda: (
                        self.get_observat_prop()))
        self.ui.listWidget_12.installEventFilter(self)
        self.load_observat()
        
        self.etc.log("Creating triggers for Log tab.")
        #add triggers for Logs
        self.ui.pushButton_28.clicked.connect(lambda: (self.reload_log()))
        self.ui.pushButton_18.clicked.connect(lambda: (self.save_log()))
        self.ui.pushButton_27.clicked.connect(lambda: (self.clear_log()))
        self.reload_log()
        
        self.etc.log("Resetting Gui for Graph tab")
        #set Graph Editor
        self.ui.label_31.setProperty("text", "")
        
        self.etc.log("Creating triggers for Graph tab")
        #set triggers Graph Editor tab
        self.ui.pushButton_44.clicked.connect(lambda: (
                self.get_graph_file_path()))
        self.ui.pushButton_45.clicked.connect(lambda: (
                self.plot_graph()))
        
        self.ui.disp_align.canvas.fig.canvas.mpl_connect(
                'button_press_event',self.mouseClick)
        
        
        self.etc.log("Resetting Gui for HExtractor tab")
        #set HExtractor Editor
        self.ui.label_28.setProperty("text", "")
        self.ui.progressBar_10.setProperty("value", 0)
        self.hextractor_annotation()
        
        self.ui.pushButton_57.clicked.connect(lambda: (
                g.add_files(self, self.ui.listWidget_18),
                self.hextractor_annotation()))
        self.ui.pushButton_56.clicked.connect(lambda: (
                g.rm(self, self.ui.listWidget_18),
                self.hextractor_annotation()))
        
        self.ui.listWidget_18.clicked.connect(lambda: (self.hextractor_list()))
        self.ui.pushButton_58.clicked.connect(lambda: (self.hextractor()))
        self.ui.listWidget_18.installEventFilter(self)
        
    def eventFilter(self, source, event):
        
        if(event.type() == 7 and source is self.ui.listWidget_18):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_18)
                self.hextractor_annotation()
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_12):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_12)
                self.load_observat()
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_11):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_11)
                self.wcs_annotation()
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_16):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_16)
                self.calculator_annotation()
            return True
            
        if(event.type() == 7 and source is self.ui.listWidget_4):
            if event.key() == 16777223:
                self.do_hedit(update_add=False)
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_15):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_15)
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_13):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_13)
                self.atrack_annotation()
                self.empty_display("ATRACK")
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_5):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_5)
                self.cosmicC_annotation()
                self.empty_display("COSMIC")
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_3):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_3)
                self.heditor_annotation()
            return True
        
        if(event.type() == 7 and source is self.ui.listWidget_6):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_6)
                self.calibration_annotation()
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_7):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_7)
                self.calibration_annotation()
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_8):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_8)
                self.calibration_annotation()
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_9):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_9)
                self.calibration_annotation()
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget)
                self.align_annotation()
                self.empty_display("ALIGN")
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_2):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_2)
                self.phot_annotation()
                self.empty_display("PHOT")
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_20):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_20)
            return True
                
        if(event.type() == 7 and source is self.ui.listWidget_14):
            if event.key() == 16777223:
                g.rm(self, self.ui.listWidget_14)
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_13):
            menu = QtWidgets.QMenu()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction('Header Editor', lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget_13),
                                    self.phot_annotation()))
            subMenu.addAction('Header Calculator', lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget_13),
                                    self.phot_annotation()))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_2):
            menu = QtWidgets.QMenu()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction('Header Calculator', lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget_2),
                                    self.phot_annotation()))
            subMenu.addAction('Cosmic Cleaner', lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget_2),
                                    self.phot_annotation()))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_5):
            menu = QtWidgets.QMenu()
            menu.addAction('Check for possible over writes', lambda: (
                    self.check_over_write(self.ui.listWidget_5)))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_11):
            menu = QtWidgets.QMenu()
            menu.addAction('Check for possible over writes', lambda: (
                    self.check_over_write(self.ui.listWidget_11)))
            menu.exec_(event.globalPos())
            return True
                
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget):
            menu = QtWidgets.QMenu()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction('Header Editor', lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget),
                                    self.align_annotation()))
            subMenu.addAction('Header Calculator', lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget),
                                    self.align_annotation()))
            menu.addSeparator()
            menu.addAction('Check for possible over writes', lambda: (
                    self.check_over_write(self.ui.listWidget_6)))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_6):
            menu = QtWidgets.QMenu()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction('Header Editor', lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget_6),
                                    self.calibration_annotation()))
            subMenu.addAction('Header Calculator', lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget_6),
                                    self.calibration_annotation()))
            menu.addSeparator()
            menu.addAction('Check for possible over writes', lambda: (
                    self.check_over_write(self.ui.listWidget_6)))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_7):
            menu = QtWidgets.QMenu()
            menu.addAction('Get Stats', lambda: (
                    self.fits_stats(self.ui.listWidget_7)))
            menu.addSeparator()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction('Header Editor', lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget_7),
                                    self.calibration_annotation()))
            subMenu.addAction('Header Calculator', lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget_7),
                                    self.calibration_annotation()))
            menu.addSeparator()
            menu.addAction("Check for possible duplicates", lambda: (
                    self.check_over_write(self.ui.listWidget_7, ow=False)))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_8):
            menu = QtWidgets.QMenu()
            menu.addAction('Get Stats', lambda: (
                    self.fits_stats(self.ui.listWidget_8)))
            menu.addSeparator()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction("Header Editor", lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget_8),
                                    self.calibration_annotation()))
            subMenu.addAction("Header Calculator", lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget_8),
                                    self.calibration_annotation()))
            menu.addSeparator()
            menu.addAction("Check for possible duplicates", lambda: (
                    self.check_over_write(self.ui.listWidget_8, ow=False)))
            menu.exec_(event.globalPos())
            
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_9):
            menu = QtWidgets.QMenu()
            menu.addAction('Get Stats', lambda: (
                    self.fits_stats(self.ui.listWidget_9)))
            menu.addSeparator()
            subMenu = menu.addMenu("Add files from")
            subMenu.addAction('Header Editor', lambda: (
                    self.bring_from(self.ui.listWidget_3,
                                    self.ui.listWidget_9),
                                    self.calibration_annotation()))
            subMenu.addAction('Header Calculator', lambda: (
                    self.bring_from(self.ui.listWidget_16,
                                    self.ui.listWidget_9),
                                    self.calibration_annotation()))
            menu.addSeparator()
            menu.addAction('Check for possible duplicates', lambda: (
                    self.check_over_write(self.ui.listWidget_9, ow=False)))
            menu.exec_(event.globalPos())
            return True
        
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.ui.listWidget_14):
            menu = QtWidgets.QMenu()
            menu.addAction('Export', self.export_coordinates)
            menu.addAction('Import', self.import_coordinates)
            menu.exec_(event.globalPos())
            return True
        
        return super(MyForm, self).eventFilter(source, event)

#    def fwhm_clc(self, event):
#        may_the_file = self.ui.listWidget_2.currentItem()
#        if may_the_file is not None:
#            the_file = may_the_file.text()
#            if self.fit.is_fit(the_file):
#                data = self.fit.data(the_file, table=False)
#                objects = self.sex.find(data, only_best=False)
#                all_sources_x = self.cnv.list2npar(objects['x'])
#                all_sources_y = self.cnv.list2npar(objects['y'])
#                wanted = self.cnv.list2npar([float(event.globalX()),
#                                             float(event.globalY())])
#                close = self.clc.get_closest_index(all_sources_x, all_sources_y, wanted)
#                print(objects[close]['x'], objects[close]['y'])
#                print(wanted)
#            else:
#                self.etc.log("The file is not a fit")
#            
#        else:
#            #Log and display an error about not selected file
#            self.etc.log("Nothing was selected in list")
#            QtWidgets.QMessageBox.critical(
#                    self, ("MYRaf Error"), ("Please select a file"))
#        PyQt5.QtCore.QPoint(941, 410)
        
    def fwhm_clc(self, event):
        print(event.globalPos())

    def check_over_write(self, list_dev_s, ow=True):
        all_lines = g.list_of_list(self, list_dev_s)
        is_there = []
        rm_list = []
        if len(all_lines) > 0:
            for it, line in enumerate(all_lines):
                path, name = self.fop.get_base_name(line)
                if not name in is_there:
                    is_there.append(name)
                else:
                    rm_list.append(it)
                    
            if len(rm_list) > 0:
                if ow:
                    the_ow = "over write"
                else:
                    the_ow = "duplicate"
                    
                post_msg = "Do you want to remove the file"
                    
                if len(rm_list) == 1:
                    msg = "There is an {}. {}?".format(the_ow, post_msg)
                else:
                    msg = "There are {} {}s. {}s?".format(len(rm_list),
                                     the_ow, post_msg)
                    
                answ = g.question(self, msg)
                if answ == QtWidgets.QMessageBox.Yes:
                    for rm_line in reversed(sorted(rm_list)):
                        list_dev_s.takeItem(rm_line)
        else:
            self.etc.log("Nothing is in source list. No overwrite expected.")

    def bring_from(self, list_dev_s, list_dev_d):
        all_lines = g.list_of_list(self, list_dev_s)
        if len(all_lines) > 0:
            g.add(self, list_dev_d, all_lines)
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing found in source list")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Nothing found in source list"))

    def export_coordinates(self):
        if not g.is_list_empty(self, self.ui.listWidget_14):
            coordinates = g.list_of_list(self, self.ui.listWidget_14)
            dest = g.save_file_other(self)
            #Check if the path is available
            if dest:
                f2w = open(dest, "w")
                for coordinate in coordinates:
                    f2w.write("{}\n".format(coordinate))
                f2w.close()
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to Export")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some coordinates"))

        #Reload log file to log view
        self.reload_log()
        
    def import_coordinates(self):
        try:
            file_path = g.get_file_path(self)
            if self.fop.is_file(file_path):
                list_to_add = []
                f2r = open(file_path, "r")
                for ln in f2r:
                    line = ln.replace("\n", "")
                    if ", " in line:
                        list_to_add.append(line)
                        
                g.add(self, self.ui.listWidget_14, list_to_add)
        except Exception as e:
            self.rtc.log(e)
          
        #Reload log file to log view 
        self.reload_log()

    def queue_header(self):
        if len(g.list_of_selected(self, self.ui.listWidget_19)) > 0:
            already_there_headers = g.list_of_list(self, self.ui.listWidget_20)
            selected_headers = g.list_of_selected(self, self.ui.listWidget_19)
            headers_to_add = []
            for header in selected_headers:
                if not header in already_there_headers:
                    headers_to_add.append(header)
            g.add(self, self.ui.listWidget_20, headers_to_add)
        
    def hextractor(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_18):
            if len(g.list_of_selected(self, self.ui.listWidget_17)) > 0 :
                self.ui.label.setText("Hextraction started")
                dest = g.save_file_other(self)
                if dest:
                    files = g.list_of_list(self, self.ui.listWidget_18)
                    headers = g.list_of_selected(self, self.ui.listWidget_17)
                    the_ret = []
                    out_put_header = ["File Name"]
                    for header in headers:
                        key = header.split("=>")[0]
                        out_put_header.append(key)
                    for it, file in enumerate(files):
                        if self.fit.is_fit(file):
                            line = [file]
                            for header in headers:
                                key = header.split("=>")[0]
                                the_header = self.fit.header(file, key)
                                if the_header is not None:
                                    ext_header = str(the_header[1])
                                else:
                                    ext_header = "None"
                                
                                line.append(ext_header)
                            
                            the_ret.append(line)
                        g.proc(self,
                               self.ui.progressBar_10, (it + 1) / len(files))
                            
                    out_file = open(dest, "w")
                    out_file.write("#{}\n".format("\t".join(out_put_header)))
                    for ln in the_ret:
                        out_file.write("{}\n".format("\t".join(ln)))
                    out_file.close()
                    
                else:
                    self.etc.log("No path was given to save")
            else:
                self.etc.log("No enough input")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Please select header keys to extract"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to hextract")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
        
    
    #Get whole list of headers of a fits file
    def hextractor_list(self):
        #Get file's name
        img = self.ui.listWidget_18.currentItem().text()
        #Check if file does exist
        if self.fit.is_fit(img):
            try:
                #Get all headers of give file
                all_header = self.fit.header(img)
                #convert [key, value] to "key=>value" format in an array
                header_list = []
                for i in all_header:
                    header_list.append("{}=>{}".format(i[0], i[1]))
                
                #Replace whole list with header list
                g.replace_list_con(self, self.ui.listWidget_17, header_list)
            except Exception as e:
                #Log error if any occurs
                self.etc.log(e)
        else:
            #Log and display an error about not existing file
            self.etc.log("Bad fits or no such (Header List)file({})".format(
                    img))
            QtWidgets.QMessageBox.critical(
                self, ("MYRaf Error"), ("Bad fits or no such a file"))
    
        #Reload log file to log view
        self.reload_log()
    
    def hextractor_annotation(self):
        img = g.list_lenght(self, self.ui.listWidget_18)
        self.ui.label_28.setProperty(
                "text", "header(s) of {0} files will be extracted".format(img))
        
        #Reload log file to log view
        self.reload_log()

    
    #Plot a graph for given file
    def plot_graph(self):
        #Get file's path
        path_to_file = self.ui.label_31.text()
        #Check path
        if self.fop.is_file(path_to_file):
            #Load the file to an array
            the_file = self.fop.read_array(path_to_file)
            
            xs = None
            ys = None
            y2s = None
            #Check if file was loaded
            if the_file is not None:                
                
                #Try to get the wanted column for X axis
                try:
                    xaxis = int(self.ui.comboBox_13.currentText())
                    xs = the_file[:, xaxis]
                except Exception as e:
                    self.etc.log(e)
                    
                #Try to get the wanted column for Y axis
                try:
                    yaxis = int(self.ui.comboBox_14.currentText())
                    ys = the_file[:, yaxis]
                except Exception as e:
                    self.etc.log(e)
                    
                #Checl if second Y (Z) axis wanted
                if self.ui.groupBox_29.isChecked():
                    #Try to get the wanted column for Y2 (Z) axis
                    try:
                        y2axis = int(self.ui.comboBox_15.currentText())
                        y2s = the_file[:, y2axis]
                    except Exception as e:
                        self.etc.log(e)
            
            #Check if X and Y axises are valid
            if xs is not None or ys is not None:
                #Check if second Y (Z) axis wanted
                if self.ui.groupBox_29.isChecked():
                    #Check if secod Y (Z) axis is valid
                    if y2s is not None:
                        #Check if it's second Y or Z axis
                        if self.ui.checkBox_7.isChecked():
                            self.etc.log("Plotting 3D Graph")
                        else:
                            self.etc.log("Plotting 2D Graph with overplot")
                    else:
                        self.etc.log("Y2 (Z) of axis is not correct")
                        QtWidgets.QMessageBox.critical(
                                self, ("MYRaf Error"),
                                ("Y2 (Z) of axis is not correct"))
                else:
                    self.etc.log("Plotting 2D Graph")
                     
            else:
                self.etc.log("X or Y of axis is not correct")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("X or Y of axis is not correct"))
            
        else:
            self.etc.log("No such file({})".format(path_to_file))
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("No such file({})".format(path_to_file)))
        
    def fits_stats(self, list_widget):
        #Getting list of files selected
        selected = g.list_of_selected(self, list_widget)
        #Check if any file(s) was selected
        if len(selected) > 0:
            stt = ""
            #Loop for all selected files
            for file in selected:
                #Check if file exist
                if self.fit.is_fit(file):
                    #Get status for file
                    the_stats = self.fit.fits_stat(file)
                    fname = self.fop.get_base_name(file)[1]
                    #Append file name and status to a string
                    stt  = "{0}, Mean:{1:.2f}, Stdev:{2:.2f}\n{3}".format(
                            fname, the_stats['Mean'], the_stats['Stdev'], stt)
            
            if not stt == "":
                #Display results
                QtWidgets.QMessageBox.information(
                        self, ("MYRaf Information"),
                        ("Stats for files are as below:\n{}".format(stt)))
            else:
                #Log and display an error about 0 files selected
                self.etc.log("Could not get any stats")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Given file(s) could not be analyed"))
        else:
            #Log and display an error about 0 files selected
            self.etc.log("No file was selected to show stats")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("Please at least select one file to analyse"))
    
    #Add header values to calculator's dropdown menus
    def header_list_calculator(self):
        #Get file's name
        img = self.ui.listWidget_16.currentItem().text()
        #Check if file does exist
        if self.fit.is_fit(img):
            try:
                #Get all headers of give file
                all_header = self.fit.header(img)
                #convert [key, value] to "key=>value" format in an array
                header_list = []
                for i in all_header:
                    header_list.append("{}=>{}".format(i[0], i[1]))
                
                #Replace whole combo with header list
                g.c_replace_list_con(self, self.ui.comboBox_16, header_list)
                g.c_replace_list_con(self, self.ui.comboBox_18, header_list)
                g.c_replace_list_con(self, self.ui.comboBox_17, header_list)
                g.c_replace_list_con(self, self.ui.comboBox_19, header_list)
                g.c_replace_list_con(self, self.ui.comboBox_20, header_list)
            except Exception as e:
                #Log error if any occurs
                self.etc.log(e)
        else:
            #Log and display an error about not existing file
            self.etc.log("Bad fits or no such (Header List)file({})".format(
                    img))
            QtWidgets.QMessageBox.critical(
                self, ("MYRaf Error"), ("Bad fits or no such a file"))
    
        #Reload log file to log view
        self.reload_log()
    
    #Calculate wanted values adn add them to header
    def do_calculator(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_16):
            #Check what calculations wanted
            do_jd = self.ui.groupBox_33.isChecked()
            do_airmass = self.ui.groupBox_34.isChecked()
            do_imexam = self.ui.groupBox_35.isChecked()
            do_utc = self.ui.groupBox_14.isChecked()
            #Get pref for header keys
            pref = self.ui.lineEdit_9.text()
            #Check if JD, airmass or imexamine calculation wanted
            if do_jd or do_airmass or do_imexam or do_utc:
                #Get list of files
                files = g.list_of_list(self, self.ui.listWidget_16)
                #Loop in files
                for it, file in enumerate(files):
                    #Check if file is a fits file
                    if self.fit.is_fit(file):
                        #Check if JD calculation wanted
                        if do_jd:
                            self.etc.log("JD calculation wanted")
                            try:
                                #Get the "key=>value" for existing value
                                combo_time_jd = self.ui.\
                                comboBox_16.currentText()
                                #Find wanted key by spliting it by "=>"
                                field_time_jd = combo_time_jd.split(
                                        "=>")[1].strip()
                                the_jd = self.clc.jd(field_time_jd)
                                the_mjd = self.clc.mjd(field_time_jd)
                                #Check if JD is valid
                                if type(the_jd) == float:
                                    #Write JD value to files header
                                    self.fit.update_header(
                                            file, "{}JD".format(pref), the_jd)
                                    
                                #Check if MJD is valid
                                if type(the_mjd) == float:
                                    #Write MJD value to files header
                                    self.fit.update_header(
                                            file, "{}MJD".format(pref),
                                            the_mjd)
                            except Exception as e:
                                self.etc.log(e)
                                continue
                                
                        #Check if imexamine wanted
                        if do_imexam:
                            self.etc.log("Imexamine calculation wanted")
                            try:
                                #Do the imexamine to file
                                imex = self.clc.imexamine(file)
                            except Exception as e:
                                self.etc.log(e)
                                continue
                            
                            #Check if imexamine succeed and returnd some values
                            if imex is not None:
                                try:
                                    #Add Mean value to header
                                    if self.ui.checkBox_8.isChecked():
                                        self.fit.update_header(
                                                file, "{}mean".format(
                                                        pref), imex[0])
                                    #Add Median value to header
                                    if self.ui.checkBox_9.isChecked():
                                        self.fit.update_header(
                                                file, "{}medi".format(
                                                        pref), imex[1])
                                    #Add STDEV value to header
                                    if self.ui.checkBox_10.isChecked():
                                        self.fit.update_header(
                                                file, "{}stdv".format(
                                                        pref), imex[2])
                                    #Add MIN value to header
                                    if self.ui.checkBox_11.isChecked():
                                        self.fit.update_header(
                                                file, "{}min".format(
                                                        pref), imex[3])
                                    #Add MAX value to header
                                    if self.ui.checkBox_12.isChecked():
                                        self.fit.update_header(
                                                file, "{}max".format(
                                                        pref), imex[4])
                                except Exception as e:
                                    self.etc.log(e)
                                    continue
                        if do_utc:
                            self.etc.log("Time calculation wanted")
                            try:
                                time = self.ui.comboBox_20.currentText()
                                the_time = time.split("=>")[1]
                                time_offset = float(
                                        self.ui.doubleSpinBox_2.value())
                                ofset_type = self.ui.comboBox.currentText()
                                new_time = self.tim.time_offset(
                                        the_time, time_offset,
                                        diff_type=ofset_type.lower())
                                if new_time is not None:
                                    self.fit.update_header(
                                            file, "{}ntime".format(pref),
                                            str(new_time))
                            except:
                                self.etc.log("BAD time")
                                
                            

                        if do_airmass:
                            self.etc.log("Airmass calculation wanted")
                            the_time = None
                            the_ra = None
                            the_dec = None
                            longitude = None
                            latitude = None
                            altitude = None
                            timezone = None
                            try:
                                time = self.ui.comboBox_18.currentText()
                                the_time = time.split("=>")[1]
                            except:
                                self.etc.log("BAD time")
                            try:
                                ra = self.ui.comboBox_17.currentText()
                                the_ra = ra.split("=>")[1]
                            except:
                                self.etc.log("BAD right ascension")
                            
                            try:
                                dec = self.ui.comboBox_19.currentText()
                                the_dec = dec.split("=>")[1]
                            except:
                                self.etc.log("BAD declination")
                            try:
                                obs = self.ui.comboBox_22.currentText()
                                obs_file = open("{}/{}".format(
                                        self.etc.observat_dir, obs))
                                
                                for ln in obs_file:
                                    line = ln.replace("\n", "")
                                    
                                    if line.startswith("longitude|"):
                                        longitude = line.split("|")[1]
                                    elif line.startswith("latitude|"):
                                        latitude = line.split("|")[1]
                                    elif line.startswith("altitude|"):
                                        altitude = float(line.split("|")[1])
                                    elif line.startswith("timezone|"):
                                        timezone = float(line.split("|")[1])
                            except Exception as e:
                                self.etc.log(e)
                            
                            if (the_time is not None and the_ra is not None
                                and the_dec is not None 
                                and longitude is not None
                                and latitude is not None
                                and altitude is not None
                                and timezone is not None):
                                the_ra_deg = None
                                the_dec_deg = None
                                if ":" in the_ra and ":" in the_dec:
                                    the_ra_deg = self.clc.sex2deg(the_ra)
                                    the_dec_deg = self.clc.sex2deg(the_dec)
                                    the_dec_lat = self.clc.sex2deg(latitude)
                                    the_dec_lon = self.clc.sex2deg(longitude)
                                    
                                
                                if (the_ra_deg is not None
                                and the_dec_deg is not None):
                                    airmass = self.clc.airmass(the_ra_deg,
                                                               the_dec_deg,
                                                               the_dec_lat,
                                                               the_dec_lon,
                                                               altitude,
                                                               the_time,
                                                               0)
                                    if airmass is not None:
                                        self.fit.update_header(
                                                file, "{}amass".format(pref),
                                                airmass)
                                    else:
                                        self.etc.log("Arimass was not calculated properly")
                                else:
                                    self.etc.log(
                                            "Can not convert ra & dec")
                            else:
                                self.etc.log(
                                        "Check values for airmass calculation")
                    else:
                        #Log an error about not existing file
                        self.etc.log("No such (Calc)file({})".format(file))
                    g.proc(self, self.ui.progressBar_9, (it + 1) / len(files))
            else:
                #Log and display an error about no operation
                self.etc.log("Nothing to do")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Please select operation(s)"))
                
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to Calculate")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))

        #Reload log file to log view
        self.reload_log()

    #Change annotation of Calculator Tab
    def calculator_annotation(self):
        #Just find how many files were given for align
        img = g.list_lenght(self, self.ui.listWidget_16)
        proc = ""
        if self.ui.groupBox_33.isChecked():
            proc = "JD, {}".format(proc)
        
        if self.ui.groupBox_34.isChecked():
            proc = "Airmass, {}".format(proc)
            
        if self.ui.groupBox_35.isChecked():
            proc = "Imexamine, {}".format(proc)
        
        if self.ui.groupBox_14.isChecked():
            proc = "Time calculation, {}".format(proc)
            
        if len(proc) == 0:
            proc = "Nothing, "
        self.ui.label_49.setProperty("text",
                                    "{0} will be done to {1} files".format(
                                            proc[:-2], img))

        #Reload log file to log view
        self.reload_log()

    #Detect mouse clicks for coordinates extraction
    def mouseClick(self, event):
        #Check if the click was a left click
        if event.button == 1:
            #Check if the click was happened when Align tab was displayed
            if self.ui.tabWidget.currentIndex() == 1:
                #Check if x and y coordinates were obtained
                if event.ydata != None and event.xdata != None:
                    #Check if any file name was selected while click happened
                    img = self.ui.listWidget.currentItem()
                    if img is not None:
                        #Get file name
                        img = img.text()
                        #Check if file exist
                        if self.fit.is_fit(img):
                            #Get number of files were given
                            rows = self.ui.listWidget.count()
                            #Get current files order
                            row = self.ui.listWidget.currentRow()
                            #Read x and y coordinates
                            x = event.xdata
                            y = event.ydata
                            #Update files header and add 'mymancoo' key and add
                            #x, y coordinates as value
                            self.fit.update_header(
                                    img, "mymancoo", "{}, {}".format(x, y))
                            #Check if current order is not the last file
                            if row < rows-1:
                                #Go to next file
                                self.ui.listWidget.setCurrentRow(row+1)
                            else:
                                #Make a BEEP sound and go to first file
                                self.etc.beep()
                                self.ui.listWidget.setCurrentRow(0)
                        else:
                            #Log and display an error about empty listWidget
                            self.etc.log(
                                    "Bad fits or no such a (Disp Align Coor)file({})".format(
                                            img))
                            QtWidgets.QMessageBox.critical(
                                    self, ("MYRaf Error"),
                                    ("Bad fits or no such a file"))
                            
                        self.display_align()
                
            #Check if the click was happened when Photometry tab was displayed
            elif self.ui.tabWidget.currentIndex() == 2:
                #Check if x and y coordinates were obtained
                if event.ydata != None and event.xdata != None:
                    #Check if any file name was selected while click happened
                    img = self.ui.listWidget_2.currentItem()
                    if img is not None:
                        #Get file name
                        img = img.text()
                        #Check if file exist
                        if self.fit.is_fit(img):
                            #Read x and y coordinates
                            x = event.xdata
                            y = event.ydata
                            #add coordinates to coordinates listwidget
                            g.c_add(self, self.ui.listWidget_14,
                                    ["{:0.4f}, {:0.4f}".format(x, y)])
                            
                        else:
                            #Log and display an error about empty listWidget
                            self.etc.log(
                                    "Bad fits or no such a (Photometry Add Source)file({})".format(img))
                            QtWidgets.QMessageBox.critical(
                                    self, ("MYRaf Error"),
                                    ("Bad fits or no such a file"))
        if event.button == 2:
            #Check if the click was happened when Align tab was displayed
            if (self.ui.tabWidget.currentIndex() == 2 and self.ui.tabWidget_6.currentIndex() == 0):
                menu = QtWidgets.QMenu()
                menu.addAction('FWHM', lambda: (self.fwhm_clc(event)))
                menu.exec_(x, y)
            
            #Reload log file to log view
            self.reload_log()

    def get_graph_file_path(self):
        pth = self.fop.abs_path(g.get_graph_file_path(self))
        self.ui.label_31.setProperty("text", pth)
        graph_arr = self.fop.read_array(pth)
        if graph_arr is not None:
            the_range = []
            for i in range(graph_arr.shape[1]):
                the_range.append(str(i))
                
            g.c_replace_list_con(self, self.ui.comboBox_13, the_range)
            g.c_replace_list_con(self, self.ui.comboBox_14, the_range)
            g.c_replace_list_con(self, self.ui.comboBox_15, the_range)
            
        else:
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("Bad rowxcolumn for given file({})".format(pth)))
        
        #Reload log file to log view
        self.reload_log()
    
    #Zero Combine Method
    def zero_combine(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_7):
            if g.list_lenght(self, self.ui.listWidget_7) > 3:
                #Where to save the file
                dest = g.save_file(self)
                #Check if the path is available
                if dest:
                    self.ui.label.setText("Zero combine started")
                    #Get the method
                    if not dest.endswith(".fit") or not dest.endswith(".fits"):
                        dest = "{}.fits".format(dest)
                    met = self.ui.comboBox_2.currentText()
                    rej = self.ui.comboBox_3.currentText()
                    file_list = g.list_of_list(self, self.ui.listWidget_7)
                    self.cal.the_zerocombine(file_list, dest,
                                             method=met, rejection=rej)
                    self.ui.label.setText("Zero combine done")
                    
                else:
                    self.etc.log("No path was given to save")
            else:
                self.etc.log("No enough input")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Zerocombine expects atleast 3 files"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to (z)combine")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
           
    #Dark Combine Method
    def dark_combine(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_8):
            if g.list_lenght(self, self.ui.listWidget_8) > 3:
                #Where to save the file
                dest = g.save_file(self)
                #Check if the path is available
                if dest:
                    self.ui.label.setText("Dark combine started")
                    if not dest.endswith(".fit") or not dest.endswith(".fits"):
                        dest = "{}.fits".format(dest)
                    met = self.ui.comboBox_4.currentText()
                    rej = self.ui.comboBox_5.currentText()
                    scl = self.ui.comboBox_8.currentText()
                    file_list = g.list_of_list(self, self.ui.listWidget_8)
                    
                    if scl == "exposure":
                        new_file_list = []
                        for i in file_list:
                            expt = self.fit.header(
                                    i, self.ui.lineEdit_13.text())

                            if expt is not None:
                                self.fit.update_header(i, "EXPTIME", expt[1])
                                self.fit.update_header(i, "EXPOSURE", expt[1])

                            new_file_list.append(i)
                                
                        file_list = new_file_list
                        
                    the_zero = None
                    if not g.is_list_empty(self, self.ui.listWidget_7):
                        answ = g.question(self, "Do you want Bias correction?")
                        if answ == QtWidgets.QMessageBox.Yes:
                            try:
                                self.etc.log("Zero correction wanted")
                                zmet = self.ui.comboBox_2.currentText()
                                zrej = self.ui.comboBox_3.currentText()
                                zfile_list = g.list_of_list(
                                        self, self.ui.listWidget_7)
                                self.cal.the_zerocombine(
                                        zfile_list, "/tmp/myraf_bias.fits",
                                        method=zmet, rejection=zrej)
                                the_zero = "/tmp/myraf_bias.fits"
                            except Exception as e:
                                self.etc.log(e)
                        
                    self.cal.the_darkcombine(
                            file_list, dest, zero=the_zero,
                            method=met, rejection=rej, scale=scl)
                    self.ui.label.setText("Dark combine done")
                    
                else:
                    self.etc.log("No path was given to save")
            else:
                self.etc.log("No enough input")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Daekcombine expects atleast 3 files"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to (d)combine")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
            
    #Flat Combine Method
    def flat_combine(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_9):
            if g.list_lenght(self, self.ui.listWidget_9) > 3:
                dest = g.save_file(self)
                #Check if the path is available
                if dest:
                    self.ui.label.setText("Flat combine started")
                    if not dest.endswith(".fit") or not dest.endswith(".fits"):
                        dest = "{}.fits".format(dest)
                        
                    met = self.ui.comboBox_6.currentText()
                    rej = self.ui.comboBox_7.currentText()
                    sub = self.ui.comboBox_9.currentText()
                    file_list = g.list_of_list(self, self.ui.listWidget_9)
                    
                    if sub == "yes":
                        new_file_list = []
                        for i in file_list:
                            subs1 = self.fit.header(i, "SUBSET")
                            subs2 = self.fit.header(i, "FILTER")
                            subs3 = self.fit.header(
                                    i, self.ui.lineEdit_14.text())
                            
                            if subs1 is not None:
                                new_file_list.append(i)
                            elif subs2 is not None:
                                self.fit.update_header(i, "SUBSET", subs2[1])
                                new_file_list.append(i)
                            elif subs3 is not None:
                                self.fit.update_header(i, "SUBSET", subs3[1])
                                self.fit.update_header(i, "FLITER", subs3[1])
                                new_file_list.append(i)
                            
                        path, name, ext = self.fop.split_file_name(dest)
                        file_list = new_file_list
                        dest = "{}/{}".format(path, name)
                        
                    the_zero = None
                    if not g.is_list_empty(self, self.ui.listWidget_7):
                        answ = g.question(self, "Do you want Bias correction?")
                        if answ == QtWidgets.QMessageBox.Yes:
                            try:
                                self.etc.log("Zero correction wanted")
                                zmet = self.ui.comboBox_2.currentText()
                                zrej = self.ui.comboBox_3.currentText()
                                zfile_list = g.list_of_list(
                                        self, self.ui.listWidget_7)
                                self.cal.the_zerocombine(
                                        zfile_list, "/tmp/myraf_bias.fits",
                                        method=zmet, rejection=zrej)
                                the_zero = "/tmp/myraf_bias.fits"
                            except Exception as e:
                                self.etc.log(e)
                        
                    the_dark = None
                    if not g.is_list_empty(self, self.ui.listWidget_8):
                        answ = g.question(self, "Do you want Dark correction?")
                        if answ == QtWidgets.QMessageBox.Yes:
                            self.etc.log("Dark correction wanted")
                            try:
                                dmet = self.ui.comboBox_4.currentText()
                                drej = self.ui.comboBox_5.currentText()
                                dscl = self.ui.comboBox_8.currentText()
                                dfile_list = g.list_of_list(
                                        self, self.ui.listWidget_8)
                                
                                if dscl == "exposure":
                                    dnew_file_list = []
                                    for i in dfile_list:
                                        dexpt1 = self.fit.header(i, "EXPTIME")
                                        dexpt2 = self.fit.header(i, "EXPOSURE")
                                        dexpt3 = self.fit.header(
                                                i, self.ui.lineEdit_13.text())
                                        
                                        if (dexpt1 is not None
                                            or dexpt2 is not None):
                                            dnew_file_list.append(i)
                                        elif dexpt3 is not None:
                                            self.fit.update_header(
                                                    i, "EXPTIME", dexpt3[1])
                                            self.fit.update_header(
                                                    i, "EXPOSURE", dexpt3[1])
                                            dnew_file_list.append(i)
                                            
                                    dfile_list = dnew_file_list
                                    
                                self.cal.the_darkcombine(
                                        dfile_list, "/tmp/myraf_dark.fits",
                                        zero=the_zero, method=dmet,
                                        rejection=drej, scale=dscl)
                                the_dark = "/tmp/myraf_dark.fits"
                            except Exception as e:
                                self.etc.log(e)
                            
                    self.cal.the_flatcombine(
                            file_list, dest, dark=the_dark, zero=the_zero,
                            method=met, rejection=rej, subset=sub)
                    self.ui.label.setText("Flat combine done")
                
                else:
                    self.etc.log("No path was given to save")
            else:
                self.etc.log("No enough input")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Flatcombine expects atleast 3 files"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to (f)combine")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
            
        #Reload log file to log view
        self.reload_log()
            
    #Display fit file on Cosmic Cleaner Tab
    def display_cosmicC(self):
        #Check if file does exist
        img = self.ui.listWidget_5.currentItem().text()
        #Find the possible file name
        if self.fit.is_fit(img):
            try:
                #Display the file
                self.cocmicC_disp.load(str(img))
            except Exception as e:
                #Log error if any occurs
                self.etc.log(e)
        else:
            #Log and display an error about not existing file
            self.etc.log("Bad fits or no such a (Disp cosmicC)file({})".format(
                    img))
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Bad fits or no such a file"))
            
        #Reload log file to log view
        self.reload_log()
       
    def get_man_coo(self):
        #Find the possible file name
        img = self.ui.listWidget.currentItem().text()
        #Check if file does exist
        if self.fit.is_fit(img):
            the_coo = self.fit.header(img, field="mymancoo")
            if the_coo is not None:
                try:
                    #Split x, y coordinates by ", "
                    x, y = the_coo[1].split(", ")
                    #Convert x coordinate to float dtype
                    x = float(x)
                    #Convert y coordinate to float dtype
                    y = float(y)
                    #Get the aperture value
                    ap = float(self.ui.doubleSpinBox_5.value())
                    #Make a circle with x, y coordinates and ap aperture value
                    circ = Circle((x, y), ap * 1.3,
                                  edgecolor="#00FFFF", facecolor="none")
                    #Add circle to canvas
                    self.ui.disp_align.canvas.fig.gca().add_artist(circ)
                    #Make the circle's center x, y
                    circ.center = x, y
                    
                    #Add iteration value as label
                    self.ui.disp_align.canvas.fig.gca().annotate(
                            "Ref", xy = (x, y), xytext=(int(ap)/3,int(ap)/3),
                            textcoords='offset points', color = "red",
                            fontsize = 10) 
                    self.ui.disp_align.canvas.draw()
                except Exception as e:
                    self.etc.log(e)
            else:
                self.etc.log("No Manual Align coordinate found")
        else:
            #Log an error about not existing file
            self.etc.log("Bad or no such a (Disp Align Coor)file({})".format(
                    img))
            
        
        #Reload log file to log view
        self.reload_log()
        
    #Display fit file on Align Tab
    def display_align(self):
        #Find the possible file name
        if self.ui.listWidget.currentItem() is not None:
            img = self.ui.listWidget.currentItem().text()
            #Check if file does exist
            if self.fit.is_fit(img):
                try:
                    #Display the file
                    self.align_disp.load(str(img))
                    self.get_man_coo()
                except Exception as e:
                    #Log error if any occurs
                    self.etc.log(e)
            else:
                #Log and display an error about not existing file
                self.etc.log("Bad fits or no such a (Disp Align)file({})".format(img))
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Bad fits or no such a file"))
            
        #Reload log file to log view
        self.reload_log()
        
    #Display fit file on Photometry Tab
    def display_phot(self):
        #Find the possible file name
        if self.ui.listWidget_2.currentItem() is not None:
            img = self.ui.listWidget_2.currentItem().text()
            #Check if file does exist
            if self.fit.is_fit(img):
                try:
                    #Display the file
                    self.phot_disp.load(str(img))
                except Exception as e:
                    #Log error if any occurs
                    self.etc.log(e)
            else:
                #Log and display an error about not existing file
                self.etc.log("Bad fits or no such a (Disp Photometry)file({})".format(img))
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Bad fits or no such a file"))
            
        #Reload log file to log view
        self.reload_log()
        
    #Display fit file on A-Track Tab
    def display_atrack(self):
        #Find the possible file name
        img = self.ui.listWidget_13.currentItem().text()
        #Check if file does exist
        if self.fit.is_fit(img):
            try:
                #Display the file
                self.atrack_disp.load(str(img))
            except Exception as e:
                #Log error if any occurs
                self.etc.log(e)
        else:
            #Log and display an error about not existing file
            self.etc.log("Bad fits or no such a (Disp A-Track)file({})".format(
                    img))
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Bad fits or no such a file"))
            
        #Reload log file to log view
        self.reload_log()
    
    #Get a header key and it's value to textEdit fields 
    def get_the_header(self):
        if self.ui.listWidget_4.currentItem() is not None:
            #Get the header's line
            line = self.ui.listWidget_4.currentItem().text()
            #Split the line by "=>" so the field and value is obtaned
            field, value = line.split("=>")
            #Set (value)text of field textEdit
            self.ui.lineEdit.setProperty("text", field)
            #Set (value)text of value textEdit
            self.ui.lineEdit_2.setProperty("text", value)
        else:
            #Log and display an error about not existing file
            self.etc.log("No such (Get the header)header")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("I don't know how you managed that. But No header was selected"))
        
        #Reload log file to log view
        self.reload_log()
        
    #Get whole list of headers of a fits file
    def header_list(self):
        #Get file's name
        img = self.ui.listWidget_3.currentItem().text()
        #Check if file does exist
        if self.fit.is_fit(img):
            try:
                #Get all headers of give file
                all_header = self.fit.header(img)
                #convert [key, value] to "key=>value" format in an array
                header_list = []
                for i in all_header:
                    header_list.append("{}=>{}".format(i[0], i[1]))
                
                #Replace whole list with header list
                g.replace_list_con(self, self.ui.listWidget_4, header_list)
                #Replace whole combo with header list
                g.c_replace_list_con(self, self.ui.comboBox_12, header_list)
            except Exception as e:
                #Log error if any occurs
                self.etc.log(e)
        else:
            #Log and display an error about not existing file
            self.etc.log("Bad fits or no such a (Header List)file({})".format(
                    img))
            QtWidgets.QMessageBox.critical(
                self, ("MYRaf Error"), ("Bad fits or no such a file"))
    
        #Reload log file to log view
        self.reload_log()
        
    #Start Calibration
    def do_calibration(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_6):
            #Ask user for output directory
            ret_dir = g.save_directory(self)
            #Check if output dir is valid
            if self.fop.is_dir(ret_dir):
                
                #Read settings for zerocombine
                zmet = self.ui.comboBox_2.currentText()
                zrej = self.ui.comboBox_3.currentText()
                
                #Read settings for darkcombine
                dmet = self.ui.comboBox_4.currentText()
                drej = self.ui.comboBox_5.currentText()
                dscl = self.ui.comboBox_8.currentText()
                
                #Read settings for flatcombine
                fmet = self.ui.comboBox_6.currentText()
                frej = self.ui.comboBox_7.currentText()
                fsub = self.ui.comboBox_9.currentText()
                
                #Progressbar status
                perc_pre = 0
                
                #Get list of files
                file_list = g.list_of_list(self, self.ui.listWidget_6)
                
                #Same as zerocombine.
                the_zero = None
                if not g.is_list_empty(self, self.ui.listWidget_7):
                    try:
                        zfile_list = g.list_of_list(self, self.ui.listWidget_7)
                        self.ui.label.setText("Zero combine started")
                        if g.list_lenght(self, self.ui.listWidget_7) > 3:
                            self.cal.the_zerocombine(
                                    zfile_list, "/tmp/myraf_bias.fits",
                                    method=zmet, rejection=zrej)
                        else:
                            the_zero_file = zfile_list[0]
                            self.fop.cp(the_zero_file, "/tmp/myraf_bias.fits")
                            
                        the_zero = "/tmp/myraf_bias.fits"
                        perc_pre += 0.1
                        self.ui.label.setText("Zero combine done")
                    except Exception as e:
                        self.etc.log(e)
                else:
                    #Log and display an error about empty listWidget
                    self.etc.log("No zero correction wanted")
                
                g.proc(self, self.ui.progressBar, perc_pre)
                
                #Same as darkcombine.
                the_dark = None
                if not g.is_list_empty(self, self.ui.listWidget_8):
                    try:
                        dfile_list = g.list_of_list(self, self.ui.listWidget_8)
                        self.ui.label.setText("Dark combine started")
                        if g.list_lenght(self, self.ui.listWidget_8) > 3:
                            if dscl == "exposure":
                                dnew_file_list = []
                                for i in dfile_list:
                                    expt1 = self.fit.header(i, "EXPTIME")
                                    expt2 = self.fit.header(i, "EXPOSURE")
                                    expt3 = self.fit.header(
                                            i, self.ui.lineEdit_13.text())
                                    
                                    if expt1 is not None or expt2 is not None:
                                        dnew_file_list.append(i)
                                    elif expt3 is not None:
                                        self.fit.update_header(
                                                i, "EXPTIME", expt3[1])
                                        self.fit.update_header(
                                                i, "EXPOSURE", expt3[1])
                                        dnew_file_list.append(i)
                                        
                                dfile_list = dnew_file_list
                                
                                new_file_list = []
                                for i in file_list:
                                    expt1 = self.fit.header(i, "EXPTIME")
                                    expt2 = self.fit.header(i, "EXPOSURE")
                                    expt3 = self.fit.header(
                                            i, self.ui.lineEdit_13.text())
                                    
                                    if expt1 is not None or expt2 is not None:
                                        new_file_list.append(i)
                                    elif expt3 is not None:
                                        self.fit.update_header(
                                                i, "EXPTIME", expt3[1])
                                        self.fit.update_header(
                                                i, "EXPOSURE", expt3[1])
                                        new_file_list.append(i)
                                        
                                file_list = new_file_list
                                
                            self.cal.the_darkcombine(
                                    dfile_list, "/tmp/myraf_dark.fits",
                                    zero=None, method=dmet,
                                    rejection=drej, scale=dscl)
                        else:
                            the_dark_file = dfile_list[0]
                            self.fop.cp(the_dark_file, "/tmp/myraf_dark.fits")
                        
                        the_dark = "/tmp/myraf_dark.fits"
                        perc_pre += 0.1
                        self.ui.label.setText("Dark combine done")
                    except Exception as e:
                        self.etc.log(e)
                else:
                    self.etc.log("No dark correction wanted")
                    
                g.proc(self, self.ui.progressBar, perc_pre)
                
                #Same as flatcombine.
                the_flats = None
                if not g.is_list_empty(self, self.ui.listWidget_9):
                    try:
                        ffile_list = g.list_of_list(self, self.ui.listWidget_9)
                        self.ui.label.setText("Flat combine started")
                        if g.list_lenght(self, self.ui.listWidget_9) > 3:
                            if fsub == "yes":
                                
                                fnew_file_list = []
                                for i in ffile_list:
                                    subs1 = self.fit.header(i, "SUBSET")
                                    subs2 = self.fit.header(i, "FILTER")
                                    subs3 = self.fit.header(
                                            i, self.ui.lineEdit_14.text())
                                    
                                    if subs1 is not None:
                                        fnew_file_list.append(i)
                                    elif subs2 is not None:
                                        self.fit.update_header(
                                                i, "SUBSET", subs2[1])
                                        fnew_file_list.append(i)
                                    elif subs3 is not None:
                                        self.fit.update_header(
                                                i, "SUBSET", subs3[1])
                                        self.fit.update_header(
                                                i, "FLITER", subs3[1])
                                        fnew_file_list.append(i)
                                        
                                ffile_list = fnew_file_list
                                
                                
                                new_file_list = []
                                for i in file_list:
                                    subs1 = self.fit.header(i, "SUBSET")
                                    subs2 = self.fit.header(i, "FILTER")
                                    subs3 = self.fit.header(
                                            i, self.ui.lineEdit_14.text())
                                    
                                    if subs1 is not None:
                                        new_file_list.append(i)
                                    elif subs2 is not None:
                                        self.fit.update_header(
                                                i, "SUBSET", subs2[1])
                                        new_file_list.append(i)
                                    elif subs3 is not None:
                                        self.fit.update_header(
                                                i, "SUBSET", subs3[1])
                                        self.fit.update_header(
                                                i, "FLITER", subs3[1])
                                        new_file_list.append(i)
                                        
                                file_list = new_file_list
                                self.cal.the_flatcombine(
                                        file_list, "/tmp/myraf_flat_",
                                        dark=None, zero=None, method=fmet,
                                        rejection=frej, subset=fsub)
                                
                        else:
                            for flat_file in ffile_list:
                                subs = self.fit.header(flat_file, "SUBSET")
                                self.fop.cp(flat_file,
                                            "/tmp/myraf_flat_{}".format(subs))
                                
                        the_flats = "/tmp/myraf_flat_*"
                        perc_pre += 0.1
                        self.ui.label.setText("Flat combine done")
                    except Exception as e:
                        self.etc.log(e)
                else:
                    self.etc.log("No flat correction wanted")
                    
                g.proc(self, self.ui.progressBar, perc_pre)
                
                #Loop in file names
                for it, file in enumerate(file_list):
                    #Create output file path
                    path, name, ext = self.fop.split_file_name(file)
                    out_file = self.fop.abs_path("{}/{}{}".format(
                            ret_dir, name, ext))
                    
                    #Remove output file is it's already exist
                    if self.fop.is_file(out_file):
                        self.fop.rm(out_file)
                        
                    #Do the calibration as wanted
                    self.cal.the_calibration(file, out_file, zero=the_zero,
                                             dark=the_dark, flat=the_flats,
                                             subset=fsub)
                    
                    #Update header
                    self.fit.update_header(out_file, "MYCAL",
                                           "Calibration done By MyRAF")
                    
                    per = (1 - perc_pre) * ((1 + it)/len(file_list))
                    g.proc(self, self.ui.progressBar, perc_pre + per)
                    self.ui.label.setText(
                            "Calibration done for {}".format(file))
            else:
                self.etc.log("No path was given to save")
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to calibrate.")
            QtWidgets.QMessageBox.critical(
                    self,  ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
        
    #Change annotation of Calibration Tab
    def calibration_annotation(self):
        #Just find how many files were given as BDF and images
        img = g.list_lenght(self, self.ui.listWidget_6)
        zer = g.list_lenght(self, self.ui.listWidget_7)
        dar = g.list_lenght(self, self.ui.listWidget_8)
        fla = g.list_lenght(self, self.ui.listWidget_9)
        pre = "File(s) will be calibrated using"
        self.ui.label.setProperty(
                "text",
                "{0} {1} {2} Bias(es), {3} Dark(s) and {4} Flat(s)".format(
                        img, pre, zer, dar, fla))
    
    #Start Alignment
    def do_align(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget):
            #Check if Auto Align is selected
            if self.ui.checkBox.isChecked():
                self.etc.log("Auto Align was stared")
                #Check if reference(ref) file was selected
                if self.ui.listWidget.currentItem() is not None:
                    #Get refrence files name
                    ref = self.ui.listWidget.currentItem().text()
                    #Check if ref file exist
                    if self.fit.is_fit(ref):
                        #ask user for output directory(dir)
                        odir = str(QtWidgets.QFileDialog.getExistingDirectory(
                                self, "Select Directory"))
                        #Check if output dir was selected
                        if self.fop.is_dir(odir):
                            files = g.list_of_list(self, self.ui.listWidget)
                            #Loop in file names was given
                            for file in files:
                                #Check if file is a fit file
                                if self.fit.is_fit(file):
                                    self.fit.autolign(file, ref, odir)
                            
                    
                else:
                    #Log and display an error about not selected ref image
                    self.etc.log("Bad fits or no such a (AAlign ref)file({})")
                    QtWidgets.QMessageBox.critical(
                            self,  ("MYRaf Error"),
                            ("Bad fits or no such a reference file"))
            else:
                self.etc.log("Manual Align was stared")
                #Check if reference(ref) file was selected
                if self.ui.listWidget.currentItem() is not None:
                    #Get refrence files name
                    ref = self.ui.listWidget.currentItem().text()
                    #Check if ref file exist
                    if self.fit.is_fit(ref):
                        #Get ref file's align coordinates
                        ref_coors = self.fit.header(ref, "mymancoo")
                        #Check if ref coordinates are available
                        if ref_coors is not None:
                            #Gey x and y values of ref coordinates
                            ref_coors = ref_coors[1]
                            #ask user for output directory(dir)
                            odir = str(
                                    QtWidgets.QFileDialog.getExistingDirectory(
                                            self, "Select Directory"))
                            #Check if output dir was selected
                            if self.fop.is_dir(odir):
                                #Loop in file names was given
                                for i in range(self.ui.listWidget.count()):
                                    #Get current files name
                                    img = self.ui.listWidget.item(i).text()
                                    #Check if file is a fit file
                                    if self.fit.is_fit(img):
                                        #Read coordinates of current file
                                        coors = self.fit.header(
                                                img, "mymancoo")
                                        #Check if coordinates are available
                                        if coors is not None:
                                            #Get current coordinates
                                            coors = coors[1]
                                            #Create output file path
                                            fp, fn = self.fop.get_base_name(
                                                    img)
                                            new_path = self.fop.abs_path(
                                                    "{}/{}".format(odir, fn))
                                            #extract ref and current files 
                                            #coordinates
                                            ry = float(
                                                    ref_coors.split(", ")[0])
                                            rx = float(
                                                    ref_coors.split(", ")[1])
                                            ty = float(coors.split(", ")[0])
                                            tx = float(coors.split(", ")[1])
                                            # Calculate the x and y shit
                                            x = rx - tx
                                            y = ry - ty
                                            #Shit the input file
                                            self.fit.shift(new_path, img, x, y)
                                            
                                        else:
                                            #Log an error about Not
                                            #existing coor
                                            pre = "No coordinate was selected"
                                            self.etc.log(
                                                    "{} for file({})".format(
                                                            pre, img))
                                    else:
                                        #Log an error about Not existing file
                                        self.etc.log(
                                                "Bad fits or no such a (MAlign)file({})".format(img))
                                        
                                    g.proc(self,
                                           self.ui.progressBar_2,
                                           (i + 1)/g.list_lenght(
                                                   self, self.ui.listWidget))
                            else:
                                #Log an error about Not existing out dir
                                self.etc.log("No out dir found({})".format(
                                        odir))
                        else:
                            #Log and display an error about
                            #Not existing ref coors
                            self.etc.log("Referance image has no coordinates")
                            QtWidgets.QMessageBox.critical(
                                    self,  ("MYRaf Error"),
                                    ("Please select Coor on Ref image"))
                    else:
                        #Log and display an error about Not existing ref image
                        self.etc.log("No Referance image() found".format(ref))
                        QtWidgets.QMessageBox.critical(
                                self,  ("MYRaf Error"),
                                ("No reference image found"))
                else:
                    #Log and display an error about not selected ref image
                    self.etc.log("No Reference image was selected")
                    QtWidgets.QMessageBox.critical(
                            self,  ("MYRaf Error"),
                            ("No reference image selected"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to align.")
            QtWidgets.QMessageBox.critical(
                    self,  ("MYRaf Error"), ("Please add some files"))
    
        #Reload log file to log view
        self.reload_log()
    
    #Change annotation of Align Tab
    def align_annotation(self):
        #Just find how many files were given for align
        img = g.list_lenght(self, self.ui.listWidget)
        self.ui.label_2.setProperty("text",
                                    "{0} file(s) will be aligned".format(img))
    
    def a_track(self):
        if not g.is_list_empty(self, self.ui.listWidget_13):
            for i in range(self.ui.listWidget_14.count()):
                img = self.ui.listWidget_13.item(i).text()
                if self.fit.is_fit(img):
                    print(img)
                else:
                    self.etc.log("Bad fits or no such a (a-track)file({})".format(img))
        else:
            self.etc.log("Nothing to track.")
            QtWidgets.QMessageBox.critical(
                    self,  ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
        
    def display_coors_phot(self):
        if self.ui.listWidget_2.currentItem() is None:
            if len(self.ui.listWidget_14.selectedItems()) != 0:
                msg1 = "Did you just import the coordinates and selected"
                msg2 = " no image or removed the image before displaying"
                msg3 = " SPECIFIC coordinates?\nCongratulations!"
                msg4 = " You have reached to the NIRVANA."
                self.etc.log(
                        "No file in display & specific coordinates draw")
                QtWidgets.QMessageBox.critical( 
                        self, ("MYRaf OMFG!"),
                        ("{}{}{}{}".format(msg1, msg2, msg3, msg4)))
                self.etc.user_is_a_monkey()
            else:
                self.etc.log("No file in display & coordinate draw wanted")
                QtWidgets.QMessageBox.critical( 
                        self, ("MYRaf OMFG!"),
                        ("Plase select n image to draw on"))
        else:
            #Refresh display
            self.display_phot()
            #Check if any specific coordinate was selected
            if len(self.ui.listWidget_14.selectedItems()) != 0:
                #User selected some coordinates to display
                self.etc.log("Displaying selected coordinates")
                #Loop in all coordinates
                for it, coo in enumerate(self.ui.listWidget_14.selectedItems()):
                    try:
                        #Convfert coodinate line to string dtype
                        the_coo = str(coo.text())
                        #Split x, y coordinates by ", "
                        x, y = the_coo.split(", ")
                        #Convert x coordinate to float dtype
                        x = float(x)
                        #Convert y coordinate to float dtype
                        y = float(y)
                        #Get the aperture value
                        ap = float(self.ui.doubleSpinBox_5.value())
    
                        #Make a circle with x, y coordinates and ap aperture value
                        circ = Circle((x, y), ap * 1.3, edgecolor="#00FFFF",
                                      facecolor="none")
                        #Add circle to canvas
                        self.ui.disp_photometry.canvas.fig.gca().add_artist(
                                circ)
                        #Make the circle's center x, y
                        circ.center = x, y
                        #Add iteration value as label
                        self.ui.disp_photometry.canvas.fig.gca().annotate(
                                it + 1, xy = (x, y), xytext=(int(ap)/3,int(ap)/3),
                                textcoords='offset points', color = "red",
                                fontsize = 10)
                    except Exception as e:
                        #Log error if any occurs
                        self.etc.log(e)
                try:
                    self.etc.log("Drawing coordinates")
                    #Draw all coordinates
                    self.ui.disp_photometry.canvas.draw()
                except Exception as e:
                    #Log error if any occurs
                    self.etc.log(e)
            else:
                #User did not select any coordinates to display. Drawing all
                self.etc.log("Displaying all coordinates")
                #Check if coordinates list is empty
                if not g.is_list_empty(self, self.ui.listWidget_14):
                    #List is not empty
                    #Loop in all coordinates
                    for it, i in enumerate(range(
                            self.ui.listWidget_14.count())):
                        #Get coordinate from the item
                        coo = self.ui.listWidget_14.item(i).text()
                        try:
                            the_coo = str(coo)
                            #Split x, y coordinates by ", "
                            x, y = the_coo.split(", ")
                            #Convert x coordinate to float dtype
                            x = float(x)
                            #Convert y coordinate to float dtype
                            y = float(y)
                            #Get the aperture value
                            ap = float(self.ui.doubleSpinBox_5.value())
                            
                            #Make a circle with x, y coordinates and ap
                            #                               aperture value
                            circ = Circle((x, y), ap * 1.3, edgecolor="#00FFFF", facecolor="none")
                            #Add circle to canvas
                            self.ui.disp_photometry.canvas.fig.gca().add_artist(circ)
                            #Make the circle's center x, y
                            circ.center = x, y
                            #Add iteration value as label
                            self.ui.disp_photometry.canvas.fig.gca().annotate(
                                    it + 1, xy = (x, y),
                                    xytext=(int(ap)/3,int(ap)/3),
                                    textcoords='offset points', color = "red",
                                    fontsize = 10)
                        except Exception as e:
                            #Log any error if any occurs
                            self.etc.log(e)
                    try:
                        self.etc.log("Drawing coordinates")
                        #Draw all coordinates
                        self.ui.disp_photometry.canvas.draw()
                    except Exception as e:
                        #Log any error if any occurs
                        self.etc.log(e)
                else:
                    self.etc.log("No coordinate was given")
                    QtWidgets.QMessageBox.critical(
                            self, ("MYRaf Error"), ("No coordinate was given"))

            
        #Reload log file to log view
        self.reload_log()
        
    def run_sex(self):
        #Check if any image file was selected
        if self.ui.listWidget_2.currentItem() is not None:
            #File was selected
            #Get file's name
            img = self.ui.listWidget_2.currentItem().text()
            #Check if file exist
            if self.fit.is_fit(img):
                try:
                    #Get data from file
                    data = self.fit.data(img, table=False)
                    #Get maximum object count to find
                    lim = int(self.ui.spinBox.value())
                    #Get coordinates from the img file
                    coors = self.sex.find_limited(data, max_sources=lim)
                    #Declare a list variable
                    sex_coors = []
                    for i in coors:
                        #Add all coordinates to list as string
                        #with "X, Y" format
                        sex_coors.append("{:0.4f}, {:0.4f}".format(
                                                            i['x'], i['y']))
                    #Add coordinate list to listwidget
                    g.replace_list_con(self, self.ui.listWidget_14, sex_coors)
                except Exception as e:
                    #Log error if any occurs
                    self.etc.log(e)
            else:
                #Log and display an error about not existing file
                self.etc.log("Bad fits or no such a (Run Sex)file({}).".format(
                        img))
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Bad fits or no such a file"))
        else:
            #Log and display an error about empty listWidget
           self.etc.log("No File was selected(Run Sex)")
           QtWidgets.QMessageBox.critical(
                   self, ("MYRaf Error"), ("No file was selected"))
           
        #Reload log file to log view
        self.reload_log()    
        
    def phot_hex(self):
        if not g.is_list_empty(self, self.ui.listWidget_2):
            files = g.list_of_list(self, self.ui.listWidget_2)
            hlist = None
            for file in files:
                if self.fit.is_fit(file):
                    headers = self.fit.header(file)
                    hlist = []
                    for header in headers:
                        hlist.append(header[0])
                    
                    break
            if hlist is not None:
                g.replace_list_con(self, self.ui.listWidget_19, hlist)
        
    #Start Photometry
    def do_phot(self):
        #Check if listWidget is empty (files)
        if not g.is_list_empty(self, self.ui.listWidget_2):
            #Check if listWidget is empty (coordinates)
            if not g.is_list_empty(self, self.ui.listWidget_14):
                #Ask user dor output directory
                odir = str(QtWidgets.QFileDialog.getExistingDirectory(
                                self, "Select Directory"))
                #Check if output dir is valid
                if self.fop.is_dir(odir):
                    #Get list of files
                    files = g.list_of_list(self, self.ui.listWidget_2)
                    
                    #Read settings for photometry
                    aperture = float(self.ui.doubleSpinBox_5.value())
                    zmag = float(self.ui.doubleSpinBox_8.value())
                    radius = 0.0027 * float(self.ui.doubleSpinBox.value())
                    
                    #Loop in files
                    for it, file in enumerate(files):
                        #Check if file is a valif fits file
                        if self.fit.is_fit(file):
                            #Create output file names
                            path, name, ext = self.fop.split_file_name(file)
                            the_data = self.fit.data(file, table=False)
                            
                            
                            the_return = []
                            
                            #Get list of coordinates
                            coords = g.list_of_list(
                                    self, self.ui.listWidget_14)
                            
                            #Read gain value
                            gain_header = self.ui.lineEdit_26.text()
                            try:
                                #Convert it to float
                                the_gain = float(gain_header)
                            except:
                                self.etc.log("Gain value was not a number. Trying to get it from header")
                                #Check if gain value is in header
                                gain = self.fit.header(file, gain_header)
                                if gain is not None:
                                    try:
                                        the_gain = float(gain[1])
                                    except:
                                        self.etc.log("Bad gain in header. Using defalut value({})".format(1.21))
                                        #Use standard gain value
                                        the_gain = 1.21
                                else:
                                    self.etc.log("No {} in header. Using defalut value({})".format(gain_header, 1.21))
                                    #Use standard gain value
                                    the_gain = 1.21
                            
                            #Loop in coordinates
                            for coord in coords:
                                #get x and y values
                                xys = coord.split(", ")
                                x = float(xys[0])
                                y = float(xys[1])
                                
                                #Do the photometry
                                flux, fluxunc, flag = self.pht.do(
                                        the_data, x, y,
                                        aper_radius=aperture, gain=the_gain)
                                #Convert flux to mag, merr
                                mag, merr = self.clc.flux2magmerr(
                                        flux, fluxunc)
                                #Add ZMag value
                                mag += zmag
                                
                                
                                NOMAD = None
                                USNO = None
                                GAIA = None
                                ra = None
                                dec = None
                                #Check if standard mags were wanted
                                if self.ui.groupBox_6.isChecked():
                                    self.etc.log("Standard mag wanted")
                                    #Convert x,y coordinates to WCS
                                    the_coors = self.clc.xy2sky(file, x, y)
                                    #Check if WCS is valid
                                    if the_coors is not None:
                                        ra, dec = the_coors
                                        
                                        #Check if NOMAD values were wanted
                                        if self.ui.checkBox_13.isChecked():
                                            #Get Nomad values
                                            NOMAD = self.cat.nomad(
                                                    ra, dec, radius=radius,
                                                    max_sources=1)
                                        
                                        #Check if usno values were wanted
                                        if self.ui.checkBox_14.isChecked():
                                            #Get usno values
                                            USNO = self.cat.usno(
                                                    ra, dec, radius=radius,
                                                    max_sources=1)
                                            
                                        #Check if gaia values were wanted
                                        if self.ui.checkBox_15.isChecked():
                                            #Get gaia values
                                            GAIA = self.cat.gaia(
                                                    ra, dec, radius=radius,
                                                    max_sources=1)
                                else:
                                    self.etc.log("No")
                                
                                #Check if NOMAD values are abailable
                                #If not add None values
                                if NOMAD is not None:
                                    nomad = [float(NOMAD["RAJ2000"]),
                                             float(NOMAD["DEJ2000"]),
                                             float(NOMAD["Bmag"]),
                                             float(NOMAD["Vmag"]),
                                             float(NOMAD["Rmag"])]
                                else:
                                    nomad = [None] * 5
                                    
                                #Check if USNO values are abailable
                                #If not add None values
                                if USNO is not None:
                                    usno = [float(USNO["RAJ2000"]),
                                            float(USNO["DEJ2000"]),
                                            float(USNO["Bmag"]),
                                            float(USNO["Rmag"])]
                                else:
                                    usno = [None] * 4
                                
                                #Check if HAIA values are abailable
                                #If not add None values
                                if GAIA is not None:
                                    gaia = [float(GAIA["RA_ICRS"]),
                                            float(GAIA["DE_ICRS"]),
                                            float(GAIA["__Gmag_"])]
                                else:
                                    gaia = [None] * 3
                                    
                                #Append a source's values
                                the_return.append(
                                        self.cnv.list2npar(
                                                [x, y, ra, dec, flux, fluxunc,
                                                 flag, mag, merr,
                                                 nomad[0], nomad[1], nomad[2],
                                                 nomad[3], nomad[4],
                                                 usno[0], usno[1], usno[2],
                                                 usno[3],
                                                 gaia[0], gaia[1], gaia[2]]))
                                        
                        #Append sources values
                        the_return = self.cnv.list2npar(the_return)
                        #Create output file name
                        out_file = "{}/{}.pho".format(odir, name)
                        #Write Outpıt file
                        file_header = ["X", "Y", "RA", "DEC", "FLUX",
                                       "FLUX_UNC", "FLAG" "MAG" "MERR",
                                       "NOMAD(ra)", "NOMAD(dec)", "NOMAD(B)",
                                       "NOMAD(V)", "NOMAD(R)", "USNO(RA)",
                                       "USNO(DEC)", "USNO(B)", "USNO(V)",
                                       "GAIA(RA)", "GAIA(DEC)", "GAIA(G)"]
                        wanted_headers = g.list_of_list(
                                self, self.ui.listWidget_20)
                        add_headers = []
                        
                        if len(wanted_headers) > 0:
                            for header in wanted_headers:
                                the_header = self.fit.header(file, header)
                                if the_header is not None:
                                    file_header.append(header)
                                    add_headers.append(the_header[1])
                                else:
                                    file_header.append(header)
                                    add_headers.append("None")
                        
                        f2w = open(out_file, "w")
                        f2w.write("#{}\n".format("\t".join(file_header)))
                        for line in the_return:
                            the_line = [str(i) for i in line]
                            the_header = [str(i) for i in add_headers]
                            write_line = "{}\t{}".format("\t".join(the_line),
                                          "\t".join(the_header))
                            f2w.write("{}\n".format(write_line))
                        f2w.close()
                                    
                        
                        g.proc(self,
                               self.ui.progressBar_4, (it + 1) / len(files))
                else:
                    #Log an error abıut Not existing out dir
                    self.etc.log("No out dir found({})".format(odir))
            else:
                #Log and display an error about empty listWidget
                self.etc.log("No coordinate was given for do photometry")
                QtWidgets.QMessageBox.critical(
                        self,  ("MYRaf Error"),
                        ("Please add some coordinates"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("No file was given for do photometry")
            QtWidgets.QMessageBox.critical(
                    self,  ("MYRaf Error"), ("Please add some files"))
    
        #Reload log file to log view
        self.reload_log()
    
    #Change annotation of Photometry Tab
    def phot_annotation(self):
        #Just find how many files were given for photometry
        img = g.list_lenght(self, self.ui.listWidget_2)
        self.ui.label_8.setProperty(
                "text", "Photometry will be done for {0} file(s)".format(img))
        
    #Change annotation of Photometry Tab
    def atrack_annotation(self):
        #Just find how many files were given for photometry
        img = g.list_lenght(self, self.ui.listWidget_13)
        self.ui.label_27.setProperty(
                "text", "A-Track will be done for {0} file(s)".format(img))
        
    #Do Hedit's Operation
    def do_hedit(self, update_add=True):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_3):
            #Check if any field was specified
            if not self.ui.lineEdit.text() == "":
                #Get field value
                field = self.ui.lineEdit.text()
                #Start an iteration for prgressBar
                for i in range(self.ui.listWidget_3.count()):
                    #Find the possible file name
                    img = self.ui.listWidget_3.item(i).text()
                    #Check if file exist
                    if self.fit.is_fit(img):
                        #Check if header must be updated/added or removed
                        if update_add:
                            #Header must be updated/added
                            try:
                                #Check if using an existion value
                                if self.ui.checkBox_5.isChecked():
                                    #Using an existing value
                                    #Get the "key=>value" for existing value
                                    combo = self.ui.comboBox_12.currentText()
                                    #Find wanted key by spliting it by "=>"
                                    wanted_filed = combo.split("=>")[0].strip()
                                    #Get the value of wanted key in header
                                    value = self.fit.header(
                                            img, wanted_filed)[1]
                                else:
                                    #Using a static value
                                    #Getting the value value
                                    value = self.ui.lineEdit_2.text()
                                    
                                #Updating the header
                                self.fit.update_header(img, field, value)
                            except Exception as e:
                                #Log error if any occurs
                                self.etc.log(e)
                                
                        else:
                            #Header must be removed
                            try:
                                #Remove header
                                self.fit.delete_header(img, field)
                            except Exception as e:
                                #Log the exception if it happened
                                self.etc.log(e)
                    else:
                        #Log and display an error about not existing file
                        self.etc.log("No such (Hedit)file({})".format(img))
                        
                    #Advance ProgressBar
                    g.proc(self, self.ui.progressBar_3, (i + 1)/g.list_lenght(
                                                self, self.ui.listWidget_3))
                #Reload header list in hedit view
                self.header_list()
            else:
                #Log and display an error about empty field
                self.etc.log("No field was specified.")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("No field was specified"))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("No file was given to Header Editor")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
    
    #Change Usage of Existing Header
    def use_existing_header(self):
        #Check if using an existing value
        if self.ui.checkBox_5.isChecked():
            #Using an existing value
            #Disable lineEdit and Enable Combobox
            self.ui.lineEdit_2.setEnabled(False)
            self.ui.comboBox_12.setEnabled(True)
        else:
            #Using a static value
            #Enable lineEdit and Disable Combobox
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.comboBox_12.setEnabled(False)
            
        self.reload_log()
    #Change annotation of Header Editor Tab
    def heditor_annotation(self):
        img = g.list_lenght(self, self.ui.listWidget_3)
        self.ui.label_10.setProperty(
                "text", "header for {0} files will be updated".format(img))
        
        #Reload log file to log view
        self.reload_log()
       
    #Start Cosmic Cleaning
    def do_cosmicC(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_5):
            #Get gain value from settings tab
            gain = float(self.ui.doubleSpinBox_20.value())
            #Get Readout Noise value from settings tab
            readN = float(self.ui.doubleSpinBox_21.value())
            #Get Sigma Clip value from settings tab
            sigmC = float(self.ui.doubleSpinBox_22.value())
            #Get Sigma Frac value from settings tab
            sigmF = float(self.ui.doubleSpinBox_23.value())
            #Get Object Limit value from settings tab
            objeL = float(self.ui.doubleSpinBox_24.value())
            #Get Maximum iteration value from settings tab
            max_it = int(self.ui.spinBox_2.value())
            #Get the output directory path from user
            odir = str(QtWidgets.QFileDialog.getExistingDirectory(
                        self, "Select Directory"))
            if self.fop.is_dir(odir):
                #Start a loop for each file name
                for i in range(self.ui.listWidget_5.count()):
                    #Find the possible file name
                    img = self.ui.listWidget_5.item(i).text()
                    #Check if file exist
                    if self.fit.is_fit(img):
                        try:
                            #Split file name and the path
                            pth, name = self.fop.get_base_name(img)
                            #User file name and path given
                            #to create new file path
                            ofile = self.fop.abs_path("{}/{}".format(
                                    odir, name))
                            #User file name and path given to
                            #create mask file path
                            mfile = self.fop.abs_path("{}/mask_{}".format(
                                    odir, name))
                            #Start cosmic clean
                            data, header = myCos.fromfits(img)
                            c = myCos.cosmicsimage(data, gain=gain,
                                                   readnoise=readN,
                                                   sigclip=sigmC,
                                                   sigfrac=sigmF,
                                                   objlim=objeL)
                            
                            c.run(maxiter=max_it)
                            if not self.fop.is_file(ofile):
                                myCos.tofits(ofile, c.cleanarray, header)
                            if self.ui.checkBox_3.isChecked():
                                if not self.fop.is_file(mfile):
                                    myCos.tofits(mfile, c.mask, header)
                            #Cosmic clean done
                        except Exception as e:
                            #Log error if any occurs
                            self.etc.log(e)
                    else:
                        #Log and display an error about not existing file
                        self.etc.log("No such (Cosmic Clean)file({})".format(
                                img))
                    
                    #Advance ProgressBar
                    g.proc(self, self.ui.progressBar_5, (i + 1)/g.list_lenght(
                            self, self.ui.listWidget_5))
            else:
                #Log an error about empty listWidget
                self.etc.log("No out dir found({})".format(odir))
        else:
            #Log and display an error about empty listWidget
            self.etc.log("Nothing to Cosimc Clean")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
    
    #Change annotation of Cosmic Cleaning Tab
    def cosmicC_annotation(self):
        #Just find how many files were given for Cosmic Cleaner
        img = g.list_lenght(self, self.ui.listWidget_5)
        self.ui.label_11.setProperty(
                "text", 
                "Cosmic Cleaning will be applied for {0} files".format(img))
        
    #Satrt WCS Operation
    def do_wcs(self):
        #Check if listWidget is empty
        if not g.is_list_empty(self, self.ui.listWidget_11):
            print("Start WCS")
        else:
            #Log and display an error about empty listWidget
            self.etc.log("No file was given to WCS Editor")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
            
        #Reload log file to log view
        self.reload_log()
        
    #Change annotation of WCS Tab
    def wcs_annotation(self):
        #Just find how many files were given for WCS
        img = g.list_lenght(self, self.ui.listWidget_11)
        self.ui.label_14.setProperty(
                "text",
                "Cosmic Cleaning will be applied for {0} files".format(img))
        
    def astrometrynet_check(self):
        if not self.etc.is_it_linux():
            self.etc.log("The system is not Linux and astrometry.net offline activated")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("Your os is not GNU/Linux. Use offline at your own risk"))
                
            
        #Reload log file to log view
        self.reload_log()
        
    def load_observat(self):
        #Get list of files in observat
        obs_files = self.fop.list_of_fiels(self.fop.abs_path(
                self.etc.observat_dir), ext="*")
        new_list = []
        for i in obs_files:
            new_list.append(self.fop.get_base_name(i)[1])
        g.replace_list_con(self, self.ui.listWidget_12, new_list)
        
        g.c_replace_list_con(self, self.ui.comboBox_22, new_list)
        
        #Reload log file to log view
        self.reload_log()
        
    def get_observat_prop(self):
        
        obs_name = self.ui.listWidget_12.currentItem().text()
        obs_path = self.fop.abs_path("{}/{}".format(
                self.etc.observat_dir, obs_name))
        if self.fop.is_file(obs_path):
            f_obs = open(obs_path, "r")
            comm = ""
            for i in f_obs:
                ln = i.replace("\n", "")
                
                if ln.startswith("observatory|"):
                    val = ln.split("|")[1]
                    self.ui.lineEdit_3.setText(str(val))
                    
                if ln.startswith("name|"):
                    val = ln.split("|")[1]
                    self.ui.lineEdit_4.setText(str(val))
                    
                if ln.startswith("longitude|"):
                    val = ln.split("|")[1]
                    self.ui.lineEdit_5.setText(str(val))
                    
                if ln.startswith("latitude|"):
                    val = ln.split("|")[1]
                    self.ui.lineEdit_6.setText(str(val))
                    
                if ln.startswith("altitude|"):
                    val = ln.split("|")[1]
                    self.ui.lineEdit_7.setText(str(val))
                    
                if ln.startswith("timezone|"):
                    val = ln.split("|")[1]
                    self.ui.lineEdit_8.setText(str(val))
                    
                if ln.startswith("#"):
                    comm = "{}\n{}".format(comm, ln.replace("#", ""))
                    
            
            self.ui.plainTextEdit.setPlainText(
                    QtWidgets.QApplication.translate(
                            "Form", "\n".join(comm.split('\n')[1:]), None))
                    
        else:
            self.etc.log("No such Observatory({})".format(obs_name))
        
        #Reload log file to log view
        self.reload_log()
    
    def rm_obs(self):
        if self.ui.listWidget_12.currentItem() is not None:
            obs_name = self.ui.listWidget_12.currentItem().text()
            obs_path = self.fop.abs_path("{}/{}".format(
                    self.etc.observat_dir, obs_name))
            if self.fop.is_file(obs_path):
                self.fop.rm(obs_path)
            else:
                #Log and display an error about about not existing
                #observatory name
                self.etc.log("No such Observatory({})".format(obs_name))
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Couldn't find the observatory"))
        else:
            #Log and display an error about about not existing observatory name
                self.etc.log("No Observatory was choosen")
                QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                               ("No Observatory was choosen"))
        self.load_observat()
        #Reload log file to log view
        self.reload_log()
    
    def add_obs(self):
        if not self.ui.lineEdit_3.text() == "":
            observatory = self.ui.lineEdit_3.text()
            name = self.ui.lineEdit_4.text()
            longitude = self.ui.lineEdit_5.text()
            latitude = self.ui.lineEdit_6.text()
            altitude = self.ui.lineEdit_7.text()
            timezone = self.ui.lineEdit_8.text()
            comm = str(self.ui.plainTextEdit.toPlainText())
            
            file_name = self.fop.abs_path("{}/{}".format(
                    self.etc.observat_dir, observatory))
            f = open(file_name, "w")
            f.write("#{}\n".format(comm.replace("\n", "\n#")))
            f.write("observatory|{}\n".format(observatory))
            f.write("name|{}\n".format(name))
            f.write("longitude|{}\n".format(longitude))
            f.write("latitude|{}\n".format(latitude))
            f.write("altitude|{}\n".format(altitude))
            f.write("timezone|{}\n".format(timezone))
            f.close()
            
            self.ui.lineEdit_3.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_6.setText("")
            self.ui.lineEdit_7.setText("")
            self.ui.lineEdit_8.setText("")
            self.ui.plainTextEdit.setPlainText("")
            
            self.load_observat()
        else:
            #Log and display an error about empty observatory name
            self.etc.log("No observatory was specified.")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("No observatory was specified"))
            
        #Reload log file to log view
        self.reload_log()
        
    def reload_log(self):
        #Remove all log lines in listwidget
        g.rm_all(self, self.ui.listWidget_10)
        #Add log file's contents to listwidget
        g.add_line_by_line(self, self.ui.listWidget_10, self.etc.mini_log_file)
        #Scroll all the way down
        self.ui.listWidget_10.scrollToBottom()
        #print("reload")
        
    def save_log(self):
        #Ask for user for save file path
        out_file = g.save_log_file(self)
        #Check if path was selected
        if out_file:
            #Copy the log file to wanted path
            self.fop.cp(self.etc.mini_log_file, out_file)
            
        self.reload_log()
        
    def clear_log(self):
        #Ask for ARE YOU SURE
        answ = g.question(self, "Are you sure you want to clear log?")
        #Check if the answer is YES
        if answ == QtWidgets.QMessageBox.Yes:
            #Copy the log file somewhere safe
            self.fop.cp(self.etc.log_file, "{}_{}".format(self.etc.log_file,
                        self.etc.time_stamp_()))
            #Copy the mini log file somewhere safe
            self.fop.cp(self.etc.mini_log_file, "{}_{}".format(
                    self.etc.mini_log_file, self.etc.time_stamp_()))
            #Dump all log files
            self.etc.dump_log()
            self.etc.dump_mlog()
        self.reload_log()
        
    def save_settings(self):
        calib_zero_comb = self.ui.comboBox_2.currentIndex()
        calib_zero_reje = self.ui.comboBox_3.currentIndex()
        
        calib_dark_comb = self.ui.comboBox_4.currentIndex()
        calib_dark_reje = self.ui.comboBox_5.currentIndex()
        calib_dark_scal = self.ui.comboBox_8.currentIndex()
        
        calib_flat_comb = self.ui.comboBox_6.currentIndex()
        calib_flat_reje = self.ui.comboBox_7.currentIndex()
        calib_flat_subs = self.ui.comboBox_9.currentIndex()
        
        photo_stan =  g.is_checked_t(self, self.ui.groupBox_6)
        photo_stan_noma =  g.is_checked_t(self, self.ui.checkBox_13)
        photo_stan_usno =  g.is_checked_t(self, self.ui.checkBox_14)
        photo_stan_gaia =  g.is_checked_t(self, self.ui.checkBox_15)
        photo_stan_radi = self.ui.doubleSpinBox.value()
        
        photo_phpa_aper = self.ui.doubleSpinBox_5.value()
        photo_phpa_zmag = self.ui.doubleSpinBox_8.value()
        photo_phpa_gain = self.ui.lineEdit_26.text()
        
        photo_dapa_expt = self.ui.lineEdit_13.text()
        photo_dapa_filt = self.ui.lineEdit_14.text()
        
        photo_head_extr = ""
        
        header_list = g.list_of_list(self, self.ui.listWidget_20)
        for header in header_list:
            photo_head_extr = "{},{}".format(header, photo_head_extr)
        
        photo_head_extr = photo_head_extr[:-1]
        
        coscl_gain = self.ui.doubleSpinBox_20.value()
        coscl_reno = self.ui.doubleSpinBox_21.value()
        coscl_sicl = self.ui.doubleSpinBox_22.value()
        coscl_sifr = self.ui.doubleSpinBox_23.value()
        coscl_obli = self.ui.doubleSpinBox_24.value()
        coscl_mait = self.ui.spinBox_2.value()
        coscl_sama =  g.is_checked_t(self, self.ui.checkBox_3)
        
        asmet_goon = g.is_checked_t(self, self.ui.groupBox_5)
        asmet_goon_serv = self.ui.lineEdit_27.text()
        asmet_goon_apke = self.ui.lineEdit_28.text()
        asmet_goon_cobe = g.is_checked_t(self, self.ui.checkBox_2)
        
        f_set = open(self.etc.setting_file, "w")
        f_set.write("calib_zero_comb->{}\n".format(calib_zero_comb))
        f_set.write("calib_zero_reje->{}\n".format(calib_zero_reje))
        
        f_set.write("calib_dark_comb->{}\n".format(calib_dark_comb))
        f_set.write("calib_dark_reje->{}\n".format(calib_dark_reje))
        f_set.write("calib_dark_scal->{}\n".format(calib_dark_scal))
        
        f_set.write("calib_flat_comb->{}\n".format(calib_flat_comb))
        f_set.write("calib_flat_reje->{}\n".format(calib_flat_reje))
        f_set.write("calib_flat_subs->{}\n".format(calib_flat_subs))
        
        
        f_set.write("photo_stan_main->{}\n".format(photo_stan))
        f_set.write("photo_stan_noma->{}\n".format(photo_stan_noma))
        f_set.write("photo_stan_usno->{}\n".format(photo_stan_usno))
        f_set.write("photo_stan_gaia->{}\n".format(photo_stan_gaia))
        f_set.write("photo_stan_radi->{}\n".format(photo_stan_radi))
        
        f_set.write("photo_phpa_aper->{}\n".format(photo_phpa_aper))
        f_set.write("photo_phpa_zmag->{}\n".format(photo_phpa_zmag))
        f_set.write("photo_phpa_gain->{}\n".format(photo_phpa_gain))
        
        f_set.write("photo_dapa_expt->{}\n".format(photo_dapa_expt))
        f_set.write("photo_dapa_filt->{}\n".format(photo_dapa_filt))
        
        f_set.write("photo_head_extr->{}\n".format(photo_head_extr))
        
        f_set.write("coscl_gain->{}\n".format(coscl_gain))
        f_set.write("coscl_reno->{}\n".format(coscl_reno))
        f_set.write("coscl_sicl->{}\n".format(coscl_sicl))
        f_set.write("coscl_sifr->{}\n".format(coscl_sifr))
        f_set.write("coscl_obli->{}\n".format(coscl_obli))
        f_set.write("coscl_mait->{}\n".format(coscl_mait))
        f_set.write("coscl_sama->{}\n".format(coscl_sama))
        
        f_set.write("asmet_goon_main->{}\n".format(asmet_goon))
        f_set.write("asmet_goon_serv->{}\n".format(asmet_goon_serv))
        f_set.write("asmet_goon_apke->{}\n".format(asmet_goon_apke))
        f_set.write("asmet_goon_cobe->{}\n".format(asmet_goon_cobe))
        
        f_set.close()
        
    def load_setting(self):
        if self.fop.is_file(self.etc.setting_file):
            f_set = open(self.etc.setting_file, "r")
            for ln in f_set:
                line = ln.replace("\n", "")
                try:
                    if line.startswith("calib_zero_comb"):
                        self.ui.comboBox_2.setCurrentIndex(
                                int(line.split("->")[1]))
                    if line.startswith("calib_zero_reje"):
                        self.ui.comboBox_3.setCurrentIndex(
                                int(line.split("->")[1]))
                
                    
                    if line.startswith("calib_dark_comb"):
                        self.ui.comboBox_4.setCurrentIndex(
                                int(line.split("->")[1]))
                    if line.startswith("calib_dark_reje"):
                        self.ui.comboBox_5.setCurrentIndex(
                                int(line.split("->")[1]))
                    if line.startswith("calib_dark_scal"):
                        self.ui.comboBox_8.setCurrentIndex(
                                int(line.split("->")[1]))
                        
                        
                    if line.startswith("calib_flat_comb"):
                        self.ui.comboBox_6.setCurrentIndex(
                                int(line.split("->")[1]))
                    if line.startswith("calib_flat_reje"):
                        self.ui.comboBox_7.setCurrentIndex(
                                int(line.split("->")[1]))
                    if line.startswith("calib_flat_subs"):
                        self.ui.comboBox_9.setCurrentIndex(
                                int(line.split("->")[1]))
                        
                    if line.startswith("photo_stan_main"):
                        if line.split("->")[1] == "YES":
                            self.ui.groupBox_6.setChecked(True)
                        else:
                            self.ui.groupBox_6.setChecked(False)
                    if line.startswith("photo_stan_noma"):
                        if line.split("->")[1] == "YES":
                            self.ui.checkBox_13.setChecked(True)
                        else:
                            self.ui.checkBox_13.setChecked(False)
                    if line.startswith("photo_stan_usno"):
                        if line.split("->")[1] == "YES":
                            self.ui.checkBox_14.setChecked(True)
                        else:
                            self.ui.checkBox_14.setChecked(False)
                    if line.startswith("photo_stan_gaia"):
                        if line.split("->")[1] == "YES":
                            self.ui.checkBox_15.setChecked(True)
                        else:
                            self.ui.checkBox_15.setChecked(False)
                    if line.startswith("photo_stan_radi"):
                        self.ui.doubleSpinBox.setValue(
                                float(line.split("->")[1]))
                        
                    if line.startswith("photo_phpa_aper"):
                        self.ui.doubleSpinBox_5.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("photo_phpa_zmag"):
                        self.ui.doubleSpinBox_8.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("photo_phpa_gain"):
                        self.ui.lineEdit_26.setText(str(line.split("->")[1]))
                        
                    if line.startswith("photo_dapa_expt"):
                        self.ui.lineEdit_13.setText(str(line.split("->")[1]))
                    if line.startswith("photo_dapa_filt"):
                        self.ui.lineEdit_14.setText(str(line.split("->")[1]))
                        
                    if line.startswith("photo_head_extr"):
                        headers = str(line.split("->")[1]).split(",")
                        g.replace_list_con(self, self.ui.listWidget_20, headers)
                        
                    if line.startswith("coscl_gain"):
                        self.ui.doubleSpinBox_20.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("coscl_reno"):
                        self.ui.doubleSpinBox_21.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("coscl_sicl"):
                        self.ui.doubleSpinBox_22.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("coscl_sifr"):
                        self.ui.doubleSpinBox_23.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("coscl_obli"):
                        self.ui.doubleSpinBox_24.setValue(
                                float(line.split("->")[1]))
                    if line.startswith("coscl_mait"):
                        self.ui.spinBox_2.setValue(int(line.split("->")[1]))
                    if line.startswith("coscl_sama"):
                        if line.split("->")[1] == "YES":
                            self.ui.checkBox_3.setChecked(True)
                        else:
                            self.ui.checkBox_3.setChecked(False)
                            
                    if line.startswith("asmet_goon_main"):
                        if line.split("->")[1] == "YES":
                            self.ui.groupBox_5.setChecked(True)
                        else:
                            self.ui.groupBox_5.setChecked(False)
                    if line.startswith("asmet_goon_serv"):
                        self.ui.lineEdit_27.setText(str(line.split("->")[1]))
                    if line.startswith("asmet_goon_apke"):
                        self.ui.lineEdit_28.setText(str(line.split("->")[1]))
                    if line.startswith("asmet_goon_cobe"):
                        if line.split("->")[1] == "YES":
                            self.ui.checkBox_2.setChecked(True)
                        else:
                            self.ui.checkBox_2.setChecked(False)
                    
                except Exception as e:
                    self.etc.log(
                            "{}. Load Settings. Using defalut settings".format(
                                    e))
                    self.load_setting(default=True)
            f_set.close()
        else:
            self.etc.log(
                    "settings file is not available. Using defalut settings")
        
        
    def first_thing_first(self):
        #Things to do first
        self.etc.log("Do first things")
        #Prevent the user to do auto align for now
#        self.ui.checkBox.setEnabled(False)
#        self.ui.checkBox.setChecked(False)
        self.ui.tabWidget_6.setTabEnabled(1, False)
        self.ui.tabWidget_3.setTabEnabled(3, False)
        self.ui.tabWidget_4.setTabEnabled(3, False)
        
        self.load_setting()
        
    def empty_display(self, dev):
        if dev.upper() == "PHOT":
            self.phot_disp = FitsPlot(self.ui.disp_photometry.canvas,
                                      verb=self.verb)
        elif dev.upper() == "ALIGN":
            self.align_disp = FitsPlot(self.ui.disp_align.canvas,
                                       verb=self.verb)
        elif dev.upper() == "ATRACK":
            self.atrack_disp = FitsPlot(self.ui.disp_atrack.canvas,
                                        verb=self.verb)
        elif dev.upper() == "COSMIC":
            self.cocmicC_disp = FitsPlot(self.ui.disp_cosmicC.canvas,
                                         verb=self.verb)
            
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    if len(argv) < 2:
        v = False
    else:
        if "verbose".startswith(argv[1].lower()):
            v = True
        else:
            v = False
        
    v = True
    widnow = MyForm(verb=v)
    widnow.show()
    sexit(app.exec_())