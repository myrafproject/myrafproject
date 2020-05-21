# -*- coding: utf-8 -*-
"""
@author: msh, yk
"""

try:
    from sys import argv

    import argparse

    from logging import getLogger, basicConfig

    from matplotlib.patches import Circle

    from PyQt5 import QtWidgets
    from PyQt5 import QtCore

    from gui import myraf
    from gui import function

    from myraflib import analyse
    from myraflib import env

    from fPlot import FitsPlot
except Exception as e:
    print(e)
    exit(0)


class MainWindow(QtWidgets.QMainWindow, myraf.Ui_MainWindow):
    def __init__(self, parent=None, logger_level=50, log_file=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.flags = QtCore.Qt.Window
        self.setWindowFlags(self.flags)

        try:
            logger_level = int(logger_level)
        except:
            logger_level = 50

        if not logger_level in [0, 10, 20, 30, 40, 50]:
            logger_level = 50

        LOG_FORMAT = "[%(asctime)s, %(levelname)s], [%(filename)s, %(funcName)s, %(lineno)s]: %(message)s"
        basicConfig(filename=log_file, level=logger_level, format=LOG_FORMAT)
        self.logger = getLogger()
        getLogger('matplotlib.font_manager').disabled = True

        self.gui_dev = function.Devices(self, self.logger)
        self.gui_file = function.Files(self, self.logger)
        self.fop = env.File(self.logger)
        self.fts = analyse.Astronomy.Fits(self.logger)
        self.iraf = analyse.Astronomy.Iraf(self.logger)

        self.align_display = FitsPlot(self.display_align.canvas, self.logger)
        self.phot_display = FitsPlot(self.display_phot.canvas, self.logger)

        self.calib_image_add.clicked.connect(lambda: (self.add_files(self.calib_image_list)))
        self.calib_image_remove.clicked.connect(lambda: (self.rm_files(self.calib_image_list)))

        self.calib_bias_add.clicked.connect(lambda: (self.add_files(self.calib_bias_list)))
        self.calib_bias_remove.clicked.connect(lambda: (self.rm_files(self.calib_bias_list)))
        self.calib_bias_combine.clicked.connect(lambda: (self.export_bias()))

        self.calib_dark_add.clicked.connect(lambda: (self.add_files(self.calib_dark_list)))
        self.calib_dark_remove.clicked.connect(lambda: (self.rm_files(self.calib_dark_list)))
        self.calib_dark_combine.clicked.connect(lambda: (self.export_dark()))

        self.calib_flat_add.clicked.connect(lambda: (self.add_files(self.calib_flat_list)))
        self.calib_flat_remove.clicked.connect(lambda: (self.rm_files(self.calib_flat_list)))
        self.calib_flat_combine.clicked.connect(lambda: (self.export_flat()))

        self.calibration_go.clicked.connect(lambda: (self.calibration()))

        self.cclean_add.clicked.connect(lambda: (self.add_files(self.cclean_list)))
        self.cclean_remove.clicked.connect(lambda: (self.rm_files(self.cclean_list)))
        self.cclean_go.clicked.connect(lambda: (self.cosmin_clean()))

        # cosmin_clean

        self.hedit_isvaluefromheader.clicked.connect(lambda: (self.toggle_header()))
        self.hedit_add.clicked.connect(lambda: (self.add_files(self.hedit_list)))
        self.hedit_remove.clicked.connect(lambda: (self.rm_files(self.hedit_list)))

        self.align_add.clicked.connect(lambda: (self.add_files(self.align_list)))
        self.align_remove.clicked.connect(lambda: (self.rm_files(self.align_list)))

        self.phot_add.clicked.connect(lambda: (self.add_files(self.phot_list)))
        self.phot_remove.clicked.connect(lambda: (self.rm_files(self.phot_list)))
        self.display_phot.canvas.fig.canvas.mpl_connect('button_press_event', self.get_coordinate_phot)

        # self.phot_add.clicked.connect(lambda: (self.add_files(self.update_list_of_headers)))

        self.hedit_remove_field.clicked.connect(lambda: (self.rm_header()))
        self.hedit_add_field.clicked.connect(lambda: (self.add_header()))

        self.align_list.clicked.connect(lambda: (self.display(self.align_list, self.align_display)))
        self.phot_list.clicked.connect(lambda: (self.display(self.phot_list, self.phot_display)))
        self.phot_list.clicked.connect(lambda: (self.update_list_of_headers()))

        self.hedit_list.clicked.connect(lambda: (self.show_headers()))
        self.hedit_header_table.clicked.connect(lambda: (self.header_selected()))

        self.phot_go.clicked.connect(lambda: (self.photometry()))

        self.phot_add_par.clicked.connect(lambda: (self.add_phot_par()))
        self.phot_rm_par.clicked.connect(lambda: (self.rm_photo_par()))
        # self.phot_update_header_list.clicked.connect(lambda: (self.update_list_of_headers()))

        self.phot_add_to_header_to_extract.clicked.connect(lambda: (self.use_wanted_headers()))

        self.hext_add.clicked.connect(lambda: (self.add_files(self.hext_list)))
        self.hext_remove.clicked.connect(lambda: (self.rm_files(self.hext_list)))
        self.hext_list.clicked.connect(lambda: (self.show_headers_extractor()))
        self.hext_go.clicked.connect(lambda: (self.export_header()))

        self.hcalc_add.clicked.connect(lambda: (self.add_files(self.hcalc_list)))
        self.hcalc_remove.clicked.connect(lambda: (self.rm_files(self.hcalc_list)))
        self.hcalc_list.clicked.connect(lambda: (self.show_headers_calculator()))

        self.calib_image_list.installEventFilter(self)
        self.calib_bias_list.installEventFilter(self)
        self.calib_dark_list.installEventFilter(self)
        self.calib_flat_list.installEventFilter(self)
        self.align_list.installEventFilter(self)
        self.phot_list.installEventFilter(self)
        self.hedit_list.installEventFilter(self)
        self.hcalc_list.installEventFilter(self)
        self.hext_list.installEventFilter(self)
        self.cclean_list.installEventFilter(self)
        self.phot_coor_list.installEventFilter(self)

        self.display_align.canvas.fig.canvas.mpl_connect('motion_notify_event', self.align_onpick)
        self.display_phot.canvas.fig.canvas.mpl_connect('motion_notify_event', self.phot_onpick)

        header = self.hedit_header_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        header = self.hext_header_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        header = self.phot_par_list.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)


    def export_header(self):
        list_of_header_indices = self.gui_dev.list_of_selected_table(self.hext_header_table)
        if list_of_header_indices is not None:
            if len(list_of_header_indices) > 0:
                files = self.gui_dev.get_from_tree(self.hext_list)
                if files is not None:
                    if len(files) > 0:
                        out_file = self.gui_file.save_file(".dat", "headers.dat")
                        if out_file:
                            progress = QtWidgets.QProgressDialog("Extracting header from files...", "Abort", 0, len(files), self)
                            progress.setWindowModality(QtCore.Qt.WindowModal)
                            progress.setWindowTitle('MYRaf: Please Wait')
                            progress.setAutoClose(True)
                            ret = []
                            for it, file in enumerate(files, start=1):
                                progress.setLabelText("Extracting header from {}".format(file))
                                file_header = ["#File"]
                                line = [file]
                                for header_index in list_of_header_indices:

                                    if progress.wasCanceled():
                                        progress.setLabelText("ABORT!")
                                        break

                                    wanted_header_field = self.hext_header_table.item(header_index, 0).text()
                                    wanted_header = self.fts.header(file, wanted_header_field)
                                    line.append(str(wanted_header))
                                    file_header.append(str(wanted_header_field))

                                ret.append(line)
                                progress.setValue(it)

                            ret.insert(0, file_header)
                            self.fop.write_list(out_file, ret, dm="|")


    def show_headers_calculator(self):
        the_file = self.hcalc_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                headers = self.fts.header(the_file.toolTip(0))
                self.gui_dev.c_replace_list_con(self.hcalc_jd_time, [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_airmass_time, [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_airmass_ra, [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_airmass_dec, [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_time_time, [str("{}->{}".format(i[0], i[1])) for i in headers])

    def show_headers_extractor(self):
        the_file = self.hext_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                headers = self.fts.header(the_file.toolTip(0))
                self.gui_dev.replace_table(self.hext_header_table, headers)

    def plot_coordinates(self, selected=True):
        if selected:
            coords = self.gui_dev.list_of_selected(self.phot_coor_list)
        else:
            coords = self.gui_dev.list_of_list(self.phot_coor_list)

        if not coords == []:
            for it, coord in enumerate(coords):
                the_coord = tuple(map(float, coord.split(",")))
                circ = Circle(the_coord, radius=30, edgecolor="#00FFFF", facecolor="#00FFFF")
                self.display_phot.canvas.fig.gca().add_artist(circ)
                self.display_phot.canvas.fig.gca().annotate("s{}".format(str(it)),
                                                            xy=the_coord, color="#00FFFF", fontsize=10)
            self.display_phot.canvas.draw()
        else:
            self.logger.warning("No coordinates to plot")
            QtWidgets.QMessageBox.critical(self, "MYRaf Error", "Please add coordinate(s)")

        self.reload_log()

    def use_wanted_headers(self):
        available_headers = self.gui_dev.list_of_selected(self.phot_header_list)
        wanted_headers = self.gui_dev.list_of_list(self.phot_header_to_exract)
        if len(available_headers) > 0:
            for available_header in available_headers:
                if available_header not in wanted_headers:
                    self.gui_dev.add(self.phot_header_to_exract, [available_header])
        else:
            self.logger.warning("No header(s) file was. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning",
                                          "No header(s) was selected. Please select at least one header")

    def update_list_of_headers(self):
        the_file = self.phot_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                headers = self.fts.header(the_file.toolTip(0), field="*")
                self.gui_dev.replace_list_con(self.phot_header_list, [str(i[0]) for i in headers])
        else:
            self.logger.warning("No data file was selected. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning",
                                          "No data file was selected. Please select a file in Photometry tab.")

    def rm_photo_par(self):
        self.gui_dev.remove_from_table(self.phot_par_list)

    def photometry(self):
        files = self.gui_dev.get_from_tree(self.phot_list)
        if len(files) > 0:
            coordinates = self.gui_dev.list_of_list(self.phot_coor_list)
            if len(coordinates) > 0:
                phot_pars = self.gui_dev.list_of_table(self.phot_par_list)
                if phot_pars is not None:
                    if len(phot_pars) > 0:
                        res_data = self.gui_file.save_file(file_type="my (*.my)", name="res")
                        if res_data is not None:
                            progress = QtWidgets.QProgressDialog("Photometry...", "Abort", 0, len(files), self)
                            progress.setWindowModality(QtCore.Qt.WindowModal)
                            progress.setWindowTitle('MYRaf: Please Wait')
                            progress.setAutoClose(True)
                            data = []
                            for it, file in enumerate(files, start=1):
                                progress.setLabelText("Photometry of {}".format(file))
                                if progress.wasCanceled():
                                    progress.setLabelText("ABORT!")
                                    break
                                for coordinate in coordinates:
                                    for phot_par in phot_pars:
                                        header_line = ["#File_name", "Coordinate", "Aperture",
                                                       "Annulus", "Dannulus", "ZMag", "MAG", "MERR"]
                                        data_line = []

                                        pn, fn = self.fop.get_base_name(file)
                                        mag_file = "{}/{}.mag".format(self.fop.tmp_dir, fn)

                                        if self.fop.is_file(mag_file):
                                            self.fop.rm(mag_file)

                                        data_line.append(file)
                                        data_line.append(coordinate)
                                        for pp in phot_par:
                                            data_line.append(pp)

                                        self.iraf.phot(file, mag_file, [coordinate],
                                                       phot_par[0], annulus=phot_par[1],
                                                       dannulus=phot_par[2], zmag=phot_par[3])
                                        phot_res = self.iraf.textdump(mag_file)[0]
                                        data_line.append(phot_res[1])
                                        data_line.append(phot_res[2])
                                        wanted_headers = self.gui_dev.list_of_list(self.phot_header_to_exract)
                                        if len(wanted_headers) > 0:
                                            for wanted_header in wanted_headers:
                                                use_header = self.fts.header(file, wanted_header)
                                                header_line.append(wanted_header)
                                                data_line.append(str(use_header))
                                        if not (phot_res[0] == "INDEF" or  phot_res[1] == "INDEF"):
                                            data.append(data_line)

                                        if self.fop.is_file(mag_file):
                                            self.fop.rm(mag_file)

                                    progress.setValue(it)

                            data.insert(0, header_line)
                            self.fop.write_list(res_data, data, dm="|")
                        else:
                            self.logger.warning("phot canceled by user.")

                else:
                    self.logger.warning("No photpars was given. Nothing to do.")
                    QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No photpars was given. Nothing to do.")
            else:
                self.logger.warning("No coordinate file was given. Nothing to do.")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No coordinate was given. Nothing to do.")
        else:
            self.logger.warning("No data file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")

    def add_phot_par(self):
        aperture = self.phot_aperture.value()
        annulus = self.phot_annulus.value()
        if aperture < annulus:
            dannulus = self.phot_dannulus.value()
            zmag = self.phot_zmag.value()
            self.gui_dev.add_table(self.phot_par_list, [[aperture, annulus, dannulus, zmag]])
        else:
            self.logger.warning("Annulus must be bigger than Aperture.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Annulus must be bigger than Aperture.")

    def cosmin_clean(self):
        files = self.gui_dev.get_from_tree(self.cclean_list)
        if len(files) > 0:
            sigclip = self.ccleaner_sigclip.value()
            sigfrac = self.ccleaner_sigfrac.value()
            objlim = self.ccleaner_objlim.value()
            gain = self.ccleaner_gain.value()
            readnoise = self.ccleaner_readnoise.value()
            satlevel = self.ccleaner_satlevel.value()
            pssl = self.ccleaner_pssl.value()
            iteration = self.ccleaner_iteration.value()
            sepmed = self.ccleaner_sepmed.isChecked()
            cleantype = self.ccleaner_cleantype.currentText()
            fsmode = self.ccleaner_fsmode.currentText()
            psfmodel = self.ccleaner_psfmodel.currentText()
            psffwhm = self.ccleaner_psffwhm.value()
            psfsize = self.ccleaner_psfsize.value()

            out_folder = self.gui_file.save_directory()
            if out_folder:
                progress = QtWidgets.QProgressDialog("Calibrating files...", "Abort", 0, len(files), self)
                progress.setWindowModality(QtCore.Qt.WindowModal)
                progress.setWindowTitle('MYRaf: Please Wait')
                progress.setAutoClose(True)
                for it, file in enumerate(files, start=1):
                    _, fn = self.fop.get_base_name(file)
                    progress.setLabelText("Calibrating {}".format(file))

                    if progress.wasCanceled():
                        progress.setLabelText("ABORT!")
                        break

                    output = "{}/{}".format(out_folder, fn)
                    self.fts.cosmic_cleaner(file, output, sigclip=sigclip, sigfrac=sigfrac, objlim=objlim, gain=gain,
                                            readnoise=readnoise, satlevel=satlevel, pssl=pssl, iteration=iteration,
                                            sepmed=sepmed, cleantype=cleantype, fsmode=fsmode, psfmodel=psfmodel,
                                            psffwhm=psffwhm, psfsize=psfsize)

                    self.fts.update_header(output, "MYCClean", "Cosmic Clean done by MYRaf V3")

                    progress.setValue(it)

        else:
            self.logger.warning("No data file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")

    def calibration(self):
        data_files = self.gui_dev.get_from_tree(self.calib_image_list)
        if len(data_files) > 0:
            zero_files = self.gui_dev.get_from_tree(self.calib_bias_list)
            if len(zero_files) > 0:
                zero_combine = self.zero_combine.currentText()
                zero_reject = self.zero_reject.currentText()
                zero_file = "{}/myraf_zero.fits".format(self.fop.tmp_dir)
                try:
                    self.iraf.zerocombine(zero_files, zero_file, method=zero_combine, rejection=zero_reject)
                except:
                    self.logger.warning("Zerocombine failed. Zerocorrection will be skipped.")
                    zero_file = None
            else:
                self.logger.warning("No zero file. Zerocorrection will be skipped.")
                zero_file = None

            dark_files = self.gui_dev.get_from_tree(self.calib_dark_list)
            if len(dark_files) > 0:

                dark_combine = self.dark_combine.currentText()
                dark_reject = self.dark_reject.currentText()
                dark_scale = self.dark_scale.currentText()
                dark_file = "{}/myraf_dark.fits".format(self.fop.tmp_dir)
                try:
                    self.iraf.darkcombine(dark_files, dark_file, method=dark_combine,
                                          rejection=dark_reject, scale=dark_scale)
                except:
                    self.logger.warning("Darkcombine failed. Darkcorrection will be skipped.")
                    dark_file = None
            else:
                self.logger.warning("No dark file. Darkcorrection will be skipped.")
                dark_file = None

            flat_files = self.gui_dev.get_from_tree(self.calib_flat_list)
            if len(flat_files) > 0:
                flat_combine = self.flat_combine.currentText()
                flat_reject = self.flat_reject.currentText()
                flat_file = "{}/myraf_flat.fits".format(self.fop.tmp_dir)
                try:
                    self.iraf.flatcombine(flat_files, flat_file, method=flat_combine, rejection=flat_reject)
                except:
                    self.logger.warning("Flatcombine failed. Flatcorrection will be skipped.")
                    flat_file = None
            else:
                self.logger.warning("No flat file. Flatcorrection will be skipped.")
                flat_file = None

            if flat_file is None and dark_file is None and zero_file is None:
                self.logger.warning("No operation available")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No operation available. Nothing to do.")
            else:
                out_folder = self.gui_file.save_directory()
                if out_folder:
                    progress = QtWidgets.QProgressDialog("Calibrating files...", "Abort", 0, len(data_files), self)
                    progress.setWindowModality(QtCore.Qt.WindowModal)
                    progress.setWindowTitle('MYRaf: Please Wait')
                    progress.setAutoClose(True)
                    for it, data_file in enumerate(data_files, start=1):
                        _, fn = self.fop.get_base_name(data_file)
                        progress.setLabelText("Calibrating {}".format(data_file))

                        if progress.wasCanceled():
                            progress.setLabelText("ABORT!")
                            break

                        output = "{}/{}".format(out_folder, fn)
                        self.iraf.ccdproc(data_file, output, zero_file, dark_file, flat_file)
                        self.fts.update_header(output, "MYCcdp", "ccdproc done by MYRaf V3")

                        progress.setValue(it)
                else:
                    self.logger.warning("ccdproc canceled by user.")
        else:
            self.logger.warning("No data file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")

    def export_flat(self):
        files = self.gui_dev.get_from_tree(self.calib_flat_list)
        if len(files) > 0:
            out_file = self.gui_file.save_file()
            if out_file:
                flat_combine = self.flat_combine.currentText()
                flat_reject = self.flat_reject.currentText()
                self.iraf.flatcombine(files, out_file, method=flat_combine, rejection=flat_reject)
                self.fts.update_header(out_file, "MYFlat", "Flatcombine done by MYRaf V3")
            else:
                self.logger.warning("Darkcombine canceled by user.")
        else:
            self.logger.warning("No file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was found. Nothing to do.")

    def export_dark(self):
        files = self.gui_dev.get_from_tree(self.calib_dark_list)
        if len(files) > 0:
            out_file = self.gui_file.save_file()
            if out_file:
                dark_combine = self.dark_combine.currentText()
                dark_reject = self.dark_reject.currentText()
                dark_scale = self.dark_scale.currentText()
                self.iraf.darkcombine(files, out_file, method=dark_combine, rejection=dark_reject, scale=dark_scale)
                self.fts.update_header(out_file, "MYDark", "Darkcombine done by MYRaf V3")
            else:
                self.logger.warning("Darkcombine canceled by user.")
        else:
            self.logger.warning("No file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was found. Nothing to do.")

    def export_bias(self):
        files = self.gui_dev.get_from_tree(self.calib_bias_list)
        if len(files) > 0:
            out_file = self.gui_file.save_file()
            if out_file:
                zero_combine = self.zero_combine.currentText()
                zero_reject = self.zero_reject.currentText()
                self.iraf.zerocombine(files, out_file, method=zero_combine, rejection=zero_reject)
                self.fts.update_header(out_file, "MYZero", "Zerocombine done by MYRaf V3")
            else:
                self.logger.warning("Zerocombine canceled by user.")
        else:
            self.logger.warning("No file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was found. Nothing to do.")

    def add_header(self):
        field_name = self.hedit_field.text()
        files = self.gui_dev.get_from_tree(self.hedit_list)

        if len(files) > 0:
            if not field_name == "":
                progress = QtWidgets.QProgressDialog("Adding Header...", "Abort", 0, len(files), self)
                progress.setWindowModality(QtCore.Qt.WindowModal)
                progress.setWindowTitle('MYRaf: Please Wait')
                progress.setAutoClose(True)

                for it, file in enumerate(files, start=1):
                    progress.setLabelText("Adding header({}) to {}".format(field_name, file))

                    if progress.wasCanceled():
                        progress.setLabelText("ABORT!")
                        break
                    if self.hedit_isvaluefromheader.isChecked():
                        seek_field = self.hedit_valuefromheader.currentText()
                        value = self.fts.header(file, seek_field.split("->")[0])
                        if value is not None:
                            self.fts.update_header(file, field_name, value)
                        else:
                            self.logger.warning("No value was found. Skipping file {}".format(file))
                    else:
                        value = self.hedit_value.text()
                        if not value == "":
                            self.fts.update_header(file, field_name, value)
                        else:
                            self.logger.warning("No value was given. Skipping file {}".format(file))
                    progress.setValue(it)

                self.show_headers()

            else:
                self.logger.warning("No field was given. Nothing to do.")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No field was given. Nothing to do.")
        else:
            self.logger.warning("No file was found. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was found. Nothing to do.")

    def rm_header(self):
        field_name = self.hedit_field.text()
        files = self.gui_dev.get_from_tree(self.hedit_list)
        if len(files) > 0:
            if not field_name == "":
                progress = QtWidgets.QProgressDialog("Removing Header...", "Abort", 0, len(files), self)
                progress.setWindowModality(QtCore.Qt.WindowModal)
                progress.setWindowTitle('MYRaf: Please Wait')
                progress.setAutoClose(True)

                for it, file in enumerate(files, start=1):
                    progress.setLabelText("Removing header({}) from {}".format(field_name, file))

                    if progress.wasCanceled():
                        progress.setLabelText("ABORT!")
                        break

                    self.fts.delete_header(file, field_name)
                    progress.setValue(it)

                self.show_headers()
            else:
                self.logger.warning("No field was given. Nothing to do.")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No field was given. Nothing to do.")
        else:
            self.logger.warning("No file was found. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was found. Nothing to do.")

    def toggle_header(self):
        self.hedit_value.setEnabled(not self.hedit_isvaluefromheader.isChecked())
        self.hedit_valuefromheader.setEnabled(self.hedit_isvaluefromheader.isChecked())

    def header_selected(self):
        self.hedit_field.setText(self.hedit_header_table.item(self.hedit_header_table.currentItem().row(), 0).text())
        self.hedit_value.setText(self.hedit_header_table.item(self.hedit_header_table.currentItem().row(), 1).text())

    def show_headers(self):
        the_file = self.hedit_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                headers = self.fts.header(the_file.toolTip(0))
                self.gui_dev.replace_table(self.hedit_header_table, headers)
                self.gui_dev.c_replace_list_con(self.hedit_valuefromheader,
                                                ["{}->{}".format(i[0], i[1]) for i in headers])

    def get_coordinate_phot(self, event):
        try:
            x, y = self.phot_display.get_xy()
            if self.phot_display.get_data() is not None:
                self.gui_dev.add(self.phot_coor_list, ["{:0.2f},{:0.2f}".format(x, y)])
            else:
                self.logger.info("Coordinate({:0.2f},{:0.2f}) out of boundary".format(x, y))
        except Exception as e:
            self.logger.error(e)

    def align_onpick(self, event):
        try:
            x, y = self.align_display.get_xy()
            val = self.align_display.get_data()
            self.info_align.setText("X: {:0.2f}, Y: {:0.2f}, Val: {:0.2f}".format(x, y, val))
        except Exception as e:
            self.logger.error(e)

    def phot_onpick(self, event):
        try:
            x, y = self.phot_display.get_xy()
            val = self.phot_display.get_data()
            self.info_phot.setText("X: {:0.2f}, Y: {:0.2f}, Val: {:0.2f}".format(x, y, val))
        except Exception as e:
            self.logger.error(e)

    def display(self, file_device, display_devide):
        the_file = file_device.currentItem()
        if the_file.child(0) is not None:
            display_devide.load(the_file.toolTip(0))

        self.reload_log()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.calib_image_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.calib_image_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.calib_image_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.calib_image_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.calib_image_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.calib_bias_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.calib_bias_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.calib_bias_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.calib_bias_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.calib_bias_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.calib_dark_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.calib_dark_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.calib_dark_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.calib_dark_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.calib_dark_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.calib_flat_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.calib_flat_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.calib_flat_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.calib_flat_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.calib_flat_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.align_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.align_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.align_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.align_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.align_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.phot_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.phot_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.phot_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.phot_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.phot_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.hext_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.hext_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.hext_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.hext_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.hext_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.hcalc_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.hcalc_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.hcalc_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.hcalc_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.hcalc_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.hedit_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.hedit_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.hedit_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.hedit_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.hedit_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.cclean_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.cclean_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.cclean_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.cclean_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.cclean_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.phot_coor_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Remove', lambda: (self.gui_dev.rm(self.phot_coor_list)))
            menu.addSeparator()
            show_all = menu.addAction('Show All', lambda: (self.plot_coordinates(selected=False)))
            show_selected = menu.addAction('Show Selected', lambda: (self.plot_coordinates(selected=True)))
            show_all.setEnabled(len(self.gui_dev.list_of_list(self.phot_coor_list)) > 0)
            show_selected.setEnabled(len(self.gui_dev.list_of_list(self.phot_coor_list)) > 0)

            menu.exec_(event.globalPos())
            return True

        return super(MainWindow, self).eventFilter(source, event)

    def rm_files(self, device):
        self.gui_dev.rm_from_tree(device)
        self.reload_log()

    def add_files(self, device):
        self.logger.info("Getting File List")
        files = self.gui_file.get_files()
        if files:
            progress = QtWidgets.QProgressDialog("Adding files...", "Abort", 0, len(files), self)
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setWindowTitle('MYRaf: Please Wait')
            progress.setAutoClose(True)

            images_to_add = []
            for it, file in enumerate(files, start=1):
                progress.setLabelText("Adding {}".format(file))

                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                if self.fts.check(file):
                    file_type = str(self.fts.header(file, "IMAGETYP"))
                    stats = self.fts.stats(file)
                    images_to_add.append([file, file_type, stats])
                progress.setValue(it)

            if len(images_to_add) > 0:
                self.logger.info("Add File List to View")
                self.gui_dev.add_to_tree(images_to_add, device)

            progress.close()
        self.reload_log()

    def reload_log(self):
        pass


def main():
    parser = argparse.ArgumentParser(description='MYRaf V3 Beta')
    parser.add_argument("--logger", "-ll", default=50, type=int,
                        help="Logger level: CRITICAL=50, ERROR=40, WARNING=30, INFO=20, DEBUG=10, NOTSET=0")
    # help="An integer of Logger level: CRITICAL=50, ERROR=40, WARNING=30, INFO=20, DEBUG=10, NOTSET=0"
    parser.add_argument("--logfile", "-lf", default=None, type=str, help="Path to log file")
    args = parser.parse_args()

    app = QtWidgets.QApplication(argv)
    window = MainWindow(logger_level=args.logger, log_file=args.logfile)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
