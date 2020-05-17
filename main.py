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

    from fPlot import FitsPlot

    from numpy import isnan
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
        # self.fts =
        self.fts = analyse.Astronomy.Fits(self.logger)

        self.align_display = FitsPlot(self.display_align.canvas, self.logger)
        self.phot_display = FitsPlot(self.display_phot.canvas, self.logger)

        self.calib_image_add.clicked.connect(lambda: (self.add_files(self.calib_image_list)))
        self.calib_image_remove.clicked.connect(lambda: (self.rm_files(self.calib_image_list)))

        self.calib_bias_add.clicked.connect(lambda: (self.add_files(self.calib_bias_list)))
        self.calib_bias_remove.clicked.connect(lambda: (self.rm_files(self.calib_image_list)))

        self.calib_dark_add.clicked.connect(lambda: (self.add_files(self.calib_dark_list)))
        self.calib_dark_remove.clicked.connect(lambda: (self.rm_files(self.calib_dark_list)))

        self.calib_flat_add.clicked.connect(lambda: (self.add_files(self.calib_flat_list)))
        self.calib_flat_remove.clicked.connect(lambda: (self.rm_files(self.calib_flat_list)))

        self.align_add.clicked.connect(lambda: (self.add_files(self.align_list)))
        self.phot_add.clicked.connect(lambda: (self.add_files(self.phot_list)))
        self.display_phot.canvas.fig.canvas.mpl_connect('button_press_event', self.get_coordinate_phot)

        self.align_list.clicked.connect(lambda: (self.display(self.align_list, self.align_display)))
        self.phot_list.clicked.connect(lambda: (self.display(self.phot_list, self.phot_display)))


        self.calib_image_list.installEventFilter(self)
        self.calib_bias_list.installEventFilter(self)
        self.calib_dark_list.installEventFilter(self)
        self.calib_flat_list.installEventFilter(self)
        self.align_list.installEventFilter(self)
        self.phot_list.installEventFilter(self)
        self.phot_coor_list.installEventFilter(self)

        self.display_align.canvas.fig.canvas.mpl_connect('motion_notify_event', self.align_onpick)
        self.display_phot.canvas.fig.canvas.mpl_connect('motion_notify_event', self.phot_onpick)


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
