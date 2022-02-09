# -*- coding: utf-8 -*-
"""
@author: msh, yk
"""

try:
    from matplotlib.backend_bases import MouseButton
    # from ginga.util import ap_region
    from regions import PixCoord, CirclePixelRegion, CircleAnnulusPixelRegion
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

    # from sklearn import linear_model
    import mplcursors
    from imexam.imexamine import Imexamine
    from astropy.io import ascii
    import numpy as np
    from astropy.time import Time, TimeDelta
    import time

except Exception as e:
    print(e)
    exit(0)


class MainWindow(QtWidgets.QMainWindow, myraf.Ui_MainWindow):
    def __init__(self, parent=None, logger_level="DEBUG", log_file=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.flags = QtCore.Qt.Window
        self.setWindowFlags(self.flags)

        self.logger_level = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0}

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
        self.atm = analyse.Astronomy.Time(self.logger)
        self.coords = analyse.Astronomy.Coordinates(self.logger)

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
        self.phot_coor_remove.clicked.connect(lambda: (self.gui_dev.rm(self.phot_coor_list)))
        self.display_phot.canvas.fig.canvas.mpl_connect('button_press_event', self.get_coordinate_phot)

        # self.phot_add.clicked.connect(lambda: (self.add_files(self.update_list_of_headers)))

        self.hedit_remove_field.clicked.connect(lambda: (self.rm_header()))
        self.hedit_add_field.clicked.connect(lambda: (self.add_header()))

        self.align_list.clicked.connect(lambda: (self.display(self.align_list, self.align_display),
                                                 self.display_coords_align()))
        self.phot_list.clicked.connect(lambda: (self.display(self.phot_list, self.phot_display)))
        self.phot_list.clicked.connect(lambda: (self.update_list_of_headers()))
        self.phot_coor_find_sources.clicked.connect(lambda: (self.source_detect()))

        self.align_go.clicked.connect(lambda: (self.align()))

        self.hedit_list.clicked.connect(lambda: (self.show_headers()))
        self.hedit_header_table.clicked.connect(lambda: (self.header_selected()))

        self.phot_go.clicked.connect(lambda: (self.photometry()))

        self.phot_add_par.clicked.connect(lambda: (self.add_phot_par()))
        self.phot_rm_par.clicked.connect(lambda: (self.rm_photo_par()))
        # self.phot_update_header_list.clicked.connect(lambda: (self.update_list_of_headers()))

        self.phot_add_to_header_to_extract.clicked.connect(lambda: (self.use_wanted_headers()))
        self.phot_remobe_from_header_to_extract.clicked.connect(lambda: (self.gui_dev.rm(self.phot_header_to_exract)))

        self.hext_add.clicked.connect(lambda: (self.add_files(self.hext_list)))
        self.hext_remove.clicked.connect(lambda: (self.rm_files(self.hext_list)))
        self.hext_list.clicked.connect(lambda: (self.show_headers_extractor()))
        self.hext_go.clicked.connect(lambda: (self.export_header()))

        self.hcalc_add.clicked.connect(lambda: (self.add_files(self.hcalc_list)))
        self.hcalc_remove.clicked.connect(lambda: (self.rm_files(self.hcalc_list)))
        self.hcalc_list.clicked.connect(lambda: (self.show_headers_calculator()))

        self.observatory_list.clicked.connect(lambda: (self.show_observat()))

        self.observatory_add.clicked.connect(lambda: (self.add_observatory()))
        self.observatory_remove.clicked.connect(lambda: (self.remove_observatory()))
        self.observatory_reload.clicked.connect(lambda: (self.all_observatioes_list()))

        self.hcalc_go.clicked.connect(lambda: (self.hcalc()))

        # self.save_the_settings() remove_settings_profile
        self.settings_save.clicked.connect(lambda: (self.save_the_settings()))
        self.settings_remove.clicked.connect(lambda: (self.remove_settings_profile()))

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
        self.display_align.canvas.fig.canvas.mpl_connect('button_press_event', self.get_coordinate_align)

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
        self.settings_profile_selector.currentTextChanged.connect(lambda: (self.setting_profile_changed()))

        # Graph section
        self.graph_get_file.clicked.connect(lambda: (self.load_phot_result()))
        self.graph_plot.clicked.connect(lambda: (self.plot_phot_result()))
        self.graph_color_picker.clicked.connect(lambda: (self.color_picker()))
        self.clear_plot_btn.clicked.connect(lambda: (self.clear_plot()))
        self.display_phot.canvas.fig.canvas.mpl_connect('key_press_event', self.plot_imexam)

        self.observatory_file = "observatories.obs"
        self.settings_file = "settings.set"
        self.all_observatioes_list()
        self.load_list_of_settngs()

    def hcalc(self):
        files = self.gui_dev.get_from_tree(self.hcalc_list)
        if files is not None:
            if len(files) > 0:
                if self.hcalc_jd.isChecked() or self.hcalc_airmass.isChecked() or self.hcalc_imexamine.isChecked() or \
                        self.hcalc_time.isChecked():
                    prefix = self.hcalc_prefix.text()
                    progress = QtWidgets.QProgressDialog("Header Calculator...", "Abort", 0, len(files), self)
                    progress.setWindowModality(QtCore.Qt.WindowModal)
                    progress.setWindowTitle('MYRaf: Please Wait')

                    for it, file in enumerate(files, start=1):

                        if progress.wasCanceled():
                            progress.setLabelText("ABORT!")
                            break

                        if self.hcalc_jd.isChecked():
                            progress.setLabelText("Calculating jd for file{}".format(file))
                            header_selcted = self.hcalc_jd_time.currentText()
                            if not header_selcted == "":
                                time_header = header_selcted.split("->")[0]
                                time_in_header = self.fts.header(file, time_header)
                                if time_in_header is not None:
                                    the_time = self.atm.str_to_time(time_in_header)
                                    jd = self.atm.jd(the_time)
                                    if jd is not None:
                                        self.fts.update_header(file, "{}JD".format(prefix), str(jd))

                                    if self.hcalc_hjd.isChecked():
                                        header_ra = self.hcalc_hjd_ra.currentText()
                                        header_dec = self.hcalc_hjd_ra.currentText()
                                        header_obs = self.hcalc_hjd_ra.currentText()
                                        if not (header_ra == "" and header_dec == "" and header_obs == ""):
                                            wanted_ra = header_ra.split("->")[0]
                                            wanted_dec = header_dec.split("->")[0]
                                            ra_in_header = self.fts.header(file, wanted_ra)
                                            dec_in_header = self.fts.header(file, wanted_dec)
                                            bjd = self.atm.jd2bjd(jd, ra_in_header, dec_in_header)
                                            hjd = self.atm.jd2hjd(jd, ra_in_header, dec_in_header)
                                            self.fts.update_header(file, "{}HJD".format(prefix), str(hjd))
                                            self.fts.update_header(file, "{}BJD".format(prefix), str(bjd))

                        if self.hcalc_airmass.isChecked():
                            progress.setLabelText("Calculating airmass for file{}".format(file))
                            all_observatories = self.fop.read_json(self.observatory_file)
                            if all_observatories is not None:
                                the_observatory = all_observatories[self.hcalc_airmass_observatory.currentText()]
                                long = the_observatory["longitude"]
                                lati = the_observatory["latitude"]
                                alti = the_observatory["altitude"]
                                if long is not None and lati is not None and alti is not None:
                                    ra_inheader = self.hcalc_airmass_ra.currentText()
                                    dec_inheader = self.hcalc_airmass_dec.currentText()
                                    time_inheader = self.hcalc_airmass_time.currentText()
                                    if not ra_inheader == "":
                                        if not dec_inheader == "":
                                            if not time_inheader == "":
                                                wanted_ra = ra_inheader.split("->")[0]
                                                wanted_dec = dec_inheader.split("->")[0]
                                                wanted_time = time_inheader.split("->")[0]

                                                ra = self.fts.header(file, wanted_ra)
                                                dec = self.fts.header(file, wanted_dec)
                                                time = self.fts.header(file, wanted_time)
                                                if ra is not None and dec is not None and time is not None:
                                                    use_time = self.atm.str_to_time(time)
                                                    use_long = self.coords.create_angle("{} degree".format(long))
                                                    use_lati = self.coords.create_angle("{} degree".format(lati))
                                                    use_alti = float(alti)

                                                    use_ra = self.coords.create_angle("{} hour".format(ra))
                                                    use_dec = self.coords.create_angle("{} degree".format(dec))

                                                    site = analyse.Astronomy.Site(self.logger,
                                                                                  use_lati, use_long, use_alti)
                                                    object = analyse.Astronomy.Obj(self.logger,
                                                                                   use_ra, use_dec)

                                                    use_site = site.create()
                                                    use_object = object.create()
                                                    if use_site is not None and use_object is not None and use_time is not None:
                                                        alt_az = site.altaz(use_site, use_object, use_time)
                                                        self.fts.update_header(file, "{}secz".format(prefix),
                                                                               str(alt_az.secz))

                        if self.hcalc_imexamine.isChecked():
                            progress.setLabelText("Calculating imexamine for file{}".format(file))
                            stats = self.fts.stats(file)
                            if stats is not None:
                                if self.hcalc_imexamine_mean.isChecked():
                                    self.fts.update_header(file, "{}mean".format(prefix), str(stats["Mean"]))

                                if self.hcalc_imexamine_median.isChecked():
                                    self.fts.update_header(file, "{}median".format(prefix), str(stats["Median"]))

                                if self.hcalc_imexamine_stdv.isChecked():
                                    self.fts.update_header(file, "{}stdv".format(prefix), str(stats["Stdev"]))

                                if self.hcalc_imexamine_min.isChecked():
                                    self.fts.update_header(file, "{}min".format(prefix), str(stats["Min"]))

                                if self.hcalc_imexamine_max.isChecked():
                                    self.fts.update_header(file, "{}max".format(prefix), str(stats["Max"]))

                        if self.hcalc_time.isChecked():
                            progress.setLabelText("Calculating timediff for file{}".format(file))
                            header_selcted = self.hcalc_time_time.currentText()
                            if not header_selcted == "":
                                wanted_header = header_selcted.split("->")[0]
                                time_in_header = self.fts.header(file, wanted_header)
                                if time_in_header is not None:
                                    time_amount = self.hcalc_time_value.value()
                                    time_type = self.hcalc_time_valueType.currentText()
                                    the_time = self.atm.str_to_time(time_in_header)
                                    new_time = self.atm.time_diff(the_time, time_offset=time_amount,
                                                                  offset_type=time_type)
                                    if new_time is not None:
                                        self.fts.update_header(file, "{}time".format(prefix), str(new_time))

                        progress.setValue(it)

                else:
                    self.logger.warning("No operation was selected. Nothing to do.")
                    QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No operation was selected. Nothing to do.")

            else:
                self.logger.warning("No file was given. Nothing to do.")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")
        else:
            self.logger.warning("No file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")

    def remove_observatory(self):
        the_observat_name = self.observatory_list.currentItem().text()
        if the_observat_name is not None:
            observats = self.fop.read_json(self.observatory_file)
            if observats is not None:
                del observats[the_observat_name]
                self.fop.write_json(self.observatory_file, observats)
                self.all_observatioes_list()
            else:
                self.logger.warning("Can't find observatory file.")

    def add_observatory(self):
        abb = self.observatory_abbreviation.text()
        name = self.observatory_name.text()
        longitude = self.observatory_longitude.text()
        latitude = self.observatory_latitude.text()
        altitude = self.observatory_altitude.text()
        timezone = self.observatory_timezone.value()
        commend = self.observatory_commend.toPlainText()
        if abb != "" or name != "" or longitude != "" or latitude != "" or altitude != "":
            the_observat = {"observatory": abb, "name": name, "longitude": longitude, "latitude": latitude,
                            "altitude": altitude, "timezone": timezone, "commendation": commend}
            observats = self.fop.read_json(self.observatory_file)
            if observats is not None:
                if abb in observats.keys():
                    self.logger.warning("Observatory({}) already exist. Updating.".format(abb))

                observats[abb] = the_observat
                self.fop.write_json(self.observatory_file, observats)
                self.all_observatioes_list()
            else:
                self.logger.warning("Can't find observatory file.")

    def show_observat(self):
        the_observat_name = self.observatory_list.currentItem().text()
        if the_observat_name is not None:
            observats = self.fop.read_json(self.observatory_file)
            if observats is not None:
                try:
                    the_observat = observats[the_observat_name]
                    self.observatory_abbreviation.setText(the_observat["observatory"])
                    self.observatory_name.setText(the_observat["name"])
                    self.observatory_longitude.setText(the_observat["longitude"])
                    self.observatory_latitude.setText(the_observat["latitude"])
                    self.observatory_altitude.setText(the_observat["altitude"])
                    self.observatory_timezone.setValue(float(the_observat["timezone"]))
                    self.observatory_commend.setPlainText(the_observat["commendation"])
                except Exception as e:
                    self.logger.error(e)

    def all_observatioes_list(self):
        observats = self.fop.read_json(self.observatory_file)
        if observats is not None:
            self.gui_dev.replace_list_con(self.observatory_list, observats.keys())
            self.gui_dev.c_replace_list_con(self.hcalc_airmass_observatory, observats.keys())
            self.observatory_list.sortItems()
        else:
            self.logger.warning("Can't find observatory file.")

    def get_coordinate_align(self, event):
        if event.button is MouseButton.LEFT:
            files = self.gui_dev.get_from_tree(self.align_list)
            the_file = self.align_list.currentItem()
            if the_file is not None:
                if the_file.child(0) is not None:
                    if self.align_display.get_data() is not None:
                        x, y = self.align_display.get_xy()
                        self.fts.update_header(the_file.toolTip(0), "my_align", "{}, {}".format(x, y))
                        current_index = self.align_list.currentIndex().row() + 1
                        new_row = current_index % (len(files))
                        self.align_list.setCurrentItem(self.align_list.topLevelItem(new_row))
                        if new_row == 0:
                            self.align_list.setCurrentItem(self.align_list.topLevelItem(new_row))
                            self.logger.warning("The whole list is done. Going back to top.")
                            QtWidgets.QMessageBox.warning(self, "MYRaf Warning",
                                                          "The whole list is done. Going back to top.")

                        self.display(self.align_list, self.align_display)
                        self.display_coords_align()

    def display_coords_align(self):
        the_file = self.align_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                header = self.fts.header(the_file.toolTip(0), "my_align")
                if header is not None:
                    the_coord = list(map(float, header.split(",")))
                    circ = Circle(the_coord, 10, edgecolor="#00FFFF", facecolor="none")
                    self.display_align.canvas.fig.gca().add_artist(circ)
                    circ.center = the_coord
                    self.display_align.canvas.fig.gca().annotate("REF", xy=the_coord, color="#00FFFF", fontsize=10)
                    self.display_align.canvas.draw()

    def source_detect(self):
        the_file = self.phot_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                if len(self.gui_dev.list_of_list(self.phot_coor_list)) > 0:
                    answ = self.gui_dev.ask_calcel(
                        "Do you want to replace coordinates. Click NO for adding coordinates")
                    if answ == "yes":
                        sources = self.fts.star_find(the_file.toolTip(0))
                        if sources is not None:
                            self.gui_dev.replace_list_con(self.phot_coor_list,
                                                          ["{:0.2f},{:0.2f}".format(i[0], i[1]) for i in sources])
                    elif answ == "no":
                        sources = self.fts.star_find(the_file.toolTip(0))
                        if sources is not None:
                            self.gui_dev.add(self.phot_coor_list,
                                             ["{:0.2f},{:0.2f}".format(i[0], i[1]) for i in sources])
                    else:
                        self.logger.warning("User canceled adding coordinates")
                else:
                    sources = self.fts.star_find(the_file.toolTip(0))
                    if sources is not None:
                        self.gui_dev.replace_list_con(self.phot_coor_list,
                                                      ["{:0.2f},{:0.2f}".format(i[0], i[1]) for i in sources])
        else:
            self.logger.warning("Reference Image no found.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Reference Image no found. Nothing to do.")

    def align(self):
        files = self.gui_dev.get_from_tree(self.align_list)
        if files is not None:
            if len(files) > 0:
                if self.align_isauto.isChecked():
                    the_file = self.align_list.currentItem()
                    if the_file is not None:
                        if the_file.child(0) is not None:
                            out_dir = self.gui_file.save_directory()
                            if out_dir:
                                progress = QtWidgets.QProgressDialog("Auto Aligning...", "Abort", 0, len(files), self)
                                progress.setWindowModality(QtCore.Qt.WindowModal)
                                progress.setWindowTitle('MYRaf: Please Wait')
                                for it, file in enumerate(files, start=1):
                                    progress.setLabelText("Aligning {}".format(file))

                                    if progress.wasCanceled():
                                        progress.setLabelText("ABORT!")
                                        break

                                    _, fn = self.fop.get_base_name(file)
                                    output = "{}/{}".format(out_dir, fn)
                                    alipy_align_info = self.fts.alipy_align(file, the_file.toolTip(0), output)
                                    if alipy_align_info is True:
                                        self.fts.update_header(file, "MYALI", "Aligned by MYRaf V3 (alipy)")
                                    elif alipy_align_info is False:
                                        align_info = self.fts.align(file, the_file.toolTip(0), output)
                                        if align_info is True:
                                            self.fts.update_header(file, "MYALI", "Aligned by MYRaf V3 (astroalign)")
                                        else:
                                            self.logger.error("Alignment is failed!")
                                    progress.setValue(it)
                        else:
                            self.logger.warning("Reference Image no found.")
                            QtWidgets.QMessageBox.warning(self,
                                                          "MYRaf Warning", "Reference Image no found. Nothing to do.")
                    else:
                        self.logger.warning("Reference Image no found.")
                        QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Reference Image no found. Nothing to do.")
                else:
                    the_file = self.align_list.currentItem()
                    if the_file is not None:
                        if the_file.child(0) is not None:
                            ref_coords = self.fts.header(the_file.toolTip(0), "my_align")
                            if ref_coords is not None:
                                ref_x, ref_y = list(map(float, ref_coords.split(",")))
                                out_dir = self.gui_file.save_directory()
                                if out_dir:
                                    progress = QtWidgets.QProgressDialog("Manual Aligning...", "Abort",
                                                                         0, len(files), self)
                                    progress.setWindowModality(QtCore.Qt.WindowModal)
                                    progress.setWindowTitle('MYRaf: Please Wait')
                                    for it, file in enumerate(files, start=1):
                                        progress.setLabelText("Aligning {}".format(file))

                                        if progress.wasCanceled():
                                            progress.setLabelText("ABORT!")
                                            break

                                        coords = self.fts.header(file, "my_align")
                                        if coords is not None:
                                            x, y = list(map(float, coords.split(",")))
                                            dx, dy = ref_x - x, ref_y - y
                                            _, fn = self.fop.get_base_name(file)
                                            out_file = "{}/{}".format(out_dir, fn)
                                            self.iraf.imshift(file, out_file, dx, dy)
                                        else:
                                            self.logger.warning(
                                                "File({}) has no my_align in header. Skipping.".format(file))

                                        progress.setValue(it)
                                else:
                                    self.logger.warning("align canceled by user.")
                            else:
                                self.logger.warning("Reference Image has not .")
                                QtWidgets.QMessageBox.warning(
                                    self, "MYRaf Warning",
                                    "Rerefence image has no my_align in header. Nothing to do.")
                        else:
                            self.logger.warning("Reference Image no found.")
                            QtWidgets.QMessageBox.warning(self, "MYRaf Warning",
                                                          "Rerefence image has no my_align in header. Nothing to do.")
                    else:
                        self.logger.warning("Reference Image no found.")
                        QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Reference Image no found. Nothing to do.")
            else:
                self.logger.warning("No file was given. Nothing to do.")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")
        else:
            self.logger.warning("No file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was given. Nothing to do.")

    def export_header(self):
        list_of_header_indices = self.gui_dev.list_of_selected_table(self.hext_header_table)
        if list_of_header_indices is not None:
            if len(list_of_header_indices) > 0:
                files = self.gui_dev.get_from_tree(self.hext_list)
                if files is not None:
                    if len(files) > 0:
                        out_file = self.gui_file.save_file(".dat", "headers.dat")
                        if not out_file == "":
                            progress = QtWidgets.QProgressDialog("Extracting header from files...",
                                                                 "Abort", 0, len(files), self)
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
                self.gui_dev.c_replace_list_con(self.hcalc_jd_time,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_airmass_time,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_airmass_ra,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_airmass_dec,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])
                self.gui_dev.c_replace_list_con(self.hcalc_time_time,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])

                self.gui_dev.c_replace_list_con(self.hcalc_hjd_ra,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])

                self.gui_dev.c_replace_list_con(self.hcalc_hjd_dec,
                                                [str("{}->{}".format(i[0], i[1])) for i in headers])

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
            # todo remove circles instead of reloading the whole display
            self.display(self.phot_list, self.phot_display)

            for it, coord in enumerate(coords):
                x, y = coord.split(",")
                aperture = self.phot_aperture.value()
                annulus = self.phot_annulus.value()
                dannulus = self.phot_dannulus.value()
                aperture_region = CirclePixelRegion(PixCoord(float(x), float(y)), radius=float(aperture))
                annulus_region = CircleAnnulusPixelRegion(PixCoord(float(x), float(y)),
                                                          inner_radius=annulus, outer_radius=annulus + dannulus)

                self.phot_display.fig.gca().add_artist(aperture_region.as_artist(lw=2))
                self.phot_display.fig.gca().add_artist(
                    annulus_region.as_artist(facecolor='none', edgecolor='red', lw=2))

            self.phot_display.fig.canvas.draw()
        else:
            self.logger.warning("No coordinates to plot")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Please add coordinate(s)")

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
                        res_data = self.gui_file.save_file(file_type="MYRaf result file (*.my, *.csv, *.txt)", name="res.my")
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
                                # for coordinate in coordinates:
                                header_line = ["#File_name", "Aperture",
                                               "Annulus", "Dannulus", "ZMag", "Coordinate", "MAG", "MERR", "FLUX", "AREA", "STDEV", "NSKY"]
                                wanted_headers = self.gui_dev.list_of_list(self.phot_header_to_exract)
                                if len(wanted_headers) > 0:
                                    for wanted_header in wanted_headers:
                                        header_line.append(wanted_header)

                                for phot_par in phot_pars:
                                    pn, fn = self.fop.get_base_name(file)
                                    mag_file = "{}/{}.mag".format(self.fop.tmp_dir, fn)

                                    if self.fop.is_file(mag_file):
                                        self.fop.rm(mag_file)

                                    self.iraf.phot(file, mag_file, coordinates,
                                                   phot_par[0], annulus=phot_par[1],
                                                   dannulus=phot_par[2], zmag=phot_par[3])
                                    all_header_res = []
                                    if len(wanted_headers) > 0:
                                        for wanted_header in wanted_headers:
                                            use_header = self.fts.header(file, wanted_header)
                                            all_header_res.append(str(use_header))

                                    phot_ress = self.iraf.textdump(mag_file)

                                    for phot_res in phot_ress:
                                        data_line = []
                                        data_line.append(file)
                                        for pp in phot_par:
                                            data_line.append(pp)
                                        data_line.append(coordinates[int(phot_res[0]) - 1])
                                        data_line.append(phot_res[1])
                                        data_line.append(phot_res[2])
                                        data_line.append(phot_res[3])
                                        data_line.append(phot_res[4])
                                        data_line.append(phot_res[5])
                                        data_line.append(phot_res[6])
                                        for header_res in all_header_res:
                                            data_line.append(header_res)

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
            if not out_file == "":
                flat_combine = self.flat_combine.currentText()
                flat_reject = self.flat_reject.currentText()
                self.iraf.flatcombine(files, out_file, method=flat_combine, rejection=flat_reject)
                self.fts.update_header(out_file, "MYFlat", "Flatcombine done by MYRaf V3")
            else:
                self.logger.warning("Flatcombine canceled by user.")
        else:
            self.logger.warning("No file was given. Nothing to do.")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No file was found. Nothing to do.")

    def export_dark(self):
        files = self.gui_dev.get_from_tree(self.calib_dark_list)
        if len(files) > 0:
            out_file = self.gui_file.save_file()
            if not out_file == "":
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
            if not out_file == "":
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
            if event.button is MouseButton.LEFT:
                x, y = self.phot_display.get_xy()
                if self.phot_display.get_data() is not None:
                    self.gui_dev.add(self.phot_coor_list, ["{:0.2f},{:0.2f}".format(x, y)])
                else:
                    self.logger.info("Coordinate({:0.2f},{:0.2f}) out of boundary".format(x, y))
        except Exception as e:
            self.logger.error(e)

    def align_onpick(self, event):
        x, y = self.align_display.get_xy()
        val = self.align_display.get_data()
        self.info_align.setText("X: {:0.2f}, Y: {:0.2f}, Val: {:0.2f}".format(x, y, val))

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

            menu.addSeparator()
            exportation = menu.addAction('Export', lambda: (self.export_coords()))
            importation = menu.addAction('Import', lambda: (self.import_coords()))
            importation.setEnabled(self.phot_display.get_data() is not None)
            exportation.setEnabled(len(self.gui_dev.list_of_list(self.phot_coor_list)) > 0)

            menu.exec_(event.globalPos())
            return True

        return super(MainWindow, self).eventFilter(source, event)

    def export_coords(self):
        data = self.gui_dev.list_of_list(self.phot_coor_list)
        if len(data) > 0:
            out_file = self.gui_file.save_file(file_type="Coordinates File (*.coo)", name="coordinates.coo")
            if not out_file == "":
                self.fop.write_list(out_file, data)
            else:
                self.logger.warning("saving canceled by user.")
        else:
            self.logger.warning("No coordinates were found to save")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Please add coordinate(s)")

    def import_coords(self):
        file = self.gui_file.get_file(file_type="Coordinates File (*.coo)")
        if file:
            data = self.fop.read_lis(file)
            if len(data) > 0:
                if len(self.gui_dev.list_of_list(self.phot_coor_list)) > 0:
                    answ = self.gui_dev.ask_calcel(
                        "Do you want to replace coordinates. Click NO for adding coordinates")
                    if answ == "yes":
                        self.gui_dev.replace_list_con(self.phot_coor_list, data)
                    elif answ == "no":
                        self.gui_dev.add(self.phot_coor_list, data)
                    else:
                        self.logger.warning("User canceled adding coordinates")
                else:
                    self.gui_dev.add(self.phot_coor_list, data)
        else:
            self.logger.warning("User canceled adding coordinates")

    def rm_files(self, device):
        self.gui_dev.rm_from_tree(device)

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

    def remove_settings_profile(self):
        profile = self.settings_profile_selector.currentText()
        self.load_settings(profile)
        if profile == "--Default--":
            self.logger.warning("Cannot remove Default Profile")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Cannot remove Default profile")
        elif profile == "--New--":
            self.logger.warning("Cannot remove New Profile")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "This setting is used for add profile only.")
        else:
            all_settings = self.fop.read_json(self.settings_file)
            del all_settings[profile]
            self.fop.write_json(self.settings_file, all_settings)

        self.load_list_of_settngs()

    def load_list_of_settngs(self):
        global current_profile
        all_settings = self.fop.read_json(self.settings_file)
        try:
            current_profile = all_settings["--Current--"]
            del all_settings["--Current--"]
        except:
            self.logger.warning("No current profile available")

        self.gui_dev.c_replace_list_con(self.settings_profile_selector, all_settings.keys())
        try:
            self.settings_profile_selector.setCurrentText(current_profile)
        except:
            self.logger.warning("No current profile available")

    def setting_profile_changed(self):
        profile = self.settings_profile_selector.currentText()

        if profile == "--Default--":
            self.settings_new_profile.setEnabled(False)
        elif profile == "--New--":
            self.settings_new_profile.setEnabled(True)
        else:
            self.settings_new_profile.setEnabled(False)
        try:
            self.load_settings(profile)
        except Exception as e:
            self.logger.warning("{}. Probably first load".format(e))

    def load_settings(self, profile_name):
        all_settings = self.fop.read_json(self.settings_file)

        the_settings = all_settings[profile_name]

        calib_settings = the_settings["calib_settings"]
        self.zero_combine.setCurrentText(calib_settings["cali_zero_combine"])
        self.zero_reject.setCurrentText(calib_settings["cali_zero_reject"])

        self.dark_combine.setCurrentText(calib_settings["cali_dark_combine"])
        self.dark_reject.setCurrentText(calib_settings["cali_dark_reject"])
        self.dark_scale.setCurrentText(calib_settings["cali_dark_scale"])

        self.flat_combine.setCurrentText(calib_settings["cali_flat_combine"])
        self.flat_reject.setCurrentText(calib_settings["cali_flat_reject"])

        phot_settings = the_settings["phot_settings"]
        self.gui_dev.clear_table(self.phot_par_list)
        self.gui_dev.add_table(self.phot_par_list, phot_settings["phot_pars"])
        self.gui_dev.replace_list_con(self.phot_header_to_exract, phot_settings["header_to_extract"])

        cosmic_settings = the_settings["cosmic_settings"]
        self.ccleaner_sigclip.setValue(cosmic_settings["sigclip"])
        self.ccleaner_sigfrac.setValue(cosmic_settings["sigfrac"])
        self.ccleaner_objlim.setValue(cosmic_settings["objlim"])
        self.ccleaner_gain.setValue(cosmic_settings["gain"])
        self.ccleaner_readnoise.setValue(cosmic_settings["readnoise"])
        self.ccleaner_satlevel.setValue(cosmic_settings["satlevel"])
        self.ccleaner_pssl.setValue(cosmic_settings["pssl"])
        self.ccleaner_iteration.setValue(cosmic_settings["iteration"])
        self.ccleaner_sepmed.setChecked(cosmic_settings["sepmed"])
        self.ccleaner_cleantype.setCurrentText(cosmic_settings["cleantype"])
        self.ccleaner_fsmode.setCurrentText(cosmic_settings["fsmode"])
        self.ccleaner_psfmodel.setCurrentText(cosmic_settings["psfmodel"])
        self.ccleaner_psffwhm.setValue(cosmic_settings["psffwhm"])
        self.ccleaner_psfsize.setValue(cosmic_settings["psfsize"])

    def save_the_settings(self):
        all_settings = self.fop.read_json(self.settings_file)
        profile = self.settings_profile_selector.currentText()
        if profile == "--Current--":
            pass
        elif profile == "--Default--":
            self.settings_new_profile.setEnabled(False)
            self.logger.warning("Cannot save default settings")
            QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Cannot save default settings")
        elif profile == "--New--":
            self.settings_new_profile.setEnabled(True)
            profile_name = self.settings_new_profile.text()
            if not profile_name == "":
                if not profile_name in self.gui_dev.c_list_pf_list(self.settings_profile_selector):
                    # Calibration group
                    cali_zero_combine = self.zero_combine.currentText()
                    cali_zero_reject = self.zero_reject.currentText()

                    cali_dark_combine = self.dark_combine.currentText()
                    cali_dark_reject = self.dark_reject.currentText()
                    cali_dark_scale = self.dark_scale.currentText()

                    cali_flat_combine = self.flat_combine.currentText()
                    cali_flat_reject = self.flat_reject.currentText()
                    calib_settings = {"cali_zero_combine": cali_zero_combine, "cali_zero_reject": cali_zero_reject,
                                      "cali_dark_combine": cali_dark_combine, "cali_dark_reject": cali_dark_reject,
                                      "cali_dark_scale": cali_dark_scale, "cali_flat_combine": cali_flat_combine,
                                      "cali_flat_reject": cali_flat_reject}

                    # Photometry group
                    phot_pars = self.gui_dev.list_of_table(self.phot_par_list)
                    if phot_pars is None:
                        phot_pars = []
                    header_to_extract = self.gui_dev.list_of_list(self.phot_header_to_exract)
                    phot_settings = {"phot_pars": phot_pars, "header_to_extract": header_to_extract}

                    # Cosmic cleaner group
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
                    cosmic_settings = {"sigclip": sigclip, "sigfrac": sigfrac, "objlim": objlim, "gain": gain,
                                       "readnoise": readnoise, "satlevel": satlevel, "pssl": pssl,
                                       "iteration": iteration, "sepmed": sepmed, "cleantype": cleantype,
                                       "fsmode": fsmode, "psfmodel": psfmodel, "psffwhm": psffwhm, "psfsize": psfsize}

                    all_settings[profile_name] = {"calib_settings": calib_settings,
                                                  "phot_settings": phot_settings,
                                                  "cosmic_settings": cosmic_settings}

                    all_settings["--Current--"] = profile
                    self.settings_new_profile.setText("")

                    self.fop.write_json(self.settings_file, all_settings)
                else:
                    self.logger.warning("Name already exist")
                    QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "Name already exist")

            else:
                self.logger.warning("No new profile name was given. Nothing to do.")
                QtWidgets.QMessageBox.warning(self, "MYRaf Warning", "No new profile name was given. Nothing to do.")

        else:
            self.settings_new_profile.setEnabled(False)
            profile_name = self.settings_profile_selector.currentText()
            cali_zero_combine = self.zero_combine.currentText()
            cali_zero_reject = self.zero_reject.currentText()

            cali_dark_combine = self.dark_combine.currentText()
            cali_dark_reject = self.dark_reject.currentText()
            cali_dark_scale = self.dark_scale.currentText()

            cali_flat_combine = self.flat_combine.currentText()
            cali_flat_reject = self.flat_reject.currentText()
            calib_settings = {"cali_zero_combine": cali_zero_combine, "cali_zero_reject": cali_zero_reject,
                              "cali_dark_combine": cali_dark_combine, "cali_dark_reject": cali_dark_reject,
                              "cali_dark_scale": cali_dark_scale, "cali_flat_combine": cali_flat_combine,
                              "cali_flat_reject": cali_flat_reject}

            # Photometry group
            phot_pars = self.gui_dev.list_of_table(self.phot_par_list)
            if phot_pars is None:
                phot_pars = []
            header_to_extract = self.gui_dev.list_of_list(self.phot_header_to_exract)
            phot_settings = {"phot_pars": phot_pars, "header_to_extract": header_to_extract}

            # Cosmic cleaner group
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
            cosmic_settings = {"sigclip": sigclip, "sigfrac": sigfrac, "objlim": objlim, "gain": gain,
                               "readnoise": readnoise, "satlevel": satlevel, "pssl": pssl, "iteration": iteration,
                               "sepmed": sepmed, "cleantype": cleantype, "fsmode": fsmode, "psfmodel": psfmodel,
                               "psffwhm": psffwhm, "psfsize": psfsize}

            all_settings[profile_name] = {"calib_settings": calib_settings,
                                          "phot_settings": phot_settings,
                                          "cosmic_settings": cosmic_settings}

            all_settings["--Current--"] = profile

            self.fop.write_json(self.settings_file, all_settings)
        self.load_list_of_settngs()

    def load_phot_result(self):
        file = self.gui_file.get_file("*.my")
        if file:
            data = ascii.read(file, delimiter='|')

            coordinates = np.unique(data['Coordinate'])
            self.graph_variabl_index.clear()
            self.graph_compair_index.clear()
            self.graph_compair2_index.clear()
            for coord_pair in coordinates:
                self.graph_variabl_index.addItem(str(coord_pair))
                self.graph_compair_index.addItem(str(coord_pair))
                self.graph_compair2_index.addItem(str(coord_pair))

            self.graph_aperture.clear()
            apertures = np.unique(data["Aperture"])
            for aperture in apertures:
                self.graph_aperture.addItem(str(aperture))

            filters = None
            for colname in data.colnames:
                if "filter" in str(colname).lower() or "subset" in colname.lower():
                    filter_col = colname
                    filters = np.unique(data[filter_col])

            self.graph_filter.clear()
            if filters is None:
                self.graph_filter.addItem("Unknown")
            else:
                for filter in filters:
                    self.graph_filter.addItem(str(filter))

            xs = None
            self.graph_x_values.clear()
            for colname in data.colnames:
                if "DATE" in colname or "JD" in colname or "UT" in colname or "TIME" in colname:
                    self.graph_x_values.addItem(str(colname))

            # self.GDevice.replace_list_con(self.file_list, image_names)
            self.graph_path.setText(file)

        else:
            self.logger.warning("User cancel")

        return True
        # graph_t_0
        # graph_period

    def color_picker(self):
        color = QtWidgets.QColorDialog.getColor()
        self.graph_color_picker.setStyleSheet(f'background-color: {color.name()}')
        self.graph_color_picker.setText(color.name())

    def clear_plot(self):
        try:
            graph_object.axlc1.cla()
            graph_object.axlc2.cla()
        except:
            pass

    def plot_phot_result(self):
        result_file = self.graph_path.text()
        data = ascii.read(result_file, delimiter="|")
        data = data[(data["MAG"] != "INDEF") & (data["MERR"] != "INDEF") &
                    (data["JD"] != "INDEF") & (data["DATE-OBS"] != "INDEF")]

        x_axis_name = self.graph_x_values.currentText()
        target_coord = self.graph_variabl_index.currentText()
        comp1_coord = self.graph_compair_index.currentText()
        comp2_coord = self.graph_compair2_index.currentText()

        filter = self.graph_filter.currentText()

        if filter != "Unknown":
            phot_data_target = data[(data["FILTER"] == filter) & (data["Coordinate"] == target_coord)].group_by(x_axis_name)
            phot_data_comp1 = data[(data["FILTER"] == filter) & (data["Coordinate"] == comp1_coord)].group_by(x_axis_name)
            phot_data_comp2 = data[(data["FILTER"] == filter) & (data["Coordinate"] == comp2_coord)].group_by(x_axis_name)
        else:
            phot_data_target = data[data["Coordinate"] == target_coord].group_by(x_axis_name)
            phot_data_comp1 = data[data["Coordinate"] == comp1_coord].group_by(x_axis_name)
            phot_data_comp2 = data[data["Coordinate"] == comp2_coord].group_by(x_axis_name)


        if "DATE" in x_axis_name or "TIME" in x_axis_name:
            if "T" in phot_data_target[x_axis_name][0]:
                format = "isot"
            else:
                format = "iso"
            offset = 0
        elif "MJD" in x_axis_name:
            format = "mjd"
        elif "JD" in x_axis_name:
            format = "jd"

        time_xs = Time(phot_data_target[x_axis_name], format=format).jd

        if self.graph_do_phase.isChecked():
            if self.graph_t_0.value() and self.graph_period.value():
                t0 = float(self.graph_t_0.value())
                period = float(self.graph_period.value())
                time_xs = ((time_xs - t0) / period) - ((time_xs - t0) / period).astype(int)
                time_axis_label = "PHASE"
            else:
                time_axis_label = "TIME [JD]"
                time_xs = phot_data_target[x_axis_name]
        else:
            time_axis_label = "TIME [JD]"
            time_axis_value = phot_data_target[x_axis_name]

        target_mag = phot_data_target["MAG"].astype(float)
        target_mag_err = phot_data_target["MERR"].astype(float)
        comp1_mag = phot_data_comp1["MAG"].astype(float)
        comp1_mag_err = phot_data_comp1["MERR"].astype(float)
        comp2_mag = phot_data_comp2["MAG"].astype(float)
        comp2_mag_err = phot_data_comp2["MERR"].astype(float)

        target_comp1_diff = target_mag - comp1_mag
        comp1_comp2_diff = comp1_mag - comp2_mag

        target_comp1_diff_err = np.sqrt(np.power((target_mag_err), 2) +
                                         np.power((comp1_mag_err), 2))

        comp1_comp2_diff_err = np.sqrt(np.power((comp2_mag_err), 2) +
                                       np.power((comp2_mag_err), 2))

        phot_stdev = np.std(comp1_comp2_diff)

        graph_object = self.graph_chart.canvas

        # graph_object.axlc1.cla()

        point_color = self.graph_color_picker.text()

        if point_color == "Pick color":
            point_color = "blue"

        point_shape = self.graph_shape.currentText()

        # graph_object.axlc1.cla()
        # graph_object.axlc2.cla()
        graph_object.axlc1.errorbar(time_xs, target_comp1_diff, yerr=target_comp1_diff_err,
                                    color=point_color, marker=point_shape, ecolor='k', capsize=2, capthick=2,
                                    label='{}'.format(filter))
        graph_object.axlc2.errorbar(time_xs, comp1_comp2_diff, yerr=comp1_comp2_diff_err,
                                    color=point_color, marker=point_shape, ecolor='k', capsize=2, capthick=2,
                                    label="{} ($\sigma$: {:.3f}$^m$)".format(filter, phot_stdev))
        graph_object.axlc2.axhline(y=phot_stdev, color='k', linestyle='-', linewidth=0.5)

        # get handles
        handles, labels = graph_object.axlc1.get_legend_handles_labels()
        # remove the errorbars
        handles = [h[0] for h in handles]
        # use them in the legend
        graph_object.axlc1.legend(handles, labels, loc = 'best')

        # get handles
        handles, labels = graph_object.axlc2.get_legend_handles_labels()
        # remove the errorbars
        handles = [h[0] for h in handles]
        # use them in the legend
        graph_object.axlc2.legend(handles, labels, loc='best')

        # plt.grid(True)
        # graph_object.axlc1.invert_yaxis()
        graph_object.axlc1.set_ylim(sorted(graph_object.axlc1.get_ylim(), reverse=True))
        # graph_object.axlc2.invert_yaxis()
        graph_object.axlc2.set_ylim(sorted(graph_object.axlc2.get_ylim(), reverse=True))
        graph_object.axlc1.set_title("MYRaf Project (v3.0.0) Photometry Result, {}".format(
            time.strftime("%d %B %Y %I:%M:%S %p")))
        graph_object.axlc2.set_xlabel(time_axis_label.upper(), fontsize = 9)
        graph_object.axlc1.set_ylabel("Diff. Mag. (V - C1)", fontsize = 9)
        graph_object.axlc2.set_ylabel("Diff. Mag. (C1 - C2)", fontsize = 9)
        graph_object.axlc1.get_xaxis().get_major_formatter().set_scientific(False)
        graph_object.axlc2.get_xaxis().get_major_formatter().set_scientific(False)
        graph_object.draw()
        # graph_object.fig.tight_layout()

        mpl_cursor = mplcursors.cursor(graph_object.fig)

        @mpl_cursor.connect("add")
        def on_add(sel):
            otime = sel.target[0]
            sel.annotation.set(text=f'Point: \nX: {sel.target[0]: .6f} \nY: {sel.target[1]: .3f}',
                               ha="left", va="center")
            sel.annotation.set_ha('left')
            sel.annotation.set_weight('bold')

            itemindex = np.where((time_xs - otime) == 0)

            fits_file = data['File_name'][itemindex][0]

            # print(time_xs[itemindex][0],fits_file)

            self.phot_display.load(fits_file)

    def plot_imexam(self, event):
        if event.key == 'r':
            x = event.xdata
            y = event.ydata
            fits_data = self.phot_display.image.get_data()
            plots = Imexamine()
            plots.radial_profile(x, y, fits_data)

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
