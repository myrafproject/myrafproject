# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:15:11 2019

@author: msh, yk
"""
try:
    from sys import argv
except Exception as e:
    print("{}: Can't import sys?".format(e))
    exit(0)

try:
    import argparse
except Exception as e:
    print("{}: Can't import argparse.".format(e))
    exit(0)

try:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
except Exception as e:
    print("{}: Can't import PyQt5.".format(e))
    exit(0)

try:
    from gui import albategnius
    from gui import myraf
    from gui import display
    from gui import animate
    from gui import photometry
    from gui import observatory
    from gui import header_editor
    from gui import header_calculator
    from gui import header_extractor
    from gui import help_analyse
    from gui import help_editor
    from gui import help_licence
    from gui import help_credits
    from gui import help_logger
    from gui import help_aboutmyraf
    from gui import help_help_ginga
    from gui import help_help_alipy
    from gui import help_help_ccleaner
    from gui import help_help_astrometrynet
    from gui import combine_subtraction
    from gui import setting_calibration
    from gui import setting_photometry
    from gui import setting_cosmiccleaner
    from gui import setting_astrometrynet
    from gui import myraf_progress
    from gui import func
    from gui import align_manual
except Exception as e:
    print("{}: Can't import GUIs. MYRaf is not installed properly.".format(e))
    exit(0)

try:
    from fPlot import FitsPlot
except Exception as e:
    print("{}: Can't import fPlot. MYRaf is not installed properly.".format(e))
    exit(0)

try:
    from matplotlib.patches import Circle
except Exception as e:
    print("{}: Can't import matplotlib.".format(e))
    exit(0)

try:
    from myraflib import analyse
    from myraflib import env
except Exception as e:
    print("{}: Can't import myraflib. MYRaf is not installed properly.".format(
            e))
    exit(0)

class MainWindow(QtWidgets.QMainWindow, myraf.Ui_MainWindow):
    def __init__(self, parent=None, verb=False, debugger=False):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.flags = QtCore.Qt.Window
        self.setWindowFlags(self.flags)
        
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        
        self.logger.log("Starting MYRaf")
        self.photometry_window = None
        self.observatory_window = None
        self.heditor_window = None
        self.hcalc_window = None
        self.hex_window = None
        self.display_window = []
        self.licence_window = None
        self.credits_window = None
        self.logger_window = None
        self.abuot_window = None
        self.ginga_window = None
        self.alipy_window = None
        self.ccleaner_window = None
        self.astrometry_window = None
        self.subtraction_window = None
        self.scalibration_window = None
        self.sphotometry_window = None
        self.sccleaner_window = None
        self.analyse_window = None
        self.editor_window = None
        self.proc_window = None
        self.animate_window = None
        self.alignmanual_window = None
        self.sastrometry_window = None
        self.albategnius_window = None
        
        self.logger.log("Creating objects")
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.ira = analyse.Astronomy.Iraf(verb=self.verb,
                                          debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.fnk_file = func.Files(self, self.logger)
        self.fnk_deve = func.Devices(self, self.logger)
        
        self.logger.log("Cleaninng TEMP Directory")
        self.fop.temp_cleaner()
        
        self.logger.log("Setting GUI")
        self.progress.setProperty("value", 0)
        
        self.logger.log("Creating Triggers")
        
        self.logger.log("Creating Menu Triggers")
        self.actionAddImage.triggered.connect(lambda: (self.add_data("image")))
        self.image_add.clicked.connect(lambda: (self.add_data("image")))
        self.image_remove.clicked.connect(lambda: (self.rm_data("image")))
        self.actionAddBias.triggered.connect(lambda: (self.add_data("bias")))
        self.bias_add.clicked.connect(lambda: (self.add_data("bias")))
        self.bias_remove.clicked.connect(lambda: (self.rm_data("bias")))
        self.actionAddDark.triggered.connect(lambda: (self.add_data("dark")))
        self.dark_add.clicked.connect(lambda: (self.add_data("dark")))
        self.dark_remove.clicked.connect(lambda: (self.rm_data("dark")))
        self.actionAddFlat.triggered.connect(lambda: (self.add_data("flat")))
        self.flat_add.clicked.connect(lambda: (self.add_data("flat")))
        self.flat_remove.clicked.connect(lambda: (self.rm_data("flat")))
        self.actionQuit.triggered.connect(lambda: (self.exit()))
        self.actionAbout_MYRaf.triggered.connect(lambda: (
                self.open_window("about")))
        self.actionLA_Cosmic_Cleaner_2.triggered.connect(lambda: (
                self.open_window("ccleaner")))
        self.actionAstrometry_net_2.triggered.connect(lambda: (
                self.open_window("astrometry")))
        self.actionAlipy_2.triggered.connect(lambda: (
                self.open_window("alipy")))
        
        self.actionAlbatenius.triggered.connect(lambda: (
                self.open_window("albategnius")))
        
        
        
        self.actionGinga_2.triggered.connect(lambda: (
                self.open_window("ginga")))
        self.actionLog_Viewer.triggered.connect(lambda: (
                self.open_window("logger")))
        self.actionLicense.triggered.connect(lambda: (
                self.open_window("licence")))
        self.actionCredits.triggered.connect(lambda: (
                self.open_window("credits")))
        self.actionPhotometry.triggered.connect(lambda: (
                self.open_window("photometry")))
        self.actionObservatory.triggered.connect(lambda: (
                self.open_window("observatory")))
        self.actionHedit.triggered.connect(lambda: (
                self.open_window("heditor")))
        self.actionHeader_Calculator.triggered.connect(lambda: (
                self.open_window("hcalc")))
        self.actionHeader_Extractor.triggered.connect(lambda: (
                self.open_window("hex")))
        self.actionCalibration_2.triggered.connect(lambda: (
                self.open_window("scalibration")))
        self.actionPhotometry_2.triggered.connect(lambda: (
                self.open_window("sphotometry")))
        self.actionCosmic_Cleaner.triggered.connect(lambda: (
                self.open_window("sccleaner")))
        
        self.actionWCS_2.triggered.connect(lambda: (
                self.open_window("swcs")))
        
        self.actionAnalyse_2.triggered.connect(lambda: (
                self.open_window("analyse")))
        self.actionEditor.triggered.connect(lambda: (
                self.open_window("editor")))
        self.actionCalibration.triggered.connect(lambda: (
                self.calibration()))
        self.actionAutoAlign.triggered.connect(lambda: (
                self.align(auto=True)))
        self.actionManualAlign.triggered.connect(lambda: (
                self.align(auto=False)))
        self.actionZerocombine.triggered.connect(lambda: (
                self.zero_combine(file_requested=False)))
        self.actionDarkcombine.triggered.connect(lambda: (
                self.dark_combine(file_requested=False)))
        self.actionFlatcombine.triggered.connect(lambda: (
                self.flat_combine(file_requested=False)))
        self.actionCosmic.triggered.connect(lambda: (self.cclean()))
        self.actionWCS.triggered.connect(lambda: (self.solve()))
        
        self.actionA_Track.triggered.connect(lambda: (
                QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                               ("Not ready yet"))))        
        
        
        self.actionClose_All_Windows.triggered.connect(lambda: (
                self.close_all()))
        self.actionClear_All_Lists.triggered.connect(lambda: (
                self.clear_list("all")))
        self.actionClear_Image_List_3.triggered.connect(lambda: (
                self.clear_list("image")))
        self.actionClear_Bias_List_3.triggered.connect(lambda: (
                self.clear_list("bias")))
        self.actionClear_Dark_List_3.triggered.connect(lambda: (
                self.clear_list("dark")))
        self.actionClear_Flat_List_3.triggered.connect(lambda: (
                self.clear_list("flat")))
        
        
        self.actionMedian.triggered.connect(lambda: (
                self.combine_images("median")))
        self.actionAverage.triggered.connect(lambda: (
                self.combine_images("average")))
        self.actionSum.triggered.connect(lambda: (
                self.combine_images("sum")))
        self.actionDifference.triggered.connect(lambda: (
                self.combine_images("diff")))
        
        
        self.logger.log("Creating Right Click Menu")
        self.image_list.clicked.connect(lambda: (
                self.list_clicked(self.image_list)))
        self.bias_list.clicked.connect(lambda: (
                self.list_clicked(self.bias_list)))
        self.dark_list.clicked.connect(lambda: (
                self.list_clicked(self.dark_list)))
        self.flat_list.clicked.connect(lambda: (
                self.list_clicked(self.flat_list)))
        
        self.logger.log("Creating Right Click Menu")
        self.image_list.installEventFilter(self)
        self.bias_list.installEventFilter(self)
        self.dark_list.installEventFilter(self)
        self.flat_list.installEventFilter(self)
        self.play_ground.installEventFilter(self)
        
    def get_ast_set(self):
        settings = self.fop.read_set("ast")
        return(settings)
        
    def solve(self):
        files = self.fnk_deve.get_from_tree(self.image_list)
        if len(files) > 0:
            the_set = self.get_ast_set()
            out_dir = self.fnk_file.save_directory()
            if out_dir is not None and not out_dir == "":
                self.open_window("proc")
                for it, file in enumerate(files):
                    self.proc_window.progress_annotation.setProperty(
                            "text", "Scolving: {}".format(file))
                    pn, fn = self.fop.get_base_name(file)
                    out_file = "{}/{}".format(out_dir, fn)
                    if the_set["online"]:
                        self.fts.astrometry(file, out_file,
                                            server=the_set["server"],
                                            apikey=the_set["apike"])
                    else:
                        self.fts.solve_field(file, out_file)
                    self.proc_window.progress_progressBar.setProperty(
                            "value", 100 *(it + 1) / (len(files)))
                    
                for wind in self.play_ground.subWindowList():
                    if wind.windowTitle() == "MYRaf Progress":
                        wind.close()
        else:
            self.logger.log("No Image to Solve")
            QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                           ("No Image to Solve"))
    
    def get_cos_set(self):
        settings = self.fop.read_set("cos")
        return(settings)
    
    def cclean(self):
        files = self.fnk_deve.get_from_tree(self.image_list)
        if len(files) > 0:
            out_dir = self.fnk_file.save_directory()
            if out_dir is not None and not out_dir == "":
                the_set = self.get_cos_set()
                    
                self.open_window("proc")
                for it, file in enumerate(files):
                    self.proc_window.progress_annotation.setProperty(
                            "text", "Cleaning: {}".format(file))
                    pn, fn = self.fop.get_base_name(file)
                    out_file = "{}/{}".format(out_dir, fn)
                    self.fts.cosmic_cleaner(file, out_file,
                                            gain=the_set["gain"],
                                            readout_noise=the_set["reno"],
                                            sigma_clip=the_set["sicl"],
                                            sigma_fraction=the_set["sifr"],
                                            object_limit=the_set["obli"],
                                            max_iter=the_set["mait"],
                                            mask=the_set["crma"])
                    self.proc_window.progress_progressBar.setProperty(
                            "value", 100 *(it + 1) / (len(files)))
                    
                for wind in self.play_ground.subWindowList():
                    if wind.windowTitle() == "MYRaf Progress":
                        wind.close()
        else:
            self.logger.log("No Image to Clean")
            QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                           ("No Image to Clean"))
        
    def align(self, auto=True):
        files = self.fnk_deve.get_from_tree(self.image_list)
        if len(files) > 0:
            if auto:
                self.logger.log("Auto Align Detected")
                if self.image_list.currentItem() is not None:
                    
                    ref = self.image_list.currentItem().text(0)
                    out_dir = self.fnk_file.save_directory()
                    if out_dir is not None and not out_dir == "":
                        self.open_window("proc")
                        for it, file in enumerate(files):
                            self.proc_window.progress_annotation.setProperty(
                                    "text", "Aligning: {}".format(file))
                            self.fts.align(file, ref, out_dir)
                            self.proc_window.progress_progressBar.setProperty(
                                    "value", 100 *(it + 1) / (len(files)))
                            
                        for wind in self.play_ground.subWindowList():
                            if wind.windowTitle() == "MYRaf Progress":
                                wind.close()
                                
                else:
                    self.logger.log("No Reference Image")
                    QtWidgets.QMessageBox.critical(
                            self, ("MYRaf Error"),
                            ("please select a Reference Image"))
            else:
                self.logger.log("Manual Align Detected")
                self.open_window("alignmanual")
        else:
            self.logger.log("No Image to Align")
            QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                           ("No Image to Align"))
            
    def get_cal_set(self):
        settings = self.fop.read_set("cal")
        
        if settings['b_combine'] == 0:
            settings['b_combine'] = "median"
        elif settings['b_combine'] == 1:
            settings['b_combine'] = "average"
            
        if settings['b_rejection'] == 0:
            settings['b_rejection'] = "none"
        elif settings['b_rejection'] == 1:
            settings['b_rejection'] = "minmax"
            
        if settings['d_combine'] == 0:
            settings['d_combine'] = "median"
        elif settings['d_combine'] == 1:
            settings['d_combine'] = "average"
            
        if settings['d_rejection'] == 0:
            settings['d_rejection'] = "none"
        elif settings['d_rejection'] == 1:
            settings['d_rejection'] = "minmax"
            
        if settings['d_scale'] == 0:
            settings['d_scale'] = "none"
        elif settings['d_scale'] == 1:
            settings['d_scale'] = "exposure"
            
        if settings['f_combine'] == 0:
            settings['f_combine'] = "median"
        elif settings['f_combine'] == 1:
            settings['f_combine'] = "average"
            
        if settings['f_rejection'] == 0:
            settings['f_rejection'] = "none"
        elif settings['f_rejection'] == 1:
            settings['f_rejection'] = "minmax"
            
        return(settings)
            
    def zero_combine(self, file_requested=False):
        files = self.fnk_deve.get_from_tree(self.bias_list)
        if len(files) > 0:
            try:
                the_set = self.get_cal_set()
                
                out_file = "{}/myraf_zerocombine_{}.fits".format(
                        self.logger.tmp_dir, self.logger.random_string(10))
                
                zro = self.ira.zerocombine(files, out_file,
                                           method=the_set["b_combine"],
                                           rejection=the_set["b_rejection"])
                if zro:
                    if file_requested:
                        return(out_file)
                    else:
                        self.open_window("display", [out_file, True])
            except Exception as e:
                self.logger.log(e)
        else:
            self.logger.log("No File to do Zerocombine")
            if not file_requested:
                QtWidgets.QMessageBox.critical(self, ("MYRaf Error"), 
                                               ("No File to do Zerocombine"))
                
            
    def dark_combine(self, file_requested=False, sub_calib=True):
        files = self.fnk_deve.get_from_tree(self.dark_list)
        if len(files) > 0:
            try:
                the_set = self.get_cal_set()
                
                out_file = "{}/myraf_darkcombine_{}.fits".format(
                                self.logger.tmp_dir,
                                self.logger.random_string(10))
                
                zero = None
                
                if len(self.fnk_deve.get_from_tree(self.bias_list)) > 0 and sub_calib:
                    msg1 = "Bias Files Detected."
                    msg2 = "Do you want to apply zero correction to master dark?"
                    msg3 = "Be aware. Bias files will be effected."
                    ans = self.fnk_deve.ask_calcel("{}\n{}\n{}".format(msg1,
                                                   msg2, msg3))
                    if ans=="yes":
                        zero = self.zero_combine(file_requested=True)
                    elif ans=="no":
                        zero = None
                    elif ans == "cancel":
                        return(None)
                else:
                    zero = None
                    
                drk = self.ira.darkcombine(files, out_file, zero=zero,
                                           method=the_set["d_combine"],
                                           rejection=the_set["d_rejection"],
                                           scale=the_set["d_scale"])
                
                if drk:
                    if file_requested:
                        return(out_file, zero)
                    else:
                        self.open_window("display", [out_file, True])
            except Exception as e:
                self.logger.log(e)
            
        else:
            self.logger.log("No File to do Darkcombine")
            if not file_requested:
                QtWidgets.QMessageBox.critical(self, ("MYRaf Error"), 
                                               ("No File to do Darkcombine"))
            
    def flat_combine(self, file_requested=False, sub_calib=True):
        files = self.fnk_deve.get_from_tree(self.flat_list)
        if len(files) > 0:
            try:
                the_set = self.get_cal_set()
                
                bias_count = len(self.fnk_deve.get_from_tree(self.bias_list))
                dark_count = len(self.fnk_deve.get_from_tree(self.dark_list))
                out_file = "{}/myraf_flatcombine_{}.fits".format(
                                self.logger.tmp_dir,
                                self.logger.random_string(10))
                
                
                dark = [None, None]
                zero = None
                
                if dark_count > 0 and sub_calib:
                    msg1 = "Dark Files Detected."
                    msg2 = "There can be zero and dark corrections"
                    msg3 = "Do you want to apply corrections to master flat?"
                    msg4 = "Be aware. Bias/Dark files will be effected."
                    ans = self.fnk_deve.ask_calcel("{} {}\n{}\n{}".format(msg1,
                                                   msg2, msg3, msg4))
                    if ans=="yes":
                        dark = self.dark_combine(file_requested=True)
                    elif ans=="no":
                        dark = [None, None]
                    elif ans == "cancel":
                        return(None)
                        
                elif bias_count > 0 and sub_calib:
                    msg1 = "Bias Files Detected."
                    msg2 = "Do you want to apply zero correction to master flat?"
                    msg3 = "Be aware. Bias files will be effected."
                    ans = self.fnk_deve.ask_calcel("{}\n{}\n{}".format(msg1,
                                                   msg2, msg3))
                    
                    if ans=="yes":
                        zero = self.zero_combine(file_requested=True)
                    elif ans=="no":
                        zero = None
                    elif ans == "cancel":
                        return(None)
                        
                        
                if not dark == [None, None]:
                    d_use = dark[0]
                    z_use = dark[1]
                elif zero is not None:
                    d_use = None
                    z_use = zero
                else:
                    d_use = None
                    z_use = None
                    
                    
                flt = self.ira.flatcombine(files, out_file, dark=d_use,
                                           zero=z_use,
                                           method=the_set['f_combine'],
                                           rejection=the_set['f_rejection'])
                if flt:
                    if file_requested:
                        return(out_file, d_use, z_use)
                    else:
                        self.open_window("display", [out_file, True])
            except Exception as e:
                self.logger.log(e)
        else:
            self.logger.log("No File to do Flatcombine")
            if not file_requested:
                QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                               ("No File to do Flatcombine"))
            
            
    def calibration(self):
        files = self.fnk_deve.get_from_tree(self.image_list)
        
        if len(files) > 0:
            zero = self.zero_combine(file_requested=True)
            dark = self.dark_combine(file_requested=True, sub_calib=False)
            flat = self.flat_combine(file_requested=True, sub_calib=False)
            if zero is not None or dark is not None or flat is not None:
                if zero is not None:
                    self.logger.log("Zero Correction Detected")
                if dark is not None:
                    self.logger.log("Dark Correction Detected")
                    dark = dark[0]
                if flat is not None:
                    self.logger.log("Flat Correction Detected")
                    flat = flat[0]
                self.open_window("proc")
                
                out_dir = self.fnk_file.save_directory()
                if out_dir is not None and not out_dir == "":
                    for it, file in enumerate(files):
                        self.proc_window.progress_annotation.setProperty(
                                "text", "Calibrating: {}".format(file))
                        path, file_name = self.fop.get_base_name(file)
                        out_file = "{}/{}".format(out_dir, file_name)
                        if self.fop.is_file(out_file):
                            self.fop.rm(out_file)
                        if self.ira.ccdproc(file, out_file, zero, dark, flat):
                            self.fts.update_header(file, "MYCORR","calibration done @ {} using MYRaf V3 Beta".format(self.logger.time_stamp()))
                            
                        proc = 100 *(it + 1) / (len(files))
                        self.proc_window.progress_progressBar.setProperty(
                                "value", proc)
                        
                for wind in self.play_ground.subWindowList():
                    if wind.windowTitle() == "MYRaf Progress":
                        wind.close()
            else:
                self.logger.log("Nothing was given for calibration")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"),
                        ("Nothing was given for calibration"))
        else:
            self.logger.log("No Image to Calibrate")
            QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                           ("No Image to Calibrate"))
        
        
        

    def reload_log(self):
        if self.logger_window is not None:
            self.logger_window.load()

    def clear_list(self, device):
        self.logger.log("Cleaning List {}".format(device))
        if device == "all":
            self.image_list.clear()
            self.bias_list.clear()
            self.dark_list.clear()
            self.flat_list.clear()
        elif device == "image":
            self.image_list.clear()
        elif device == "bias":
            self.bias_list.clear()
        elif device == "dark":
            self.dark_list.clear()
        elif device == "flat":
            self.flat_list.clear()
        
        self.reload_log()
        
    def close_all(self):
        self.logger.log("Closeing All Open Windows")
        for the_window in self.play_ground.subWindowList():
            self.logger.log("Closing {}".format(the_window))
            the_window.close()
            
        self.reload_log()
        
    def list_clicked(self, device):
        if device.currentItem() is not None:
            self.logger.log("File List Clicked")
            path = device.currentItem().text(0)
            self.logger.log("Checking file Path")
            if self.fts.check(path):
                if self.heditor_window is not None:
                    self.logger.log("Header Editor Window is Open")
                    self.logger.log("Get All Headers for file {}".format(path))
                    headers = self.fts.header(path)
                    fill_list = []
                    if headers is not None:
                        for header in headers:
                            fill_list.append("{}->{}".format(header[0],
                                             header[1]))
                    
                    self.heditor_window.fill_header_list(fill_list)
                
                if self.hex_window is not None:
                    self.logger.log("Header Extractor Window is Open")
                    self.logger.log("Get All Headers for file {}".format(path))
                    headers = self.fts.header(path)
                    fill_list = []
                    if headers is not None:
                        for header in headers:
                            fill_list.append("{}->{}".format(header[0],
                                             header[1]))
                            
                    self.hex_window.fill_header_list(fill_list)
                    
                if self.hcalc_window is not None:
                    self.logger.log("Header Calculator Window is Open")
                    self.logger.log("Get All Headers for file {}".format(path))
                    headers = self.fts.header(path)
                    fill_list = []
                    if headers is not None:
                        for header in headers:
                            fill_list.append("{}->{}".format(header[0],
                                             header[1]))
                    self.hcalc_window.fill_header_list(fill_list)
                    
                if self.photometry_window is not None:
                    self.logger.log("Photometry Window is Open")
                    if device == self.image_list:
                        self.photometry_window.show_me(path)
                        
                if not self.display_window == []:
                    self.logger.log("Display Window is Open")
                    if not self.display_window == []:
                        self.display(device, False)
                        
                if self.alignmanual_window is not None:
                    if device == self.image_list:
                        self.alignmanual_window.show_me(path)
        
        self.reload_log()
        
    def combine_images(self, combine_method):
        self.logger.log("Image Combine")
        all_files = None
        if self.file_containter.currentIndex() == 0:
            self.logger.log("Combine from Image List")
            device = self.image_list
        elif self.file_containter.currentIndex() == 1:
            self.logger.log("Combine from Bias List")
            device = self.bias_list
        elif self.file_containter.currentIndex() == 2:
            self.logger.log("Combine from Dark List")
            device = self.dark_list
        elif self.file_containter.currentIndex() == 3:
            self.logger.log("Combine from Flat List")
            device = self.flat_list
        
        all_files = self.fnk_deve.get_from_tree(device, selected=False)
        
        
        if not (all_files is None or all_files == []):
            if combine_method == "diff":
                self.logger.log("Subtraction detected")
                self.open_window("subtract", all_files)
            else:
                data = self.fts.combine(all_files,
                                        combine_method=combine_method)
                if data is not None:
                    the_file = "{}/myraf_{}_{}.fits".format(
                            self.logger.tmp_dir, combine_method,
                            self.logger.random_string(10))
                    self.fts.write(the_file, data)
                    self.open_window("display", [the_file, True])
        else:
            self.logger.log("No file to combine")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("Please add some files"))
        
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.image_list):
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_data("image")))
            menu.addAction('Remove', lambda: (self.rm_data("image")))
            menu.addSeparator()
            menu.addAction('Animate', lambda: (self.animate(self.image_list)))
            menu.addAction('Display..', lambda: (self.display(
                    self.image_list, False)))
            menu.addAction('Display in New Window...', lambda: (
                    self.display(self.image_list, True)))
            menu.exec_(event.globalPos())
            return(True)
            
#        elif (event.type() == QtCore.QEvent.ContextMenu and source is self.play_ground):
#            print(source)
#            menu = QtWidgets.QMenu()
#            subMenu_data = menu.addMenu("Data")
#            
#            subMenu_data_import = subMenu_data.addMenu("Import Data")
#            subMenu_data_import.addAction('Image', lambda: (self.add_data("image")))
#            subMenu_data_import.addAction('Bias', lambda: (self.add_data("bias")))
#            subMenu_data_import.addAction('Dark', lambda: (self.add_data("dark")))
#            subMenu_data_import.addAction('Flat', lambda: (self.add_data("flat")))
#            
#            subMenu_data_clear = subMenu_data.addMenu("Clear Lists")
#            subMenu_data_clear.addAction('Clear All Lists', lambda: (self.clear_list("all")))
#            subMenu_data_clear.addAction('Clear Image List', lambda: (self.clear_list("image")))
#            subMenu_data_clear.addAction('Clear Bias List', lambda: (self.clear_list("bias")))
#            subMenu_data_clear.addAction('Clear Dark List', lambda: (self.clear_list("dark")))
#            subMenu_data_clear.addAction('Clear Flat List', lambda: (self.clear_list("flat")))
#            
#            subMenu_analyse = menu.addMenu("Analyse")
#            subMenu_analyse_combine = subMenu_analyse.addMenu("Combine")
#            subMenu_analyse_combine.addAction('Median...', lambda: (self.combine_images("median")))
#            subMenu_analyse_combine.addAction('Average...', lambda: (self.combine_images("average")))
#            subMenu_analyse_combine.addAction('Sum...', lambda: (self.combine_images("sum")))
#            subMenu_analyse_combine.addAction('Difference...', lambda: (self.combine_images("diff")))
#            
#            subMenu_analyse.addAction('Calibration', lambda: (print("calibration")))
#            subMenu_analyse.addAction('Align', lambda: (print("align")))
#            subMenu_analyse.addAction('Photometry...', lambda: (self.open_window("photometry")))
#            subMenu_analyse.addAction('A_Track', lambda: (print("a_Track")))
#            
#            subMenu_editor = menu.addMenu("Editor")
#            subMenu_editor_header = subMenu_editor.addMenu("Header")
#            subMenu_editor_header.addAction('Header Editor...', lambda: (self.open_window("heditor")))
#            subMenu_editor_header.addAction('Header Calculator...', lambda: (self.open_window("hcalc")))
#            subMenu_editor_header.addAction('Header Extractor...', lambda: (self.open_window("hex")))
#            
#            subMenu_editor.addAction('Observatory...', lambda: (self.open_window("observatory")))
#            subMenu_editor.addAction('Cosmic Cleaner', lambda: (print("Cosmic Cleaner")))
#            subMenu_editor.addAction('WCS', lambda: (print("WCS")))
#            
#            menu.exec_(event.globalPos())
#            return(True)
            
        elif (event.type() == QtCore.QEvent.ContextMenu and
              source is self.bias_list):
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_data("bias")))
            menu.addAction('Remove', lambda: (self.rm_data("bias")))
            menu.addSeparator()
            menu.addAction('Animate', lambda: (self.animate(self.bias_list)))
            menu.addAction('Display..', lambda: (self.display(
                    self.bias_list, False)))
            menu.addAction('Display in New Window', lambda: (
                    self.display(self.bias_list, True)))
            menu.exec_(event.globalPos())
            return(True)
            
        elif (event.type() == QtCore.QEvent.ContextMenu and
              source is self.dark_list):
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_data("dark")))
            menu.addAction('Remove', lambda: (self.rm_data("dark")))
            menu.addSeparator()
            menu.addAction('Animate', lambda: (self.animate(self.dark_list)))
            menu.addAction('Display..', lambda: (self.display(
                    self.dark_list, False)))
            menu.addAction('Display in New Window...', lambda: (
                    self.display(self.dark_list, True)))
            menu.exec_(event.globalPos())
            return(True)
            
        elif (event.type() == QtCore.QEvent.ContextMenu and
              source is self.flat_list):
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_data("flat")))
            menu.addAction('Remove', lambda: (self.rm_data("flat")))
            menu.addSeparator()
            menu.addAction('Animate', lambda: (self.animate(self.flat_list)))
            menu.addAction('Display..', lambda: (self.display(
                    self.flat_list, False)))
            menu.addAction('Display in New Window...', lambda: (
                    self.display(self.flat_list, True)))
            menu.exec_(event.globalPos())
            return(True)
        
        return super(MainWindow, self).eventFilter(source, event)
        
    def display(self, device, new_window):
        if device.currentItem() is not None:
            path = device.currentItem().text(0)
            if self.fts.check(path):
                self.open_window("display", [path, new_window])
                
        self.reload_log()
        
    def animate(self, device):
        files = self.fnk_deve.get_from_tree(device, selected=True)
        if len(files) > 1:
            self.open_window("animate", arg=files)
        elif len(files) == 1:
            self.logger.log(
                    "Trying to animate one file. Redirecting to Display")
            self.open_window("display", arg=[files[0], True])
        
        
    def add_lines_to_files_tree(self, device):
        self.logger.log("Getting File List")
        files = self.fnk_file.get_files()
        if files:                
            images_to_add = []
            for it, file in enumerate(files):
                if self.fts.check(file):
                    file_type = str(self.fts.header(file, "IMAGETYP"))
                    stats = self.fts.stats(file)
                    images_to_add.append([file, file_type, stats])
                    
                self.progress.setProperty("value", 100 * (it + 1)/(len(files)))
            
            if len(images_to_add) > 0:
                self.logger.log("Add File List to View")
                self.fnk_deve.add_to_tree(images_to_add, device)
                
        self.reload_log()
        
    def rm_data(self, typ):
        if typ== "image":
            device = self.image_list
        elif typ== "bias":
            device = self.bias_list
        elif typ== "dark":
            device = self.dark_list
        elif typ== "flat":
            device = self.flat_list
            
        self.logger.log("Removing Data From List")
        self.fnk_deve.rm_from_tree(device)
            
        self.reload_log()
        
    def add_data(self, typ):
        if typ == "image":
            device = self.image_list
            self.file_containter.setCurrentIndex(0)
        elif typ == "bias":
            device = self.bias_list
            self.file_containter.setCurrentIndex(1)
        elif typ == "dark":
            device = self.dark_list
            self.file_containter.setCurrentIndex(2)
        elif typ == "flat":
            device = self.flat_list
            self.file_containter.setCurrentIndex(3)
            
        self.add_lines_to_files_tree(device)
        self.reload_log()
        
    def open_window(self, window_name, arg=None):
        self.logger.log("Open Window Requested {}".format(window_name))
        
        if window_name == "photometry":
            if self.photometry_window is None:
                self.photometry_window = PhotometryWindow(
                        self, arg, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.photometry_window)
                self.photometry_window.show()
            else:
                self.photometry_window.show_me(arg)
                
        elif window_name == "licence":
            if self.licence_window is None:
                self.licence_window = LicenceWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.licence_window)
                self.licence_window.show()
                
        elif window_name == "proc":
            if self.proc_window is None:
                self.proc_window = ProcWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.proc_window)
                self.proc_window.show()
                
        elif window_name == "ginga":
            if self.ginga_window is None:
                self.ginga_window = GingaWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.ginga_window)
                self.ginga_window.show()
        
        elif window_name == "astrometry":
            if self.astrometry_window is None:
                self.astrometry_window = AstrometryWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.astrometry_window)
                self.astrometry_window.show()
                
        elif window_name == "ccleaner":
            if self.ccleaner_window is None:
                self.ccleaner_window = CCleanerWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.ccleaner_window)
                self.ccleaner_window.show()
                
        elif window_name == "alipy":
            if self.alipy_window is None:
                self.alipy_window = AlipyWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.alipy_window)
                self.alipy_window.show()
                
        elif window_name == "alignmanual":
            if self.alignmanual_window is None:
                self.alignmanual_window = AlignManualWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.alignmanual_window)
                self.alignmanual_window.show()
                
        elif window_name == "analyse":
            if self.analyse_window is None:
                self.analyse_window = AnalyseWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.analyse_window)
                self.analyse_window.show()
                
        elif window_name == "editor":
            if self.editor_window is None:
                self.editor_window = EditorWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.editor_window)
                self.editor_window.show()
                
        elif window_name == "about":
            if self.abuot_window is None:
                self.abuot_window = AboutWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.abuot_window)
                self.abuot_window.show()
                
        elif window_name == "logger":
            if self.logger_window is None:
                self.logger_window = LoggerWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.logger_window)
                self.logger_window.show()
                
        elif window_name == "credits":
            if self.credits_window is None:
                self.credits_window = CreditsWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.credits_window)
                self.credits_window.show()
                
        elif window_name == "observatory":
            if self.observatory_window is None:
                self.observatory_window = ObservatoryWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.observatory_window)
                self.observatory_window.show()
                
        elif window_name == "heditor":
            if self.heditor_window is None:
                self.heditor_window = HEditorWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.heditor_window)
                self.heditor_window.show()
        
        elif window_name == "hcalc":
            if self.hcalc_window is None:
                self.hcalc_window = HCalcWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.hcalc_window)
                self.hcalc_window.show()
                
        elif window_name == "hex":
            if self.hex_window is None:
                self.hex_window = HexWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.hex_window)
                self.hex_window.show()
                
        elif window_name == "display":
            if arg[1]:
                    self.display_window.append(DisplayWindow(
                            self, arg[0], verb=self.verb,
                            debugger=self.debugger))
                    self.play_ground.addSubWindow(self.display_window[-1])
                    self.display_window[-1].show()
            else:
                if self.display_window == []:
                    self.display_window.append(DisplayWindow(
                            self, arg[0], verb=self.verb,
                            debugger=self.debugger))
                    self.play_ground.addSubWindow(self.display_window[-1])
                    self.display_window[-1].show()
                else:
                    self.display_window[-1].show_me(arg[0])
                    
        elif window_name == "subtract":
            if self.subtraction_window is None:
                self.subtraction_window = SubtractionWindow(
                        self, arg, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.subtraction_window)
                self.subtraction_window.show()
            else:
                self.subtraction_window.update_lists(arg)
                
        elif window_name == "scalibration":
            if self.scalibration_window is None:
                self.scalibration_window = SetCalibrationWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.scalibration_window)
                self.scalibration_window.show()
                
        elif window_name == "sphotometry":
            if self.sphotometry_window is None:
                self.sphotometry_window = SetPhotometryWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.sphotometry_window)
                self.sphotometry_window.show()
                
        elif window_name == "sccleaner":
            if self.sccleaner_window is None:
                self.sccleaner_window = SetCCleanerWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.sccleaner_window)
                self.sccleaner_window.show()
                
        elif window_name == "swcs":
            if self.sastrometry_window is None:
                self.sastrometry_window = SetAstrometryWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.sastrometry_window)
                self.sastrometry_window.show()
                
        elif window_name == "animate":
            if self.animate_window is None:
                self.animate_window = AnimateWindow(
                        self, arg, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.animate_window)
                self.animate_window.show()
                
        elif window_name == "albategnius":
            if self.albategnius_window is None:
                self.albategnius_window = AlbategniusWindow(
                        self, verb=self.verb, debugger=self.debugger)
                self.play_ground.addSubWindow(self.albategnius_window)
                self.albategnius_window.show()
                
        self.reload_log()
                
                
    def closeEvent(self, event):
        widgetList = self.play_ground.subWindowList()
        if len(widgetList) > 0:
            if self.fnk_deve.ask("Are you sure you want to quit?"):
                event.accept()
            else:
                event.ignore()
    
    def exit(self):
        widgetList = self.play_ground.subWindowList()
        if len(widgetList) > 0:
            if self.fnk_deve.ask("Are you sure you want to quit?"):
                self.destroy()

class AnimateWindow(QtWidgets.QWidget, animate.Ui_Form):
    def __init__(self, parent, image_list, verb=False, debugger=False):
        self.parent = parent
        super(AnimateWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        
        self.image_list = image_list
        
        self.timer = QtCore.QBasicTimer()
        self.started = False
        
        self.set_slider_range()
        
        
        self.disp = FitsPlot(self.animate_display.canvas,
                                  verb=self.verb, debugger=self.debugger)
        self.load_all_images()
        self.show_first()
        self.animate_goNext.clicked.connect(lambda: (self.show_next()))
        self.animate_goPrevious.clicked.connect(lambda: (self.show_prev()))
        self.animate_goLast.clicked.connect(lambda: (self.show_last()))
        self.animate_goFirst.clicked.connect(lambda: (self.show_first()))
        self.animate_playPause.clicked.connect(lambda: (self.play_pause()))
        
        self.animate_display.canvas.fig.canvas.mpl_connect(
                'motion_notify_event', self.onpick)
        
    def onpick(self, event):
        x, y = self.disp.get_xy()
        val = self.disp.get_data()
        self.animate_x.setText("{:.2f}".format(float(x)))
        self.animate_y.setText("{:.2f}".format(float(y)))
        self.animate_value.setText("{:.2f}".format(float(val)))
        
    def write_file_name(self):
        value = self.animate_tim_line.value()
        self.animate_file_name.setText(self.image_list[value])
        
    def button_setup(self, logical):
        self.animate_goFirst.setEnabled(logical)
        self.animate_goPrevious.setEnabled(logical)
        self.animate_goNext.setEnabled(logical)
        self.animate_goLast.setEnabled(logical)
        
    def play_pause(self):
        self.started = not self.started
        self.button_setup(not self.started)
        if self.started:
            self.animate_playPause.setText("||")
            self.show_next()
            self.timer.start(300, self)
        else:
            self.timer.stop()
            self.animate_playPause.setText("|>")
            
    def timerEvent(self, e):
        self.show_next()
        
    def show_first(self):
        self.write_file_name()
        new_value = 0
        self.animate_tim_line.setValue(new_value)
        self.disp.show_from_all(new_value)
        
    def show_last(self):
        self.write_file_name()
        new_value = self.animate_tim_line.maximum()
        self.animate_tim_line.setValue(new_value)
        self.disp.show_from_all(new_value)
        
    def show_next(self):
        self.write_file_name()
        value = self.animate_tim_line.value()
        new_value = (value + 1) % (self.animate_tim_line.maximum() + 1)
        self.animate_tim_line.setValue(new_value)
        self.disp.show_from_all(new_value)
        
    def show_prev(self):
        self.write_file_name()
        value = self.animate_tim_line.value()
        new_value = (value - 1) % (self.animate_tim_line.maximum() + 1)
        self.animate_tim_line.setValue(new_value)
        self.disp.show_from_all(new_value)
        
    def load_all_images(self):
        self.disp.load_array(self.image_list)
        
    def set_slider_range(self):
        if self.image_list is not None:
            self.animate_tim_line.setMinimum(0)
            self.animate_tim_line.setMaximum(len(self.image_list) - 1)
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.animate_window = None

class DisplayWindow(QtWidgets.QWidget, display.Ui_Form):
    def __init__(self, parent, image, verb=False, debugger=False):
        self.parent = parent
        super(DisplayWindow, self).__init__(parent.play_ground)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        
        self.logger.log("DisplayW: Opening Display Window")
        
        self.logger.log("DisplayW: Creating Objects")
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.sar = analyse.Statistics.Array(verb=False, debugger=False)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        self.fnk_file = func.Files(self, self.logger)
        
        self.logger.log("DisplayW: Setting GUI")
        
        self.logger.log("DisplayW: Creating Triggers")
        self.display_export.clicked.connect(lambda: (self.save_file()))
        
        self.disp = FitsPlot(self.display_display.canvas,
                                  verb=self.verb, debugger=self.debugger)
        self.display_display.canvas.fig.canvas.mpl_connect(
                'motion_notify_event', self.onpick)
        
        self.data = None
        self.image = image
        
        self.show_me(self.image)
        
    def reload_log(self):
        self.logger.log("DisplayW: Reload Log File")
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def save_file(self):
        self.logger.log("DisplayW: Save Log Files")
        output_file = self.fnk_file.save_file()
        if output_file is not None:
            self.fop.cp(self.image, output_file)
            
        self.reload_log()
        
    def onpick(self, event):
        x, y = self.disp.get_xy()
        val = self.disp.get_data()
        self.display_x.setText("{:.2f}".format(float(x)))
        self.display_y.setText("{:.2f}".format(float(y)))
        self.display_value.setText("{:.2f}".format(float(val)))
        
    def show_me(self, image):
        self.logger.log("DisplayW: Display Data")
        self.disp.load(image)
        file_name = self.fop.abs_path(image)
        self.display_file_name.setText(file_name)
            
        self.reload_log()
        
    def closeEvent(self, event):
        self.logger.log("DisplayW: Kill on Close")
        self.parent.display_window.remove(self)

class PhotometryWindow(QtWidgets.QWidget, photometry.Ui_Form):
    def __init__(self, parent, image, verb=False, debugger=False):
        self.parent = parent
        super(PhotometryWindow, self).__init__(self.parent.play_ground)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        self.fnk_file = func.Files(self, self.logger)
        
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.coo = analyse.Astronomy.Coordinates(verb=self.verb,
                                           debugger=self.debugger)
        self.sar = analyse.Statistics.Array(verb=self.verb,
                                            debugger=self.debugger)
        self.sma = analyse.Statistics.Math(verb=self.verb,
                                           debugger=self.debugger)
        
        
        self.set_file = "{}_photometry.set".format(self.logger.setting_file)
        
        self.photometry_progress.setProperty("value", 0)
        
        self.photometry_go.clicked.connect(lambda: (self.do_photometry()))
        
        self.display_photometry = FitsPlot(self.photometry_display.canvas,
                                  verb=self.verb, debugger=self.debugger)
        
        self.photometry_display.canvas.fig.canvas.mpl_connect(
                'motion_notify_event', self.onpick)
        self.photometry_display.canvas.fig.canvas.mpl_connect(
                'button_press_event', self.get_coordinates)
        
        
        self.photometry_coordinates.installEventFilter(self)
        self.photometry_display.installEventFilter(self)
        
        self.artist = []
        self.artist_fwhm = []
        
        self.image = image
        self.data = None
        self.show_me(self.image)
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
    
    def get_pho_set(self):
        settings = self.fop.read_set("pho")
        try:
            settings['photpar_aperture'] = list(map(float,
                    settings['photpar_aperture'].split(",")))
        except Exception as e:
            self.logger.log("{}. Using default settings".format(e))
            settings['photpar_aperture'] = list(map(float,
                    self.logger.pho_set['photpar_aperture'].split(",")))
        return(settings)
        
    def do_photometry(self):
        files = self.fnk_deve.get_from_tree(self.parent.image_list)
        if len(files) > 0:
            coords = self.fnk_deve.list_of_list(self.photometry_coordinates)
            if len(coords) > 0:
                out_file = self.fnk_file.save_file(file_type="All (*.*)")
                if out_file is not None and not out_file == "":
                    f2w = open(out_file, "w")
                    the_set = self.get_pho_set()
                    
                    wanted_headers = the_set["header_to_use"].split(",")
                    if wanted_headers == ['']:
                        file_header = "file,x_coor,y_coor,aperture,flx,ferr,flag,mag,merr"
                    else:
                        file_header = "file,x_coor,y_coor,aperture,flx,ferr,flag,mag,merr,{}".format(",".join(wanted_headers))
                    f2w.write("{}\n".format(file_header))
                    use_coords = []
                    for coord in coords:
                        x, y = coord.split(" - ")
                        use_coords.append([float(x), float(y)])
                    for it, file in enumerate(files):
                        use_header = []
                        if not wanted_headers == ['']:
                            for wanted_header in wanted_headers:
                                use_header.append(
                                        str(self.fts.header(file,
                                                            wanted_header)))
                                
                        gvalue = self.fts.header(file, the_set["photpar_gain"])
                        if gvalue is None or gvalue == 0:
                            gvalue = 1.21
                        
                        phot = self.fts.mphotometry(
                                file, use_coords,
                                zmag=the_set["photpar_zmag"],
                                apertures=the_set["photpar_aperture"],
                                gain=gvalue)
                        for ph in phot:
                            if phot is not None:
                                if use_header == []:
                                    wirte_line = "{},{}\n".format(
                                            file, ",".join(ph))
                                else:
                                    wirte_line = "{},{},{}\n".format(
                                            file, ",".join(ph),
                                            ",".join(use_header))    
                            f2w.write(wirte_line)
                            
                        perc = 100 * (it + 1) / (len(files))
                        self.photometry_progress.setProperty("value", perc)
                    f2w.close()
                    
            else:
                self.logger.log("No coordinate was given")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Please select coordinate(s)"))
        else:
            self.logger.log("No file was given")
            QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Please add file(s)"))
            
        self.reload_log()
        
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.photometry_coordinates):
            menu = QtWidgets.QMenu()
            menu.addAction('Remove', lambda: (self.rm_line()))
            menu.addSeparator()
            menu.addAction('SEx!', lambda: (self.sex()))
            menu.addAction('Plot', lambda: (self.plot_coordinates()))
            menu.addSeparator()
            menu.addAction('Import', lambda: (self.import_coordinates()))
            menu.addAction('Export', lambda: (self.export_coordinates()))
            menu.exec_(event.globalPos())
            return(True)
            
        elif (event.type() == QtCore.QEvent.ContextMenu and
            source is self.photometry_display):
            menu = QtWidgets.QMenu()
            menu.addAction('FWHM', lambda: (self.get_fwhm()))
            menu.exec_(event.globalPos())
            return(True)
            
        return super(PhotometryWindow, self).eventFilter(source, event)
    
    def get_fwhm(self):
        if self.image is not None:
            sources = self.fts.star_finder(self.image, max_star=15000)
            x, y = self.display_photometry.get_xy()
            if sources is not None:
                index = self.coo.find_closest(sources, [x, y])
                if index is not None:
                    found_x = sources[index][0]
                    found_y = sources[index][1]
                    circ = Circle((found_x, found_y), 10, edgecolor="#FFFF00",
                                  facecolor="none")
                    self.artist_fwhm.append(
                            self.photometry_display.canvas.fig.gca(
                                    ).add_artist(circ))
                    circ.center = found_x, found_y
                    self.artist_fwhm.append(
                            self.photometry_display.canvas.fig.gca().annotate(
                                    "Obj", xy = (found_x, found_y),
                                    color = "#FFFF00", fontsize = 10))
                    self.photometry_display.canvas.draw()
                    QtWidgets.QMessageBox.information(
                            self, ("MYRaf Information"),
                            ("FWHM: {}".format(sources[index][2])))
                    for art in self.artist_fwhm:
                        art.remove()
                    self.artist_fwhm = []
                    self.photometry_display.canvas.draw()
            else:
                self.logger.log("Could't find any source(s)")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Could't find any source(s)"))
        else:
            self.logger.log("No image file was given")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("No image file was given"))
    
    def rm_line(self):
        self.fnk_deve.rm(self.photometry_coordinates)
        self.reload_log()
                
    def get_max_source(self):
        try:
            if self.fop.is_file(self.set_file):
                setting_file = open(self.set_file, "r")
                
                for line in setting_file:
                    ln = line.replace("\n", "").split("|")
                    if ln[0] == "stf_max":
                        return(int(ln[1]))
                        
                return(500)
            else:
                return(500)
        except Exception as e:
            self.logger.log(e)
            return(500)
    
    def sex(self):
        if self.image is not None:
            max_str = self.get_max_source()
            sources = self.fts.star_finder(self.image, max_star=max_str)
            if sources is not None:
                use_sources = []
                for source in sources:
                    use_sources.append("{:.2f} - {:.2f}".format(source[0],
                                       source[1]))
                self.fnk_deve.replace_list_con(self.photometry_coordinates,
                                               use_sources)
            else:
                self.logger.log("Could't find any source(s)")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Could't find any source(s)"))
        else:
            self.logger.log("No image file was given")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("No image file was given"))
            
    def plot_coordinates(self):
        coords = self.fnk_deve.list_of_selected(self.photometry_coordinates)
        if not coords == []:
            for art in self.artist:
                art.remove()
            self.artist = []
            
            settings = self.fop.read_set("pho")
            try:
                aperture = settings['photpar_aperture']
                if aperture is None:
                    aperture = self.logger.pho_set['photpar_aperture']
                    
            except Exception as e:
                self.logger.log(e)
                settings = self.logger.pho_set
                aperture = settings['photpar_aperture']
                
            print(aperture)
            for it, coord in enumerate(coords):
                print(coord)
                x, y = coord.split(" - ")
                x, y = float(x), float(y)
                circ = Circle((x, y), aperture, edgecolor="#00FFFF",
                              facecolor="none")
                self.artist.append(self.photometry_display.canvas.fig.gca(
                        ).add_artist(circ))
                circ.center = x, y
                self.artist.append(self.photometry_display.canvas.fig.gca(
                        ).annotate("s{}".format(str(it)), xy = (x, y),
                                  color = "#00FFFF", fontsize = 10))

            self.photometry_display.canvas.draw()

        else:
            self.logger.log("No coordinates to plot")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("Please add coordinate(s)"))
            
        self.reload_log()
                    
    def import_coordinates(self):
        file = self.fnk_file.get_files(file_type="All (*.*)")
        if not file == []:
            file = file[0]
            lines_2_add = []
            f2r = open(file, "r")
            for line in f2r:
                try:
                    if not line.startswith("#"):
                        coord = line.replace("\n", "")
                        x, y = coord.split(",")
                        lines_2_add.append("{} - {}".format(
                                str(float(x)), str(float(y))))
                except Exception as e:
                    self.logger.log(e)
            f2r.close()
            self.fnk_deve.replace_list_con(self.photometry_coordinates,
                                           lines_2_add)
            
        self.reload_log()
    
    def export_coordinates(self):
        coords = self.fnk_deve.list_of_list(self.photometry_coordinates)
        if not coords == []:
            file = self.fnk_file.save_file(file_type="All (*.*)")
            if not file == "":
                f2w = open(file, "w")
                f2w.write("#X_coord,Y_coord\n")
                for coord in coords:
                    f2w.write("{}\n".format(coord.replace(" - ", ",")))
                f2w.close()
        else:
            self.logger.log("No coordinates to export")
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"), ("No coordinates to export"))
            
        self.reload_log()
        
    def get_coordinates(self, event):
        if event.button == 1:
            x, y = self.display_photometry.get_xy()
            self.fnk_deve.add(self.photometry_coordinates,
                              ["{:.2f} - {:.2f}".format(float(x), float(y))])
                    
        self.reload_log()
        
    def onpick(self, event):
        x, y = self.display_photometry.get_xy()
        self.photometry_annotation.setText("{:.4f}, {:.4f}".format(x, y))
                
        self.reload_log()
            
    def show_me(self, image):
        self.logger.log("Photometry: Display Data")
        self.display_photometry.load(image)
        self.image = image
        self.reload_log()
            
    def closeEvent(self, event):
        self.parent.photometry_window = None
        
class ObservatoryWindow(QtWidgets.QWidget, observatory.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(ObservatoryWindow, self).__init__(self.parent.play_ground)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        
        self.reload_observatories()
        
        self.observatory_reload.clicked.connect(lambda: (
                self.reload_observatories()))
        
        self.observatory_add.clicked.connect(lambda: (
                self.create_observatory()))
        
        self.observatory_list.clicked.connect(lambda: (
                self.fill_observatory()))
        
        self.observatory_remove.clicked.connect(lambda: (
                self.remove_observatory()))
        
        
    def fill_observatory(self):
        obs = self.observatory_list.currentItem()
        if obs is not None:
            observatory = obs.text()
            file = "{}/{}".format(self.logger.obs_dir, observatory)
            
            properties = self.fop.read_json(file)
            
            
            self.observatory_abbreviation.setText(properties["observatory"])
            self.observatory_name.setText(properties["name"])
            self.observatory_longitude.setText(properties["longitude"])
            self.observatory_latitude.setText(properties["latitude"])
            self.observatory_altitude.setText(properties["altitude"])
            self.observatory_timezone.setText(properties["timezone"])
            self.observatory_commend.setPlainText(properties["commendation"])
            
        
    def remove_observatory(self):
        if self.observatory_list.currentItem() is not None:
            files = self.fnk_deve.list_of_selected(self.observatory_list)
            for file in files:
                file_to_delete = "{}/{}".format(self.logger.obs_dir, file)
                self.fop.rm(file_to_delete)
                
            self.reload_observatories()
        else:
            self.logger.log("Please select an observatory to delete")
        
    def create_observatory(self):
        try:
            observatory = self.observatory_abbreviation.text()
            name = self.observatory_name.text()
            longitude = self.observatory_longitude.text()
            latitude = self.observatory_latitude.text()
            altitude = self.observatory_altitude.text()
            timezone = self.observatory_timezone.text()
            commendation = self.observatory_commend.toPlainText()
            
            if not (observatory.strip() == "" or
                    name.strip() == "" or
                    longitude.strip() == "" or
                    latitude.strip() == "" or
                    altitude.strip() == "" or
                    timezone.strip() == ""):
                
                observat = {"observatory":observatory.strip(),
                            "name":name.strip(),
                            "longitude":longitude.strip(),
                            "latitude":latitude.strip(),
                            "altitude":altitude.strip(),
                            "timezone":timezone.strip(),
                            "commendation":commendation.strip()}
                
                file_name = "{}/{}".format(self.logger.obs_dir, observatory)
                
                self.fop.write_json(file_name, observat)
                
                self.observatory_abbreviation.setText("")
                self.observatory_name.setText("")
                self.observatory_longitude.setText("")
                self.observatory_latitude.setText("")
                self.observatory_altitude.setText("")
                self.observatory_timezone.setText("")
                self.observatory_commend.setPlainText("")
            
                self.reload_observatories()
            else:
                self.logger.log("At least one value is empty.")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("All fields must be filled."))
        except Exception as e:
            self.logger.log(e)
        
    def reload_observatories(self):
        
        observatories = self.fop.list_of_observatories()
        if observatories is not None:
            
            observats = []
            
            for observat in observatories:
                pn, fn = self.fop.get_base_name(observat)
                observats.append(fn)
            
            self.fnk_deve.replace_list_con(self.observatory_list, observats)
        else:
            self.logger.log("No observatory found")
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.observatory_window = None
    
class HEditorWindow(QtWidgets.QWidget, header_editor.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(HEditorWindow, self).__init__(self.parent.play_ground)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        
        self.header_progress.setProperty("value", 0)
        
        self.header_useExisting.clicked.connect(lambda: (
                self.header_value.setEnabled(
                        not self.header_useExisting.isChecked()),
                self.header_listOfExisting.setEnabled(
                        self.header_useExisting.isChecked())))
        self.header_hlist.clicked.connect(lambda: (self.fill_values()))
        self.header_delete.clicked.connect(lambda: (self.delete_header()))
        self.header_insert_update.clicked.connect(lambda: (self.update()))
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def update(self):
        all_files = None
        if self.parent.file_containter.currentIndex() == 0:
            device = self.parent.image_list
        elif self.parent.file_containter.currentIndex() == 1:
            device = self.parent.bias_list
        elif self.parent.file_containter.currentIndex() == 2:
            device = self.parent.dark_list
        elif self.parent.file_containter.currentIndex() == 3:
            device = self.parent.flat_list
            
        all_files = self.fnk_deve.get_from_tree(device, selected=False)
        
        if not (all_files is None or all_files == []):
            field = self.header_field.text()
            if self.header_useExisting.isChecked():
                value_field = self.header_listOfExisting.currentText()
                if value_field is not None:
                    value_field = value_field.split("->")[0]
                    for it, file in enumerate(all_files):
                        value = self.fts.header(file, value_field)
                        if value is not None:
                            self.fts.update_header(file, field, value)
            else:
                value = self.header_value.text()
                for it, file in enumerate(all_files):
                    self.fts.update_header(file, field, value)
                    self.header_progress.setProperty("value",
                                                     100 * (it + 1)/(len(
                                                             all_files)))
                    self.header_annotation.setProperty("text", file)
                
            self.parent.list_clicked(device)
        
        self.reload_log()
        
    def delete_header(self):
        all_files = None
        if self.parent.file_containter.currentIndex() == 0:
            device = self.parent.image_list
        elif self.parent.file_containter.currentIndex() == 1:
            device = self.parent.bias_list
        elif self.parent.file_containter.currentIndex() == 2:
            device = self.parent.dark_list
        elif self.parent.file_containter.currentIndex() == 3:
            device = self.parent.flat_list
            
        all_files = self.fnk_deve.get_from_tree(device, selected=False)
            
        if not (all_files is None or all_files == []):
            field = self.header_field.text()
            if not field == "":
                for it, file in enumerate(all_files):
                    self.fts.delete_header(file, field)
                    self.header_progress.setProperty("value",
                                                     100 * (it + 1)/(len(
                                                             all_files)))
                    self.header_annotation.setProperty("text", file)
                    
            self.parent.list_clicked(device)
            
        self.reload_log()
        
    def fill_values(self):
        line = self.header_hlist.currentItem()
        if line is not None:
            line = line.text()
            field, value = line.split("->")
            self.header_field.setProperty("text", field)
            self.header_value.setProperty("text", value)
            
        self.reload_log()
        
    def fill_header_list(self, header_list):
        self.fnk_deve.replace_list_con(self.header_hlist, header_list)
        self.fnk_deve.c_replace_list_con(self.header_listOfExisting,
                                         header_list)
        self.reload_log()
        
    def closeEvent(self, event):
        self.parent.heditor_window = None

class HCalcWindow(QtWidgets.QWidget, header_calculator.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(HCalcWindow, self).__init__(self.parent.play_ground)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.atm = analyse.Astronomy.Time(verb=self.verb,
                                          debugger=self.debugger)
        
        self.hcalc_progress.setProperty("value", 0)
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        
        self.hcalc_go.clicked.connect(lambda: (self.calculate()))
        
        self.hcalc_jd_time.currentIndexChanged.connect(lambda: (
                self.time_change(self.hcalc_jd_time)))
    
    def time_change(self, dev):
        if dev is not None:
            devices = [self.hcalc_jd_time,
                       self.hcalc_airmass_time,
                       self.hcalc_time_time]
            for device in devices:
                if device is not dev:
                    device.setCurrentIndex(dev.currentIndex())
    
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def calculate(self):
        files = self.fnk_deve.get_from_tree(self.parent.image_list)
        if len(files) > 0:
            do_jd = self.hcalc_jd.isChecked()
            do_airmass = self.hcalc_airmass.isChecked()
            do_imexamine = self.hcalc_imexamine.isChecked()
            do_time = self.hcalc_time.isChecked()
            prefx = self.hcalc_prefix.text()
            if do_jd or do_airmass or do_imexamine or do_time:
                utc_head_jd = self.hcalc_jd_time.currentText().split("->")[0]
                utc_head_tc = self.hcalc_time_time.currentText().split("->")[0]
                for it, file in enumerate(files):
                    if do_jd:
                        utc = self.fts.header(file, field=utc_head_jd)
                        if utc is not None:
                            jd = self.atm.jd(utc)
                            if jd is not None:
                                self.fts.update_header(file,
                                                       "{}_jd".format(prefx),
                                                       jd)
                            else:
                                self.logger.log(
                                        "Cannot calculate JD for ({})".format(
                                                utc))
                    if do_airmass:
                        pass
                    
                    if do_imexamine:
                        mean = self.hcalc_imexamine_mean.isChecked()
                        median = self.hcalc_imexamine_median.isChecked()
                        stdv = self.hcalc_imexamine_stdv.isChecked()
                        the_min = self.hcalc_imexamine_min.isChecked()
                        the_max = self.hcalc_imexamine_max.isChecked()
                        
                        if mean or median or stdv or the_min or the_max:
                            try:
                                stats = self.fts.stats(file)
                                
                                add_to_header = []
                                if mean:
                                    add_to_header.append([
                                            "{}_mean".format(prefx),
                                            stats["Mean"]])
                                if median:
                                    add_to_header.append([
                                            "{}_medi".format(prefx),
                                            stats["Median"]])
                                if stdv:
                                    add_to_header.append([
                                            "{}_stdv".format(prefx),
                                            stats["Stdev"]])
                                if the_min:
                                    add_to_header.append([
                                            "{}_min".format(prefx),
                                            stats["Min"]])
                                if the_max:
                                    add_to_header.append([
                                            "{}_max".format(prefx),
                                            stats["Max"]])
                                    
                                self.fts.mupdate_header(file, add_to_header)
                            except Exception as e:
                                self.logger.log(e)
                        else:
                            self.logger.log("Nothing to do")
                            
                    if do_time:
                        utc = self.fts.header(file, field=utc_head_tc)
                        dif = self.hcalc_time_value.value()
                        dif_type = self.hcalc_time_valueType.currentText()
                        if utc is not None:
                            UTC = self.atm.str_to_time(str(utc))
                            if UTC is not None:
                                new_time = self.atm.time_diff(
                                        UTC, time_offset=dif,
                                        offset_type=dif_type)
                                
                                if new_time is not None:
                                    self.fts.update_header(
                                            file, "{}_ntime".format(prefx),
                                            str(new_time))
                                else:
                                    self.logger.log("Cannot calculate time_diff for ({})".format(utc))
                    
                    proc = 100 * (it + 1) / (len(files))
                    self.hcalc_progress.setProperty("value", proc)
            else:
                self.logger.log("Nothing to do")
                QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Don't know what to do"))
            
        else:
            self.logger.log("No file was given")
            QtWidgets.QMessageBox.critical(
                        self, ("MYRaf Error"), ("Please add file(s)"))
        
    def fill_header_list(self, header_list):
        self.fnk_deve.c_replace_list_con(self.hcalc_jd_time, header_list)
        self.fnk_deve.c_replace_list_con(self.hcalc_airmass_time, header_list)
        self.fnk_deve.c_replace_list_con(self.hcalc_airmass_ra, header_list)
        self.fnk_deve.c_replace_list_con(self.hcalc_airmass_dec, header_list)
        self.fnk_deve.c_replace_list_con(self.hcalc_airmass_observatory,
                                         header_list)
        self.fnk_deve.c_replace_list_con(self.hcalc_time_time, header_list)
        
        self.reload_log()
        
    def closeEvent(self, event):
        self.parent.hcalc_window = None
        
class HexWindow(QtWidgets.QWidget, header_extractor.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(HexWindow, self).__init__(self.parent.play_ground)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.hex_progress.setProperty("value", 0)
        
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        self.fnk_file = func.Files(self, self.logger)
        
        self.hex_go.clicked.connect(lambda: (self.extract()))
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def extract(self):
        
        all_files = None
        if self.parent.file_containter.currentIndex() == 0:
            device = self.parent.image_list
        elif self.parent.file_containter.currentIndex() == 1:
            device = self.parent.bias_list
        elif self.parent.file_containter.currentIndex() == 2:
            device = self.parent.dark_list
        elif self.parent.file_containter.currentIndex() == 3:
            device = self.parent.flat_list
            
        all_files = self.fnk_deve.get_from_tree(device, selected=False)
        
        if not (all_files is None or all_files == []):
            if len(self.fnk_deve.list_of_selected(self.hex_header_list)) > 0:
                output_file = self.fnk_file.save_file(file_type="All (*.*)")
                if output_file is not None and not output_file == "":
                    arr_to_write = []
                    for it, file in enumerate(all_files):
                        line_of_array = [file]
                        file_header = ["File_name"]
                        for header in self.fnk_deve.list_of_selected(
                                self.hex_header_list):
                            the_header = header.split("->")[0]
                            extracted_header = str(self.fts.header(file,
                                                                   the_header))
                            line_of_array.append(extracted_header)
                            file_header.append(the_header)
                        
                        self.hex_progress.setProperty("value",
                                                      100 * (it + 1) / (len(
                                                              all_files)))
                        arr_to_write.append(line_of_array)
                    
                    
                        f2w = open(output_file, "w")
                        f2w.write("#{}\n".format(",".join(file_header)))
                        for line in arr_to_write:
                            f2w.write("{}\n".format(",".join(line)))
                            
                    f2w.close()
                    
        self.reload_log()
        
    def fill_header_list(self, header_list):
        self.fnk_deve.replace_list_con(self.hex_header_list, header_list)
        self.reload_log()
        
    def closeEvent(self, event):
        self.parent.hex_window = None
        
class LicenceWindow(QtWidgets.QWidget, help_licence.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(LicenceWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.licence_window = None

class CreditsWindow(QtWidgets.QWidget, help_credits.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(CreditsWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.credits_window = None
        
class LoggerWindow(QtWidgets.QWidget, help_logger.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(LoggerWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        self.fnk_file = func.Files(self, self.logger)
        
        self.help_logger_reload.clicked.connect(lambda: (self.load()))
        self.help_logger_clear.clicked.connect(lambda: (self.clear_log()))
        self.help_logger_save.clicked.connect(lambda: (self.save_log()))
        
        self.load()
        
    def file_size(self):
        mlog_size = 0.
        log_size = 0.
        if self.fop.is_file(self.logger.mini_log_file):
            mlog_size = self.fop.get_size(self.logger.mini_log_file) / 1048576
        if self.fop.is_file(self.logger.log_file):
            log_size = self.fop.get_size(self.logger.log_file) / 1048576
        self.logger_annotation.setProperty(
                "text", "Total Temperory File size is: {:.2} MB".format(
                        mlog_size + log_size))
        
    def save_log(self):
        directory = self.fnk_file.save_directory()
        if directory is not None and not directory == "":
            self.fop.cp(self.logger.mini_log_file, directory)
            self.fop.cp(self.logger.log_file, directory)
        
    def load(self):
        write_arr = []
        if self.fop.is_file(self.logger.mini_log_file):
            tmp_file = open(self.logger.mini_log_file, "r")
            for line in tmp_file:
                write_arr.append(line.replace("\n", ""))
            
        self.fnk_deve.replace_list_con(self.help_logger_list, write_arr)
        self.help_logger_list.scrollToBottom()
        self.file_size()
        
    def clear_log(self):
        self.logger.dump_log()
        self.logger.dump_mlog()
        self.load()
        
    def closeEvent(self, event):
        self.parent.logger_window = None
        
class AboutWindow(QtWidgets.QWidget, help_aboutmyraf.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(AboutWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.abuot_window = None
        
class AnalyseWindow(QtWidgets.QWidget, help_analyse.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(AnalyseWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.analyse_window = None
        
class EditorWindow(QtWidgets.QWidget, help_editor.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(EditorWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.editor_window = None

class ProcWindow(QtWidgets.QWidget, myraf_progress.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(ProcWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.progress_progressBar.setProperty("value", 0)
        self.progress_annotation.setProperty("text", "")
        
    def kill_me(self):
        print(self)
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.proc_window = None
        
class GingaWindow(QtWidgets.QWidget, help_help_ginga.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(GingaWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.ginga_window = None
        
class AlipyWindow(QtWidgets.QWidget, help_help_alipy.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(AlipyWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.alipy_window = None
        
class CCleanerWindow(QtWidgets.QWidget, help_help_ccleaner.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(CCleanerWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.ccleaner_window = None
        
class AstrometryWindow(QtWidgets.QWidget, help_help_astrometrynet.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(AstrometryWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.astrometry_window = None
        
class AlignManualWindow(QtWidgets.QWidget, align_manual.Ui_Form):
    def __init__(self, parent, image=None, verb=False, debugger=False):
        self.parent = parent
        super(AlignManualWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        self.image = image
        
        self.disp = FitsPlot(self.manualAlign_display.canvas,
                                  verb=self.verb, debugger=self.debugger)
        
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.ira = analyse.Astronomy.Iraf(verb=self.verb,
                                          debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        
        self.fnk_deve = func.Devices(self, self.logger)
        self.fnk_file = func.Files(self, self.logger)
        
        self.manualAlign_progress.setProperty("value", 0)
        
        self.manualAlign_go.clicked.connect(lambda: (self.align()))
        
        self.manualAlign_display.canvas.fig.canvas.mpl_connect(
                'button_press_event', self.get_coordinate)
        self.manualAlign_display.canvas.fig.canvas.mpl_connect(
                'motion_notify_event', self.onpick)
        
        self.show_first_file()

    def align(self):
        files = self.fnk_deve.get_from_tree(self.parent.image_list)
        if files is not None and not files ==[]:
            ref = self.parent.image_list.currentItem().text(0)
            ref_x = self.fts.header(ref, "MYALIGNX")
            ref_y = self.fts.header(ref, "MYALIGNY")
            if ref_x is not None and ref_y is not None:
                out_dir = self.fnk_file.save_directory()
                if out_dir is not None and not out_dir == "":
                    for it, file in enumerate(files):
                        x = self.fts.header(file, "MYALIGNX")
                        y = self.fts.header(file, "MYALIGNY")
                        dx = ref_x - x
                        dy = ref_y - y
                        pn, fn = self.fop.get_base_name(file)
                        out_file = "{}/{}".format(out_dir, fn)
                        if self.fop.is_file(out_file):
                            self.fop.rm(out_file)
                        self.ira.imshift(file, out_file, dx, dy)
                        proc = 100 * (it + 1) / len(files)
                        self.manualAlign_progress.setProperty("value", proc)
        else:
            self.logger.log("No Image to Align")
            QtWidgets.QMessageBox.critical(self, ("MYRaf Error"),
                                           ("No Image to Align"))

    def onpick(self, event):
        x, y = self.disp.get_xy()
        self.manualAlign_update_x.setText("{:.4f}".format(x))
        self.manualAlign_update_y.setText("{:.4f}".format(y))

    def get_coordinate(self, event):
        if self.image is not None:
            x, y = self.disp.get_xy()
            self.fts.update_header(self.image, "MYALIGNX", x)
            self.fts.update_header(self.image, "MYALIGNY", y)
            new_row = self.parent.image_list.currentIndex().row() + 1
            lenght = len(self.fnk_deve.get_from_tree(self.parent.image_list))
            new_row = new_row % (lenght)
            self.parent.image_list.setCurrentItem(
                    self.parent.image_list.topLevelItem(new_row))
            path = self.parent.image_list.currentItem().text(0)
            self.show_me(path)

    def show_first_file(self):
        files = self.fnk_deve.get_from_tree(self.parent.image_list)
        if files is not None and not files == []:
            self.parent.image_list.setCurrentItem(
                    self.parent.image_list.topLevelItem(0))
            if self.parent.image_list.currentItem() is not None:
                file = self.parent.image_list.currentItem().text(0)
                self.show_me(file)
                
    def show_me(self, image):
        self.logger.log("DisplayW: Display Data")
        self.disp.load(image)
        self.image = self.fop.abs_path(image)
        x = self.fts.header(self.image, "MYALIGNX")
        y = self.fts.header(self.image, "MYALIGNY")
        if x is not None and y is not None:
            self.manualAlign_x.setText("{:.4f}".format(x))
            self.manualAlign_y.setText("{:.4f}".format(y))
            circ = Circle((x, y), 10, edgecolor="#00FFFF", facecolor="none")
            self.manualAlign_display.canvas.fig.gca( ).add_artist(circ)
            circ.center = x, y
            self.manualAlign_display.canvas.fig.gca(
                    ).annotate("REF", xy = (x, y),
                              color = "#00FFFF", fontsize = 10)
            self.manualAlign_display.canvas.draw()
        else:
            self.manualAlign_x.setText("{:.4f}".format(float('nan')))
            self.manualAlign_y.setText("{:.4f}".format(float('nan')))
        
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.alignmanual_window = None
        
class SetCalibrationWindow(QtWidgets.QWidget, setting_calibration.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(SetCalibrationWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        
        self.file = "{}_calibration.set".format(self.logger.setting_file)
        
        self.setting_calibration_save.clicked.connect(lambda: (self.save()))
        
        self.load()
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.scalibration_window = None
        
    def load_default(self):
        settings = self.logger.cal_set
        
        self.fop.write_set(settings, "cal")
        
        self.setting_calibration_z_combine.setCurrentIndex(
                settings['b_combine'])
        self.setting_calibration_z_rejection.setCurrentIndex(
                settings['b_rejection'])
        
        self.setting_calibration_d_combine.setCurrentIndex(
                settings['d_combine'])
        self.setting_calibration_d_rejection.setCurrentIndex(
                settings['d_rejection'])
        self.setting_calibration_d_scale.setCurrentIndex(
                settings['d_scale'])
        
        self.setting_calibration_f_combine.setCurrentIndex(
                settings['f_combine'])
        self.setting_calibration_f_rejection.setCurrentIndex(
                settings['f_rejection'])
    def load(self):
        try:
            settings = self.fop.read_set("cal")
            self.setting_calibration_z_combine.setCurrentIndex(
                    settings['b_combine'])
            self.setting_calibration_z_rejection.setCurrentIndex(
                    settings['b_rejection'])
            
            self.setting_calibration_d_combine.setCurrentIndex(
                    settings['d_combine'])
            self.setting_calibration_d_rejection.setCurrentIndex(
                    settings['d_rejection'])
            self.setting_calibration_d_scale.setCurrentIndex(
                    settings['d_scale'])
            
            self.setting_calibration_f_combine.setCurrentIndex(
                    settings['f_combine'])
            self.setting_calibration_f_rejection.setCurrentIndex(
                    settings['f_rejection'])
        except Exception as e:
            self.logger.log(e)
            self.load_default()
            
                    
        self.reload_log()
        
    def save(self):
        b_combine = self.setting_calibration_z_combine.currentIndex()
        b_rejection = self.setting_calibration_z_rejection.currentIndex()
        
        d_combine = self.setting_calibration_d_combine.currentIndex()
        d_rejection = self.setting_calibration_d_rejection.currentIndex()
        d_scale = self.setting_calibration_d_scale.currentIndex()
        
        f_combine = self.setting_calibration_f_combine.currentIndex()
        f_rejection = self.setting_calibration_f_rejection.currentIndex()
        
        cal_set = {"b_combine": b_combine, "b_rejection": b_rejection,
                   "d_combine": d_combine, "d_rejection": d_rejection,
                   "d_scale": d_scale, "f_combine": f_combine,
                   "f_rejection": f_rejection}
        
        self.fop.write_set(cal_set, "cal")
        self.reload_log()
        
    
class SetPhotometryWindow(QtWidgets.QWidget, setting_photometry.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(SetPhotometryWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        
        self.file = "{}_photometry.set".format(self.logger.setting_file)
        
        self.setting_phot_hex_add.clicked.connect(lambda: (self.add_head()))
        self.setting_phot_hex_remove.clicked.connect(lambda: (self.rm_head()))
        self.setting_phot_hex_update.clicked.connect(lambda: (self.update()))
        
        self.setting_phot_save.clicked.connect(lambda: (self.save()))
        
        self.load()
        
    def add_head(self):
        wanted_headers = self.fnk_deve.list_of_selected(
                self.setting_phot_hex_available)
        if not wanted_headers == []:
            already_using_h = self.fnk_deve.list_of_list(
                    self.setting_phot_hex_use)
            diff = set(wanted_headers) - set(already_using_h)
            if not diff == []:
                self.fnk_deve.add(self.setting_phot_hex_use, diff)
        else:
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("Please select header(s)"))
    
    def rm_head(self):
        self.fnk_deve.rm(self.setting_phot_hex_use)
    
    def update(self):
        files = self.fnk_deve.get_from_tree(self.parent.image_list)
        if files is not None and not files == []:
            file = files[0]
            headers = self.fts.header(file)
            add_to_list = []
            for header in headers:
                add_to_list.append(header[0])
                
            self.fnk_deve.replace_list_con(
                    self.setting_phot_hex_available, add_to_list)
        else:
            QtWidgets.QMessageBox.critical(
                    self, ("MYRaf Error"),
                    ("Please add file(s) to Image list"))
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.sphotometry_window = None
        
    def load_default(self):
        settings = self.logger.pho_set
        
        self.fop.write_set(settings, "pho")
        
        self.setting_phot_std.setChecked(settings['std_mag'])
        self.setting_phot_std_nomad.setChecked(settings['std_mag_nomad'])
        self.setting_phot_std_usno.setChecked(settings['std_mag_usno'])
        self.setting_phot_std_gaia.setChecked(settings['std_mag_gaia'])
        self.setting_photo_std_radius.setValue(settings['std_mag_radius'])
        
        self.setting_phot_datapar_exposure.setProperty(
                "text", settings['datapar_exposure'])
        self.setting_phot_datapar_filter.setProperty(
                "text", settings['datapar_filter'])
        self.setting_phot_photpar_aperture.setProperty(
                "text", settings['photpar_aperture'])
        self.setting_phot_photpar_zmag.setValue(settings['photpar_zmag'])
        self.setting_phot_photpar_gain.setProperty(
                "text", settings['photpar_gain'])
        
        self.setting_phot_wcs_ra.setProperty("text", settings['wcs_ra'])
        self.setting_phot_wcs_dec.setProperty("text", settings['wcs_dec'])
        
        self.setting_phot_tlc_observatory.setProperty(
                "text", settings['lot_obse'])
        self.setting_phot_tlc_time.setProperty("text", settings['lot_time'])
        
        self.setting_phot_starf_max.setValue(settings['stf_max'])
        
        if not settings['header_to_use'] == "":
            headers = settings['header_to_use'].split(",")
            self.fnk_deve.replace_list_con(self.setting_phot_hex_use, headers)
        
    def load(self):
        try:
            settings = self.fop.read_set("pho")
            self.setting_phot_std.setChecked(settings['std_mag'])
            self.setting_phot_std_nomad.setChecked(settings['std_mag_nomad'])
            self.setting_phot_std_usno.setChecked(settings['std_mag_usno'])
            self.setting_phot_std_gaia.setChecked(settings['std_mag_gaia'])
            self.setting_photo_std_radius.setValue(settings['std_mag_radius'])
            
            self.setting_phot_datapar_exposure.setProperty(
                    "text", settings['datapar_exposure'])
            self.setting_phot_datapar_filter.setProperty(
                    "text", settings['datapar_filter'])
            self.setting_phot_photpar_aperture.setProperty(
                "text", settings['photpar_aperture'])
            self.setting_phot_photpar_zmag.setValue(settings['photpar_zmag'])
            self.setting_phot_photpar_gain.setProperty(
                    "text", settings['photpar_gain'])
            
            self.setting_phot_wcs_ra.setProperty("text", settings['wcs_ra'])
            self.setting_phot_wcs_dec.setProperty("text", settings['wcs_dec'])
            
            self.setting_phot_tlc_observatory.setProperty(
                    "text", settings['lot_obse'])
            self.setting_phot_tlc_time.setProperty(
                    "text", settings['lot_time'])
            
            self.setting_phot_starf_max.setValue(settings['stf_max'])
            
            if not settings['header_to_use'] == "":
                headers = settings['header_to_use'].split(",")
                self.fnk_deve.replace_list_con(
                        self.setting_phot_hex_use, headers)
        except Exception as e:
            self.logger.log(e)
            
        
        self.reload_log()
        
    def save(self):
        std_mag = self.setting_phot_std.isChecked()
        std_mag_nomad = self.setting_phot_std_nomad.isChecked()
        std_mag_usno = self.setting_phot_std_usno.isChecked()
        std_mag_gaia = self.setting_phot_std_gaia.isChecked()
        std_mag_radius = self.setting_photo_std_radius.value()
        
        datapar_exposure = self.setting_phot_datapar_exposure.text()
        datapar_filter = self.setting_phot_datapar_filter.text()
        
        photpar_aperture = self.setting_phot_photpar_aperture.text()
        photpar_zmag = self.setting_phot_photpar_zmag.value()
        photpar_gain = self.setting_phot_photpar_gain.text()
        
        wcs_ra = self.setting_phot_wcs_ra.text()
        wcs_dec = self.setting_phot_wcs_dec.text()
        
        lot_obse = self.setting_phot_tlc_observatory.text()
        lot_time = self.setting_phot_tlc_time.text()
        
        stf_max = self.setting_phot_starf_max.value()
        
        #setting_phot_hex_use
        header_to_use = ",".join(self.fnk_deve.list_of_list(
                self.setting_phot_hex_use))
        
        
        
        pho_set = {"std_mag": std_mag, "std_mag_nomad": std_mag_nomad,
                   "std_mag_usno": std_mag_usno, "std_mag_gaia": std_mag_gaia,
                   "std_mag_radius": std_mag_radius,
                   
                   "datapar_exposure": datapar_exposure,
                   "datapar_filter": datapar_filter,
                   
                   "photpar_aperture": photpar_aperture,
                   "photpar_zmag": photpar_zmag, "photpar_gain": photpar_gain,
                   
                   "wcs_ra": wcs_ra, "wcs_dec": wcs_dec,
                   
                   "lot_obse": lot_obse, "lot_time": lot_time,
                   "stf_max": stf_max,
                   
                   "header_to_use": header_to_use}
        
        self.fop.write_set(pho_set, "pho")
        
        self.reload_log()
        
        
class SetCCleanerWindow(QtWidgets.QWidget, setting_cosmiccleaner.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(SetCCleanerWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        
        self.file = "{}_cosmiccleaner.set".format(self.logger.setting_file)
        
        self.setting_cclener_save.clicked.connect(lambda: (self.save()))
        
        self.load()
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def closeEvent(self, event):
        self.parent.sccleaner_window = None
        
    def load_default(self):
        settings = self.logger.cos_set
        self.setting_cclener_gain.setValue(settings["gain"])
        self.setting_cclener_readnoise.setValue(settings["reno"])
        self.setting_cclener_sigmaclip.setValue(settings["sicl"])
        self.setting_cclener_sigmafraction.setValue(settings["sifr"])
        self.setting_cclener_objectlimit.setValue(settings["obli"])
        self.setting_cclener_maxiteration.setValue(settings["mait"])
        self.setting_cclener_createmask.setChecked(settings["crma"])
        
    def load(self):
        try:
            settings = self.fop.read_set("cos")
            
            self.setting_cclener_gain.setValue(settings["gain"])
            self.setting_cclener_readnoise.setValue(settings["reno"])
            self.setting_cclener_sigmaclip.setValue(settings["sicl"])
            self.setting_cclener_sigmafraction.setValue(settings["sifr"])
            self.setting_cclener_objectlimit.setValue(settings["obli"])
            self.setting_cclener_maxiteration.setValue(settings["mait"])
            self.setting_cclener_createmask.setChecked(settings["crma"])
        except Exception as e:
            self.logger.log(e)
            self.load_default()
                    
        self.reload_log()
    
    def save(self):
        gain = self.setting_cclener_gain.value()
        reno = self.setting_cclener_readnoise.value()
        sicl = self.setting_cclener_sigmaclip.value()
        sifr = self.setting_cclener_sigmafraction.value()
        obli = self.setting_cclener_objectlimit.value()
        mait = self.setting_cclener_maxiteration.value()
        crma = self.setting_cclener_createmask.isChecked()
        
        
        cos_set = {"gain": gain, "reno": reno,
                        "sicl": sicl, "sifr": sifr,
                        "obli": obli, "mait": mait, "crma": crma}
                
        self.fop.write_set(cos_set, "cos")
        
        self.reload_log()
        
class SetAstrometryWindow(QtWidgets.QWidget, setting_astrometrynet.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(SetAstrometryWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        
        self.setting_astrometry_save.clicked.connect(lambda: (self.save()))
        
        self.load()
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
            
    def closeEvent(self, event):
        self.parent.sastrometry_window = None
            
    def load_default(self):
        settings = self.logger.cos_ast
        self.setting_astrometry_online.setChecked(settings["online"])
        self.setting_astrometry_online_server.setProperty(
                "text", settings['server'])
        self.setting_astrometry_online_apikey.setProperty(
                "text", settings['apike'])
        
    def load(self):
        try:
            settings = self.fop.read_set("ast")
            
            self.setting_astrometry_online.setChecked(settings["online"])
            self.setting_astrometry_online_server.setProperty(
                    "text", settings['server'])
            self.setting_astrometry_online_apikey.setProperty(
                    "text", settings['apike'])
            
        except Exception as e:
            self.logger.log(e)
            self.load_default()
                    
        self.reload_log()
    
    def save(self):
        online = self.setting_astrometry_online.isChecked()
        server = self.setting_astrometry_online_server.text()
        apike = self.setting_astrometry_online_apikey.text()
        
        
        cal_ast = {"online": online, "server": server, "apike": apike}
        
        self.fop.write_set(cal_ast, "ast")
        
        self.reload_log()
    
class SubtractionWindow(QtWidgets.QWidget, combine_subtraction.Ui_Form):
    def __init__(self, parent, files, verb=False, debugger=False):
        self.parent = parent
        super(SubtractionWindow, self).__init__(self.parent)
        self.setupUi(self)
        
        self.verb = verb
        self.debugger = debugger
        self.files = files
        
        self.fts = analyse.Astronomy.Fits(verb=self.verb,
                                          debugger=self.debugger)
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fnk_deve = func.Devices(self, self.logger)
        self.update_lists(self.files)
        
        self.subtract_go.clicked.connect(lambda: (self.calculate()))
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
        
    def update_lists(self, files):
        self.fnk_deve.c_replace_list_con(self.subtract_image1, files)
        self.fnk_deve.c_replace_list_con(self.subtract_image2, files)
        self.reload_log()
        
    def calculate(self):
        file1 = self.subtract_image1.currentText()
        file2 = self.subtract_image2.currentText()
        diff = self.fts.subtract(file1, file2)
        if diff is not None:
            the_file = "{}/myraf_diff_{}.fits".format(self.logger.tmp_dir,
                        self.logger.random_string(10))
            self.fts.write(the_file, diff)
            
            self.parent.open_window("display", [the_file, True])

        self.reload_log()
        
    def closeEvent(self, event):
        self.parent.subtraction_window = None

class AlbategniusWindow(QtWidgets.QWidget, albategnius.Ui_Form):
    def __init__(self, parent, verb=False, debugger=False):
        self.parent = parent
        super(AlbategniusWindow, self).__init__(self.parent)
        self.setupUi(self)
        
    def reload_log(self):
        if self.parent.logger_window is not None:
            self.parent.logger_window.load()
            
    def closeEvent(self, event):
        self.parent.albategnius_window = None

def main():
    parser = argparse.ArgumentParser(description='MYRaf V3 Beta')
    parser.add_argument("--verbose", "-v", help="Increase output verbosity",
                        action="store_true")
    parser.add_argument("--debugger", "-d", help="Debugger mode",
                        action="store_true")
    args = parser.parse_args()
    
    app = QtWidgets.QApplication(argv)
    window = MainWindow(verb=args.verbose, debugger=args.debugger)
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()