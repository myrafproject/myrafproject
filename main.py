# -*- coding: utf-8 -*-
"""
@author: msh, yk
"""

try:
    from sys import argv

    import argparse

    from logging import getLogger, basicConfig, DEBUG

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
    def __init__(self, parent=None, logger_level=50):
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
        basicConfig(filename=None, level=logger_level, format=LOG_FORMAT)
        self.logger = getLogger()

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
        self.calib_bias_remove.clicked.connect(lambda: (self.rm_files(self.calib_image_list)))
        self.calib_bias_combine.clicked.connect(lambda: (self.export_bias()))

        self.calib_dark_add.clicked.connect(lambda: (self.add_files(self.calib_dark_list)))
        self.calib_dark_remove.clicked.connect(lambda: (self.rm_files(self.calib_dark_list)))
        self.calib_dark_combine.clicked.connect(lambda: (self.export_dark()))

        self.calib_flat_add.clicked.connect(lambda: (self.add_files(self.calib_flat_list)))
        self.calib_flat_remove.clicked.connect(lambda: (self.rm_files(self.calib_flat_list)))
        self.calib_flat_combine.clicked.connect(lambda: (self.export_flat()))

        self.calibration_go.clicked.connect(lambda: (self.calibration()))

        self.hedit_isvaluefromheader.clicked.connect(lambda: (self.toggle_header()))

        self.hedit_add.clicked.connect(lambda: (self.add_files(self.hedit_list)))
        self.hedit_remove.clicked.connect(lambda: (self.rm_files(self.hedit_list)))

        self.align_add.clicked.connect(lambda: (self.add_files(self.align_list)))
        self.phot_add.clicked.connect(lambda: (self.add_files(self.phot_list)))
        self.display_phot.canvas.fig.canvas.mpl_connect('button_press_event', self.get_coordinate_phot)

        self.hedit_remove_field.clicked.connect(lambda: (self.rm_header()))
        self.hedit_add_field.clicked.connect(lambda: (self.add_header()))

        self.align_list.clicked.connect(lambda: (self.display(self.align_list, self.align_display)))
        self.phot_list.clicked.connect(lambda: (self.display(self.phot_list, self.phot_display)))
        self.hedit_list.clicked.connect(lambda: (self.show_headers()))
        self.tableWidget.clicked.connect(lambda: (self.header_selected()))

        self.calib_image_list.installEventFilter(self)
        self.calib_bias_list.installEventFilter(self)
        self.calib_dark_list.installEventFilter(self)
        self.calib_flat_list.installEventFilter(self)
        self.align_list.installEventFilter(self)
        self.phot_list.installEventFilter(self)
        self.hedit_list.installEventFilter(self)
        self.phot_coor_list.installEventFilter(self)

        self.display_align.canvas.fig.canvas.mpl_connect('motion_notify_event', self.align_onpick)
        self.display_phot.canvas.fig.canvas.mpl_connect('motion_notify_event', self.phot_onpick)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

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
                flat_subset = self.flat_subset.currentText()
                flat_file = "{}/myraf_flat.fits".format(self.fop.tmp_dir)
                try:
                    self.iraf.flatcombine(flat_files, flat_file, method=flat_combine,
                                          rejection=flat_reject, subset=flat_subset)
                except:
                    self.logger.warning("Flatcombine failed. Flatcorrection will be skipped.")
                    flat_file = None
            else:
                self.logger.warning("No flat file. Flatcorrection will be skipped.")
                flat_file = None

            if flat_file is None and dark_file is None and zero_file is None:
                self.logger.warning("No operation available")
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
                flat_subset = self.flat_subset.currentText()
                self.iraf.flatcombine(files, out_file, method=flat_combine, rejection=flat_reject, subset=flat_subset)
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
        self.hedit_field.setText(self.tableWidget.item(self.tableWidget.currentItem().row(), 0).text())
        self.hedit_value.setText(self.tableWidget.item(self.tableWidget.currentItem().row(), 1).text())

    def show_headers(self):
        the_file = self.hedit_list.currentItem()
        if the_file is not None:
            if the_file.child(0) is not None:
                headers = self.fts.header(the_file.toolTip(0))
                self.gui_dev.replace_table(self.tableWidget, headers)
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

        if event.type() == QtCore.QEvent.ContextMenu and source is self.hedit_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Add', lambda: (self.add_files(self.hedit_list)))
            menu.addAction('Remove', lambda: (self.rm_files(self.hedit_list)))
            menu.addSeparator()
            menu.addAction('Expand All', lambda: (self.hedit_list.expandAll()))
            menu.addAction('Collapse All', lambda: (self.hedit_list.collapseAll()))
            menu.exec_(event.globalPos())
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.phot_coor_list:
            menu = QtWidgets.QMenu()
            menu.addAction('Remove', lambda: (self.gui_dev.rm(self.phot_coor_list)))
            menu.addSeparator()
            menu.addAction('Show All', lambda: ())
            menu.addAction('Show Selected', lambda: ())
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
    parser.add_argument("--logger", "-ll", help="Logger Level", default=50)
    args = parser.parse_args()

    app = QtWidgets.QApplication(argv)
    window = MainWindow(logger_level=args.logger)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
