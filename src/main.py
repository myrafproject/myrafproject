# -*- coding: utf-8 -*-
"""
@author: msh, yk
"""

import warnings

import argparse
import json
import platform
from logging import getLogger, basicConfig
from pathlib import Path
from sys import argv

from typing import List
from logging import Logger

import pandas as pd
import math
import statistics

# noinspection PyUnresolvedReferences
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QEvent, Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem

import qdarktheme

from astropy.utils.exceptions import AstropyWarning
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.io.fits import Header
from astropy.time import Time
from astropy.wcs import WCS
from astropy.wcs.utils import fit_wcs_from_points

from dateutil.relativedelta import relativedelta
import astroalign

from ginga.AstroImage import AstroImage
from ginga.canvas.types.basic import Circle, Rectangle
from ginga.qtw.ImageViewQt import CanvasView

from myraflib import FitsArray, Fits
from myraflib.error import Unsolvable
from myrafgui import Ui_MainWindow, Ui_FormDisplay, Ui_FormArithmetic, Ui_FormCombine, Ui_FormCosmicCleaner, \
    Ui_FormAlign, Ui_FormShift, Ui_FormRotate, Ui_FormHedit, Ui_FormBin, Ui_FormCrop, Ui_FormHeader, Ui_FormHSelect, \
    Ui_FormStatics, Ui_FormObservatory, Ui_FormHeaderCalculator, Ui_FormAbout, Ui_FormLog, Ui_FormCCDPROC, \
    Ui_FormPhotometry, Ui_FormSettings, Ui_FormWCS

from myrafgui.functions import SCHEMA, GUIFunctions, CustomQTreeWidgetItem

DEFAULT_OBSERVATORIES = {
    "NEW": {
        "lat": 0,
        "lon": 0,
        "height": 0
    }
}

DEFAULT_SETTINGS = {
    "ZMag": 25,
    "display": {
        "interval": 100,
    },
    "operations": {
        "arithmetic": {
            "operation": 0,
            "default_value": 0,
        },
        "combine": {
            "combine": {
                "method": 0,
                "clipping": 0,
                "weight": "None",
            },
            "zerocombine": {
                "method": 2,
                "clipping": 2,
                "weight": "None",
            },
            "darkcombine": {
                "method": 2,
                "clipping": 2,
                "weight": "EXPTIME",
            },
            "flatcombine": {
                "method": 2,
                "clipping": 2,
                "weight": "None",
            },
        },
        "transform": {
            "align": {
                "maximum_control_point": 50,
                "detection_sigma": 5.0,
                "minimum_area": 50,
            },
        },
        "ccdproc": {
            "exposure": "None",
            "force": False,
        },
        "photometry": {
            "kind": 0,
            "exposure": "None",
            "apertures": [],
            "headers_to_extract": [],
            "sextractor": {
                "extract": {
                    "sigma": 5.0,
                    "maximum_area": 5.0,
                },
                "daofind": {
                    "sigma": 3.0,
                    "fwhm": 3.0,
                    "threshold": 5.0,
                },
            },
        },
    },
    "edit": {
        "cosmic_clean": {
            "sigclip": 4.5,
            "sigfrac": 0.3,
            "objlim": 5.0,
            "gain": 1.0,
            "readnoise": 6.5,
            "satlevel": 65535.0,
            "niter": 4,
            "sepmed": True,
            "cleantype": 0,
            "fsmode": 0,
            "psfmodel": 0,
            "psffwhm": 2.5,
            "psfsize": 7,
            "psfbeta": 4.76,
            "gain_apply": True
        },
        "wcs": {
            "astrometry_apikey": '',
            "save": False
        }
    }
}

LOGO = (Path(__file__).parent.parent / 'myraf.png').absolute().__str__()

warnings.filterwarnings('ignore', category=AstropyWarning)


def database_dir():
    home_dir = Path.home()
    if platform.system() == "Windows":
        settings_dir = home_dir / "AppData" / "Local" / "MYRaf"
    elif platform.system() == "Darwin":
        settings_dir = home_dir / "Library" / "Application Support" / "MYRaf"
    else:
        settings_dir = home_dir / ".config" / "MYRaf"

    if not settings_dir.exists():
        settings_dir.mkdir()

    return settings_dir


# noinspection PyUnresolvedReferences
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, logger_level="DEBUG", log_file=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        if log_file is None:
            self.log_file = database_dir() / Path("myraf.log")
        else:
            self.log_file = log_file

        log_format = "[%(asctime)s, %(levelname)s], [%(filename)s, %(funcName)s, %(lineno)s]: %(message)s"
        basicConfig(filename=self.log_file, level=logger_level, format=log_format)

        self.logger = getLogger("MYRaf")

        getLogger('matplotlib.font_manager').disabled = True
        getLogger('libGL').disabled = True

        self.settings = Setting(self.logger)

        self.gui_functions = GUIFunctions(self)

        self.treeWidget.installEventFilter(self)

        self.actionObservatories.triggered.connect(lambda: self.show_window(ObservatoriesForm(self)))
        self.actionAbout.triggered.connect(lambda: self.show_window(AboutForm(self)))
        self.actionLog.triggered.connect(lambda: self.show_window(LogForm(self)))
        self.actionSettings.triggered.connect(lambda: self.show_window(SettingsForm(self)))
        self.actionQuit.triggered.connect(lambda: self.close())

    def show_window(self, window):
        self.playGround.addSubWindow(window)
        window.show()

    def add_files(self):
        files = self.gui_functions.get_files("Get Files")
        if files:
            self.gui_functions.add_to_files(files, self.treeWidget)

    def remove_files(self):
        self.gui_functions.remove_from_files(self.treeWidget)

    def rename(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        group_name = list(files.keys())[0].text(0)
        new_name, ok = self.gui_functions.get_text("Rename Group", "Provide new group name", group_name)
        if ok:
            list(files.keys())[0].setText(0, new_name)

    def save_as(self):
        warn = 0
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        drct = self.gui_functions.get_directory("Save Folder")
        if not drct:
            return

        directory = Path(drct)

        if not directory:
            return

        progress = QtWidgets.QProgressDialog("Copying ...", "Abort", 0, len(fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.treeWidget, ["Copy"])

        for iteration, fits in enumerate(fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = directory / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.save_as(file_name.__str__())

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.logger.warning(e)
        progress.close()
        if group_layer.childCount() == 0:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def merge(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        new_name, ok = self.gui_functions.get_text("Group Name", "Merged Group Name", "Group")
        if ok:
            new_files = sorted(
                list(set([
                    (Path(file.child(0).text(1)) / Path(file.text(0))).absolute().__str__()
                    for _, file_list in files.items()
                    for file in file_list
                ]))
            )
            self.gui_functions.add_to_files(new_files, self.treeWidget, grp=new_name)

    def split(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        group_name = list(files.keys())[0].text(0)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)
        list_of_header = list(fits_array[0].header().keys())
        item, ok = self.gui_functions.get_item("Select header(s)", "Headers", list_of_header)
        if ok:
            groups = fits_array.group_by(item)
            for group, files in groups.items():
                self.gui_functions.add_to_files(files.files(), self.treeWidget, f"{group_name}_{'_'.join(group)}")

    def display(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        for group, files in selected_files.items():
            self.show_window(DisplayForm(
                self,
                FitsArray([Fits(Path(file.child(0).text(1)) / Path(file.text(0))) for file in files])
            ))

    def arithmetic(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in
                list(selected_files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(ArithmeticForm(self, fits_array))

    def combine(self, combine_type=None):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]

        if len(fits) > 10:
            answer = self.gui_functions.ask(
                "Warning",
                f"You selected {len(fits)} files. This might require too much RAM. Do you wish to continue?"
            )
            if not answer:
                return

        fits_array = FitsArray.from_paths(fits)
        combine = CombineForm(self, fits_array, combine_type)
        self.show_window(combine)

    def align(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in
                list(selected_files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(AlignForm(self, fits_array))

    def binning(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in
                list(selected_files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(BinForm(self, fits_array))

    def crop(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in
                list(selected_files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(CropForm(self, fits_array))

    def rotate(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in
                list(selected_files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(RotateForm(self, fits_array))

    def shift(self):
        selected_files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in
                list(selected_files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(ShiftForm(self, fits_array))

    def header_show(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(HeaderForm(self, fits_array))

    def hselect(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(HSelectForm(self, fits_array))

    def statics(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        data = []
        for key, rows in files.items():
            for row in rows:
                image = (Path(row.child(0).text(1)) / Path(row.text(0))).absolute().__str__()
                npix = row.child(1).text(1)
                mean = row.child(2).text(1)
                stddev = row.child(3).text(1)
                min = row.child(4).text(1)
                max = row.child(5).text(1)

                data.append(
                    [image, npix, mean, stddev, min, max]
                )

        self.show_window(StatisticsForm(self, data))

    def cosmic_clean(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(CosmicCleanerForm(self, fits_array))

    def hedit(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(HeditForm(self, fits_array))

    def ccdproc(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(CCDProcForm(self, fits_array))

    def hcalc(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(HCalcForm(self, fits_array))

    def photometry(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(PhotometryForm(self, fits_array))

    def wcs(self):
        files = self.gui_functions.get_selected_files(self.treeWidget)
        fits = [(Path(f.child(0).text(1)) / Path(f.text(0))).absolute().__str__() for f in list(files.values())[0]]
        fits_array = FitsArray.from_paths(fits)

        self.show_window(WCSForm(self, fits_array))

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.treeWidget:

            selected = self.gui_functions.get_selected_files(self.treeWidget)

            menu_file = QtWidgets.QMenu("File")
            menu_file.addAction('Add', lambda: (self.add_files()))

            remove = menu_file.addAction('Remove', lambda: (self.remove_files()))
            if len(selected) < 1:
                remove.setEnabled(False)

            rename = menu_file.addAction('Rename', lambda: (self.rename()))
            if len(selected) != 1:
                rename.setEnabled(False)

            save_as = menu_file.addAction('Save As', lambda: (self.save_as()))
            if len(selected) != 1:
                save_as.setEnabled(False)

            menu_file.addSeparator()
            merge = menu_file.addAction('Merge', lambda: (self.merge()))
            if len(selected) < 2:
                merge.setEnabled(False)
            split = menu_file.addAction('Split', lambda: (self.split()))
            if len(selected) != 1:
                split.setEnabled(False)
            #
            menu_operations = QtWidgets.QMenu("Operations")

            arithmetic = menu_operations.addAction("Arithmetic...", lambda: (self.arithmetic()))
            if len(selected) != 1:
                arithmetic.setEnabled(False)

            menu_operations_combine = QtWidgets.QMenu("Combine")

            combine = menu_operations_combine.addAction("Combine...", lambda: (self.combine("combine")))
            if len(selected) != 1:
                combine.setEnabled(False)
            else:
                if len(selected[list(selected.keys())[0]]) < 2:
                    combine.setEnabled(False)

            menu_operations_combine.addSeparator()
            zero_combine = menu_operations_combine.addAction("Zero Combine...", lambda: (self.combine("zerocombine")))
            if len(selected) != 1:
                zero_combine.setEnabled(False)
            else:
                if len(selected[list(selected.keys())[0]]) < 2:
                    zero_combine.setEnabled(False)

            dark_combine = menu_operations_combine.addAction("Dark Combine...", lambda: (self.combine("darkcombine")))
            if len(selected) != 1:
                dark_combine.setEnabled(False)
            else:
                if len(selected[list(selected.keys())[0]]) < 2:
                    dark_combine.setEnabled(False)

            flat_combine = menu_operations_combine.addAction("Flat Combine...", lambda: (self.combine("flatcombine")))
            if len(selected) != 1:
                flat_combine.setEnabled(False)
            else:
                if len(selected[list(selected.keys())[0]]) < 2:
                    flat_combine.setEnabled(False)

            menu_operations_transform = QtWidgets.QMenu("Transform")
            align = menu_operations_transform.addAction("Align...", lambda: (self.align()))
            if len(selected) != 1:
                align.setEnabled(False)
            else:
                if len(selected[list(selected.keys())[0]]) < 2:
                    align.setEnabled(False)

            menu_operations_transform.addSeparator()
            binning = menu_operations_transform.addAction("Bin...", lambda: (self.binning()))
            if len(selected) != 1:
                binning.setEnabled(False)

            crop = menu_operations_transform.addAction("Crop...", lambda: (self.crop()))
            if len(selected) != 1:
                crop.setEnabled(False)
            #
            rotate = menu_operations_transform.addAction("Rotate...", lambda: (self.rotate()))
            if len(selected) != 1:
                rotate.setEnabled(False)

            shift = menu_operations_transform.addAction("Shift...", lambda: (self.shift()))
            if len(selected) != 1:
                shift.setEnabled(False)

            menu_operations_info = QtWidgets.QMenu("Information")
            header = menu_operations_info.addAction("Header...", lambda: (self.header_show()))
            if len(selected) != 1:
                header.setEnabled(False)

            statics = menu_operations_info.addAction("Statics...", lambda: (self.statics()))
            if len(selected) != 1:
                statics.setEnabled(False)

            menu_editor = QtWidgets.QMenu("Editor")

            cosmic_clean = menu_editor.addAction("Cosmic Clean...", lambda: (self.cosmic_clean()))
            if len(selected) != 1:
                cosmic_clean.setEnabled(False)

            hcalc = menu_editor.addAction("HCalc...", lambda: (self.hcalc()))
            if len(selected) != 1:
                hcalc.setEnabled(False)

            hselect = menu_editor.addAction("HSelect...", lambda: (self.hselect()))
            if len(selected) != 1:
                hselect.setEnabled(False)

            hedit = menu_editor.addAction("Header...", lambda: (self.hedit()))
            if len(selected) != 1:
                hedit.setEnabled(False)

            wcs = menu_editor.addAction("WCS...", lambda: (self.wcs()))
            if len(selected) != 1 or True:
                wcs.setEnabled(False)

            menu = QtWidgets.QMenu()
            menu.addMenu(menu_file)
            menu.addSeparator()
            display = menu.addAction('Display...', lambda: (self.display()))
            if len(selected) < 1:
                display.setEnabled(False)

            menu_operations.addMenu(menu_operations_combine)
            menu_operations.addMenu(menu_operations_transform)
            menu_operations.addMenu(menu_operations_info)
            menu_operations.addMenu(menu_editor)

            menu.addSeparator()

            ccdproc = menu_operations.addAction("CCDProc...", lambda: (self.ccdproc()))
            if len(selected) != 1:
                ccdproc.setEnabled(False)

            photometry = menu_operations.addAction("Photometry...", lambda: (self.photometry()))
            if len(selected) != 1:
                photometry.setEnabled(False)

            menu.addMenu(menu_operations)
            menu.exec_(event.globalPos())
            menu.addMenu(menu_editor)
            return True

        return super(MainWindow, self).eventFilter(source, event)

    def closeEvent(self, event):
        if self.gui_functions.ask("MYRaf", "Are you sure you want to quit?"):
            event.accept()
        else:
            event.ignore()


# noinspection PyUnresolvedReferences
class PhotometryForm(QWidget, Ui_FormPhotometry):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(PhotometryForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.canvas = CanvasView(render='widget')
        self.canvas.enable_autocuts('on')
        self.canvas.set_autocut_params('zscale')
        self.canvas.enable_autozoom('on')
        self.canvas.set_bg(0.2, 0.2, 0.2)
        self.canvas.ui_set_active(True)

        group_box_layout = QVBoxLayout()
        self.ginga_widget = self.canvas.get_widget()
        group_box_layout.addWidget(self.ginga_widget)
        self.groupBox.setLayout(group_box_layout)
        self.img = AstroImage(logger=self.parent.logger)
        self.img.load_data(self.fits_array[0].data())
        self.canvas.set_image(self.img)

        self.iteration = 0
        self.current_angle = 0

        self.ginga_widget.installEventFilter(self)
        self.listWidgetApertureRadii.installEventFilter(self)
        self.tableWidgetCoordinates.installEventFilter(self)

        self.reset_transform()
        self.load_headers()

        self.pushButtonAddToRadii.clicked.connect(self.add_to_apertures)
        self.pushButtonAddToHeaderToExtract.clicked.connect(self.select_header)
        self.pushButtonRemoveFromHeaderToExtract.clicked.connect(self.take_header)

        self.comboBoxPhotometryMethods.currentIndexChanged.connect(self.save_settings)
        self.comboBoxExposureInHeader.currentIndexChanged.connect(self.save_settings)
        self.doubleSpinBoxSexSigma.valueChanged.connect(self.save_settings)
        self.doubleSpinBoxSexMinimumArea.valueChanged.connect(self.save_settings)
        self.doubleSpinBoxDAOFindSigma.valueChanged.connect(self.save_settings)
        self.doubleSpinBoxDAOFindFWHM.valueChanged.connect(self.save_settings)
        self.doubleSpinBoxDAOindThreshold.valueChanged.connect(self.save_settings)
        self.load_settings()

        self.pushButtonGO.clicked.connect(self.go)

    def go(self):
        warn = 0
        coordinates = self.parent.gui_functions.get_from_table(self.tableWidgetCoordinates)
        if not coordinates:
            self.parent.gui_functions.error("No coordinates were given for aperture")
            return

        radii = self.parent.gui_functions.get_from_list(self.listWidgetApertureRadii)
        if not radii:
            self.parent.gui_functions.error("No radius were given for aperture")
            return

        headers = self.parent.gui_functions.get_from_list(self.listWidgetHeadersToExtract)

        exposure = self.comboBoxExposureInHeader.currentText()

        numeric_coordinates_x = [int(float(coord[0])) for coord in coordinates]
        numeric_coordinates_y = [int(float(coord[1])) for coord in coordinates]
        numeric_radii = [float(each) for each in radii]
        headers_to_extract = headers if headers else None
        exposure_in_header = None if exposure == "None" else exposure

        save_file = self.parent.gui_functions.save_file("Save File", "Comma Seperated Value (*.csv)")

        if not save_file:
            return

        progress = QtWidgets.QProgressDialog("Doing Photometry ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        photometry = []
        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                method = self.comboBoxPhotometryMethods.currentIndex()

                if method == 0:
                    phot = fits.photometry(numeric_coordinates_x, numeric_coordinates_y, numeric_radii,
                                           headers_to_extract, exposure_in_header)
                elif method == 1:
                    phot = fits.photometry_sep(numeric_coordinates_x, numeric_coordinates_y, numeric_radii,
                                               headers_to_extract, exposure_in_header)
                else:
                    phot = fits.photometry_phu(numeric_coordinates_x, numeric_coordinates_y, numeric_radii,
                                               headers_to_extract, exposure_in_header)

                photometry.append(phot)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()

        if len(photometry) == 0:
            self.parent.logger.warning("Cloudn't do photometry")
            self.parent.gui_functions.error("Cloudn't do photometry")
            return

        stacked_photometry = pd.concat(photometry, axis=0)
        stacked_photometry.to_csv(save_file)

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def load_settings(self):
        settings = self.parent.settings.settings
        self.comboBoxPhotometryMethods.setCurrentIndex(settings["operations"]["photometry"]["kind"])
        try:
            self.comboBoxExposureInHeader.setCurrentText(settings["operations"]["photometry"]["exposure"])
        except Exception as _:
            self.parent.logger.warning("Cannot set exposure header. Setting to default.")
            self.comboBoxExposureInHeader.setCurrentText("None")

        self.listWidgetApertureRadii.clear()
        self.parent.gui_functions.add_to_list(
            self.listWidgetApertureRadii, settings["operations"]["photometry"]["apertures"]
        )

        self.listWidgetHeadersToExtract.clear()
        self.parent.gui_functions.add_to_list(
            self.listWidgetHeadersToExtract, settings["operations"]["photometry"]["headers_to_extract"]
        )

        self.doubleSpinBoxSexSigma.setValue(settings["operations"]["photometry"]["sextractor"]["extract"]["sigma"])
        self.doubleSpinBoxSexMinimumArea.setValue(
            settings["operations"]["photometry"]["sextractor"]["extract"]["maximum_area"]
        )

        self.doubleSpinBoxDAOFindSigma.setValue(settings["operations"]["photometry"]["sextractor"]["daofind"]["sigma"])
        self.doubleSpinBoxDAOFindFWHM.setValue(settings["operations"]["photometry"]["sextractor"]["daofind"]["fwhm"])
        self.doubleSpinBoxDAOindThreshold.setValue(
            settings["operations"]["photometry"]["sextractor"]["daofind"]["threshold"]
        )

    def save_settings(self):
        settings = self.parent.settings.settings

        settings["operations"]["photometry"]["kind"] = self.comboBoxPhotometryMethods.currentIndex()
        settings["operations"]["photometry"]["exposure"] = self.comboBoxExposureInHeader.currentText()
        settings["operations"]["photometry"]["apertures"] = \
            self.parent.gui_functions.get_from_list(self.listWidgetApertureRadii)
        settings["operations"]["photometry"]["headers_to_extract"] = \
            self.parent.gui_functions.get_from_list(self.listWidgetHeadersToExtract)
        settings["operations"]["photometry"]["sextractor"]["extract"]["sigma"] = self.doubleSpinBoxSexSigma.value()
        settings["operations"]["photometry"]["sextractor"]["extract"]["maximum_area"] = \
            self.doubleSpinBoxSexMinimumArea.value()
        settings["operations"]["photometry"]["sextractor"]["daofind"]["sigma"] = self.doubleSpinBoxDAOFindSigma.value()
        settings["operations"]["photometry"]["sextractor"]["daofind"]["fwhm"] = self.doubleSpinBoxDAOFindFWHM.value()
        settings["operations"]["photometry"]["sextractor"]["daofind"]["threshold"] = \
            self.doubleSpinBoxDAOindThreshold.value()

        self.parent.settings.settings = settings

    def take_header(self):
        self.parent.gui_functions.remove_from_list(self.listWidgetHeadersToExtract)
        self.save_settings()

    def select_header(self):
        def f7(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        headers_to_add = self.parent.gui_functions.get_from_list_selected(self.listWidgetHeaders)
        available_headers = self.parent.gui_functions.get_from_list(self.listWidgetHeadersToExtract)
        headers = list(f7(available_headers + headers_to_add))
        self.listWidgetHeadersToExtract.clear()
        self.parent.gui_functions.add_to_list(self.listWidgetHeadersToExtract, headers)
        self.save_settings()

    def load_headers(self):
        header_keys = list(self.fits_array[0].header().columns)

        self.listWidgetHeaders.clear()
        self.parent.gui_functions.add_to_list(self.listWidgetHeaders, header_keys)

        self.comboBoxExposureInHeader.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxExposureInHeader, ["None"] + list(header_keys))

    def reset_transform(self):
        x, y, swap = self.canvas.get_transforms()
        if x:
            self.canvas.flip_x()
        if y:
            self.canvas.flip_y()
        if swap:
            self.canvas.swap_xy()

    def reset(self):
        self.reset_transform()
        self.canvas.rotate(0)
        self.canvas.zoom_fit()
        self.canvas.set_color_algorithm('linear')
        self.canvas.restore_cmap()
        self.canvas.set_color_map('gray')
        self.canvas.restore_contrast()
        self.canvas.set_intensity_map('ramp')

    def rotate(self):
        angle, ok = self.parent.gui_functions.get_number("Angle", "Please provide angle to rotate", 0, 360)
        if ok:
            try:
                self.current_angle = float(angle)
                self.canvas.rotate(self.current_angle)
            except Exception as e:
                self.logger.warning(e)

    def add_to_apertures(self):
        aperture = self.doubleSpinBoxApertureRadius.value()
        apertures = self.parent.gui_functions.get_from_list(self.listWidgetApertureRadii)
        if str(aperture) in apertures:
            self.parent.logger.error("aperture already exists")
            if not self.parent.gui_functions.ask("aperture already exists", "Do you want to force add it?"):
                return

        self.parent.gui_functions.add_to_list(self.listWidgetApertureRadii, [str(aperture)])
        self.save_settings()

    def aperture_to_show(self):
        try:
            apertures = self.parent.gui_functions.get_from_list(self.listWidgetApertureRadii)
            aperture = statistics.mean(map(float, apertures))
            if aperture > 0:
                return aperture
            return 10
        except Exception as e:
            self.parent.logger.warning(e)
            return 10

    def draw_aperture(self):
        current_coord = self.parent.gui_functions.get_from_table_selected(self.tableWidgetCoordinates)
        aperture = self.aperture_to_show()
        del self.canvas.canvas.objects[1:]
        coordinates = self.parent.gui_functions.get_from_table(self.tableWidgetCoordinates)
        for x, y in coordinates:
            try:
                x = int(x)
                y = int(y)
            except Exception as e:
                self.parent.logger.warning(e)
                return

            color = "red"
            if current_coord:
                for each in current_coord:
                    if each[0] == str(x) and each[1] == str(y):
                        color = "blue"

            circle = Circle(x, y, aperture, color, 5)
            self.canvas.canvas.add(circle)

    def source_extraction(self):
        sources = self.fits_array[0].extract(
            self.doubleSpinBoxSexSigma.value(),
            self.doubleSpinBoxSexMinimumArea.value()
        )
        coordinates = sources[["xcentroid", "ycentroid"]].to_numpy().tolist()

        self.parent.gui_functions.add_to_table(
            self.tableWidgetCoordinates,
            [[str(int(each)) for each in coord] for coord in coordinates]
        )
        self.draw_aperture()

    def daofind(self):
        sources = self.fits_array[0].daofind(
            self.doubleSpinBoxDAOFindSigma.value(),
            self.doubleSpinBoxDAOFindFWHM.value(),
            self.doubleSpinBoxDAOFindFWHM.value()
        )
        coordinates = sources[["xcentroid", "ycentroid"]].to_numpy().tolist()

        self.parent.gui_functions.add_to_table(
            self.tableWidgetCoordinates,
            [[str(int(each)) for each in coord] for coord in coordinates]
        )
        self.draw_aperture()

    def eventFilter(self, source, event):

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.canvas.set_pan(the_x, the_y)
                return True

            if event.button() == Qt.LeftButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.parent.gui_functions.add_to_table(
                    self.tableWidgetCoordinates,
                    [[int(the_x).__str__(), int(the_y).__str__()]]
                )
                self.draw_aperture()
                return True

        if event.type() == QtCore.QEvent.Wheel:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.current_angle += 1
                else:
                    self.current_angle -= 1

                self.current_angle %= 360
                self.canvas.rotate(self.current_angle)

                return True
            self.canvas.zoom_in(event.angleDelta().y() // 120)
            return True

        if event.type() == QtCore.QEvent.ContextMenu:
            if source is self.listWidgetApertureRadii:
                menu = QtWidgets.QMenu()
                menu.addAction("Remove",
                               lambda: (
                                   self.parent.gui_functions.remove_from_list(self.listWidgetApertureRadii),
                                   self.save_settings()
                               ))

                menu.exec_(event.globalPos())
                return True

            if source is self.tableWidgetCoordinates:
                menu = QtWidgets.QMenu()
                menu.addAction("Remove",
                               lambda: (
                                   self.parent.gui_functions.remove_from_table(self.tableWidgetCoordinates),
                                   self.draw_aperture()
                               ))

                menu.exec_(event.globalPos())
                return True

            if source is self.ginga_widget:
                menu = QtWidgets.QMenu()

                transform_menu = QtWidgets.QMenu('Transform')
                transform_menu.addAction('Reset', lambda: (
                    self.reset_transform(),
                    self.canvas.rotate(0),
                    self.canvas.zoom_fit()
                ))
                transform_menu.addSeparator()
                transform_flip_menu = QtWidgets.QMenu('Flip')
                transform_flip_menu.addAction('Reset', lambda: self.reset_transform())
                transform_flip_menu.addSeparator()
                transform_flip_menu.addAction('X', lambda: self.canvas.flip_x())
                transform_flip_menu.addAction('Y', lambda: self.canvas.flip_y())
                transform_flip_menu.addAction('Swap XY', lambda: self.canvas.swap_xy())

                transform_rotate_menu = QtWidgets.QMenu('Rotate')
                transform_rotate_menu.addAction('Reset', lambda: self.canvas.rotate(0))
                transform_rotate_menu.addSeparator()
                transform_rotate_menu.addAction('90', lambda: self.canvas.rotate(90))
                transform_rotate_menu.addAction('180', lambda: self.canvas.rotate(180))
                transform_rotate_menu.addAction('270', lambda: self.canvas.rotate(270))
                transform_rotate_menu.addAction('Custom', lambda: self.rotate())

                display_menu = QtWidgets.QMenu('Display')
                display_menu.addAction('Reset', lambda: (
                    self.canvas.set_color_algorithm('linear'),
                    self.canvas.restore_cmap(),
                    self.canvas.set_color_map('gray'),
                    self.canvas.restore_contrast(),
                    self.canvas.set_intensity_map('ramp')
                ))
                display_menu.addSeparator()
                display_scale_menu = QtWidgets.QMenu('Scale')
                display_scale_menu.addAction('Reset', lambda: self.canvas.set_color_algorithm('linear'))
                display_scale_menu.addSeparator()
                display_scale_menu.addAction('Linear', lambda: self.canvas.set_color_algorithm('linear'))
                display_scale_menu.addAction('Log', lambda: self.canvas.set_color_algorithm('log'))
                display_scale_menu.addAction('Power', lambda: self.canvas.set_color_algorithm('power'))
                display_scale_menu.addAction('Square Root', lambda: self.canvas.set_color_algorithm('sqrt'))
                display_scale_menu.addAction('Squared', lambda: self.canvas.set_color_algorithm('squared'))
                display_scale_menu.addAction('Inverse Hyperbolic Sine',
                                             lambda: self.canvas.set_color_algorithm('asinh'))
                display_scale_menu.addAction('Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('sinh'))
                display_scale_menu.addAction('Histogram Equalization',
                                             lambda: self.canvas.set_color_algorithm('histeq'))

                display_cmap_menu = QtWidgets.QMenu('Map')
                display_cmap_menu.addAction('Reset', lambda: (
                    self.canvas.restore_cmap(), self.canvas.set_color_map('gray')
                ))
                display_cmap_menu.addAction('Reverse', lambda: self.canvas.invert_cmap())
                display_cmap_menu.addSeparator()
                display_cmap_menu.addAction('Accent', lambda: self.canvas.set_color_map('Accent'))
                display_cmap_menu.addAction('Autumn', lambda: self.canvas.set_color_map('autumn'))
                display_cmap_menu.addAction('Blue', lambda: self.canvas.set_color_map('blue'))
                display_cmap_menu.addAction('Blues', lambda: self.canvas.set_color_map('Blues'))
                display_cmap_menu.addAction('Bone', lambda: self.canvas.set_color_map('bone'))
                display_cmap_menu.addAction('Color', lambda: self.canvas.set_color_map('color'))
                display_cmap_menu.addAction('Cool', lambda: self.canvas.set_color_map('cool'))
                display_cmap_menu.addAction('Cool Warm', lambda: self.canvas.set_color_map('coolwarm'))
                display_cmap_menu.addAction('Copper', lambda: self.canvas.set_color_map('copper'))
                display_cmap_menu.addAction('Cube Helix', lambda: self.canvas.set_color_map('cubehelix'))
                display_cmap_menu.addAction('Dark', lambda: self.canvas.set_color_map('Dark2'))
                display_cmap_menu.addAction('DS9', lambda: self.canvas.set_color_map('ds9_a'))
                display_cmap_menu.addAction('DS9 Cool', lambda: self.canvas.set_color_map('ds9_cool'))
                display_cmap_menu.addAction('DS9 He', lambda: self.canvas.set_color_map('ds9_he'))
                display_cmap_menu.addAction('Flag', lambda: self.canvas.set_color_map('flag'))
                display_cmap_menu.addAction('Gist Earth', lambda: self.canvas.set_color_map('gist_earth'))
                display_cmap_menu.addAction('Gist Gray', lambda: self.canvas.set_color_map('gist_gray'))
                display_cmap_menu.addAction('Gist Heat', lambda: self.canvas.set_color_map('gist_heat'))
                display_cmap_menu.addAction('Gist Ncar', lambda: self.canvas.set_color_map('gist_ncar'))
                display_cmap_menu.addAction('Gist Rainbow', lambda: self.canvas.set_color_map('gist_rainbow'))
                display_cmap_menu.addAction('Gist Stern', lambda: self.canvas.set_color_map('gist_stern'))
                display_cmap_menu.addAction('Gist Yarg', lambda: self.canvas.set_color_map('gist_yarg'))
                display_cmap_menu.addAction('GnBu', lambda: self.canvas.set_color_map('GnBu'))
                display_cmap_menu.addAction('Gnuplot', lambda: self.canvas.set_color_map('gnuplot'))
                display_cmap_menu.addAction('Gray Clip', lambda: self.canvas.set_color_map('grayclip'))
                display_cmap_menu.addAction('Gray', lambda: self.canvas.set_color_map('gray'))
                display_cmap_menu.addAction('Green', lambda: self.canvas.set_color_map('green'))
                display_cmap_menu.addAction('Greens', lambda: self.canvas.set_color_map('Greens'))
                display_cmap_menu.addAction('Light', lambda: self.canvas.set_color_map('light'))
                display_cmap_menu.addAction('Magma', lambda: self.canvas.set_color_map('magma'))
                display_cmap_menu.addAction('Nipy Spectral', lambda: self.canvas.set_color_map('nipy_spectral'))
                display_cmap_menu.addAction('Ocean', lambda: self.canvas.set_color_map('ocean'))
                display_cmap_menu.addAction('Oranges', lambda: self.canvas.set_color_map('Oranges'))
                display_cmap_menu.addAction('Paired', lambda: self.canvas.set_color_map('Paired'))
                display_cmap_menu.addAction('Pastel', lambda: self.canvas.set_color_map('pastel'))
                display_cmap_menu.addAction('Random', lambda: self.canvas.set_color_map('random'))
                display_cmap_menu.addAction('Winter', lambda: self.canvas.set_color_map('winter'))

                display_imap_menu = QtWidgets.QMenu('Intensity')
                display_imap_menu.addAction('Reset', lambda: (
                    self.canvas.set_intensity_map('ramp')
                ))
                display_imap_menu.addSeparator()
                display_imap_menu.addAction('Equa', lambda: self.canvas.set_intensity_map('equa'))
                display_imap_menu.addAction('Expo', lambda: self.canvas.set_intensity_map('expo'))
                display_imap_menu.addAction('Gamma', lambda: self.canvas.set_intensity_map('gamma'))
                display_imap_menu.addAction('Jigsaw', lambda: self.canvas.set_intensity_map('jigsaw'))
                display_imap_menu.addAction('Lasritt', lambda: self.canvas.set_intensity_map('lasritt'))
                display_imap_menu.addAction('Log', lambda: self.canvas.set_intensity_map('log'))
                display_imap_menu.addAction('Neg', lambda: self.canvas.set_intensity_map('neg'))
                display_imap_menu.addAction('NegLog', lambda: self.canvas.set_intensity_map('neglog'))
                display_imap_menu.addAction('Null', lambda: self.canvas.set_intensity_map('null'))
                display_imap_menu.addAction('Ramp', lambda: self.canvas.set_intensity_map('ramp'))
                display_imap_menu.addAction('Stairs', lambda: self.canvas.set_intensity_map('stairs'))
                display_imap_menu.addAction('UltraSmooth', lambda: self.canvas.set_intensity_map('ultrasmooth'))

                transform_menu.addMenu(transform_flip_menu)
                transform_menu.addMenu(transform_rotate_menu)

                display_menu.addMenu(display_scale_menu)
                display_menu.addMenu(display_cmap_menu)
                display_menu.addMenu(display_imap_menu)
                display_menu.addAction('Contrast', lambda: self.set_contrast())

                sextract_menu = QtWidgets.QMenu('SExtract')

                sextract_menu.addAction("SEP", lambda: self.source_extraction())
                sextract_menu.addAction("DAOFind", lambda: self.daofind())

                menu.addMenu(sextract_menu)
                menu.addSeparator()
                menu.addMenu(display_menu)
                menu.addMenu(transform_menu)

                menu.exec_(event.globalPos())
                return True

        return super().eventFilter(source, event)


# noinspection PyUnresolvedReferences
class ArithmeticForm(QWidget, Ui_FormArithmetic):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(ArithmeticForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.pushButtonGetFile.clicked.connect(self.get_operand)
        self.pushButtonGO.clicked.connect(self.go)

        self.pushButtonGetFile.installEventFilter(self)

        self.comboOperation.currentIndexChanged.connect(self.save_settings)
        self.doubleSpinBoxValue.valueChanged.connect(self.save_settings)
        self.load_settings()

    def load_settings(self):
        settings = self.parent.settings.settings
        self.comboOperation.setCurrentIndex(settings["operations"]["arithmetic"]["operation"])
        self.doubleSpinBoxValue.setValue(settings["operations"]["arithmetic"]["default_value"])

    def save_settings(self):
        settings = self.parent.settings.settings
        settings["operations"]["arithmetic"]["operation"] = self.comboOperation.currentIndex()
        settings["operations"]["arithmetic"]["default_value"] = self.doubleSpinBoxValue.value()

        self.parent.settings.settings = settings

    def add_from_files_tree(self, file_path_label):
        files = self.parent.gui_functions.get_selected_files(self.parent.treeWidget)
        files_data = []
        for grp, children in files.items():
            for child in children:
                files_data.append(
                    (Path(child.child(0).text(1)) / Path(child.text(0))).absolute().__str__()
                )

        the_file, ok = self.parent.gui_functions.get_item("Select A File", "File", files_data)
        if ok:
            file_path_label.setText(the_file)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu:
            if source is self.pushButtonGetFile:
                menu = QtWidgets.QMenu()
                menu.addAction("Add From list", lambda: self.add_from_files_tree(self.labelFile))
                menu.exec_(event.globalPos())

            return True

        return super(ArithmeticForm, self).eventFilter(source, event)

    def get_operand(self):
        file = self.parent.gui_functions.get_file("Get Operand")
        if file:
            self.labelFile.setText(file)

    def go(self):
        warn = 0
        if self.tabWidget.currentIndex() == 0:
            other = self.doubleSpinBoxValue.value()
        else:
            other_file = self.labelFile.text()
            if other_file == "":
                self.parent.gui_functions.error("No operand file was selected")
                return
            other = Fits.from_path(other_file)
        operator = self.comboOperation.currentText()

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Adding ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Operated"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                if operator == "+ Add":
                    new_fits = fits.add(
                        other, output=(Path(save_directory) / file_name).absolute().__str__(), override=True
                    )
                elif operator == "- Subtract":
                    new_fits = fits.sub(
                        other, output=(Path(save_directory) / file_name).absolute().__str__(), override=True
                    )
                elif operator == "* Multiply":
                    new_fits = fits.mul(
                        other, output=(Path(save_directory) / file_name).absolute().__str__(), override=True
                    )
                elif operator == "/ Divide":
                    new_fits = fits.div(
                        other, output=(Path(save_directory) / file_name).absolute().__str__(), override=True
                    )
                elif operator == "^ Power":
                    new_fits = fits.pow(
                        other, output=(Path(save_directory) / file_name).absolute().__str__(), override=True
                    )
                else:
                    new_fits = fits.mod(
                        other, output=(Path(save_directory) / file_name).absolute().__str__(), override=True
                    )

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)
            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")


# noinspection PyUnresolvedReferences
class CCDProcForm(QWidget, Ui_FormCCDPROC):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(CCDProcForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.pushButtonZeroFile.clicked.connect(self.set_zero)
        self.pushButtonZeroClear.clicked.connect(lambda: self.labelZeroFile.setText(""))
        self.pushButtonDarkFile.clicked.connect(self.set_dark)
        self.pushButtonDarkClear.clicked.connect(lambda: (self.labelDarkFile.setText(""), self.reset_exposure_header()))
        self.pushButtonFlatFile.clicked.connect(self.set_flat)
        self.pushButtonFlatClear.clicked.connect(lambda: self.labelFlatFile.setText(""))

        self.pushButtonZeroShow.clicked.connect(lambda: self.show_image(self.labelZeroFile))
        self.pushButtonDarkShow.clicked.connect(lambda: self.show_image(self.labelDarkFile))
        self.pushButtonFlatShow.clicked.connect(lambda: self.show_image(self.labelFlatFile))

        self.pushButtonGO.clicked.connect(self.go)

        self.pushButtonZeroFile.installEventFilter(self)
        self.pushButtonDarkFile.installEventFilter(self)
        self.pushButtonFlatFile.installEventFilter(self)

        self.load_settings()

        self.comboBoxExposureHeader.currentIndexChanged.connect(self.save_settings)
        self.checkBoxForce.stateChanged.connect(self.save_settings)

    def load_settings(self):
        settings = self.parent.settings.settings
        try:
            self.comboBoxExposureHeader.setCurrentText(settings["operations"]["ccdproc"]["exposure"])
        except Exception as _:
            self.parent.logger.warning("Cannot set exposure header. Setting to default.")
            self.comboBoxExposureHeader.setCurrentText("None")

        self.checkBoxForce.setChecked(settings["operations"]["ccdproc"]["force"])

    def save_settings(self):
        settings = self.parent.settings.settings
        settings["operations"]["ccdproc"]["exposure"] = self.comboBoxExposureHeader.currentText()
        settings["operations"]["ccdproc"]["force"] = self.checkBoxForce.isChecked()

        self.parent.settings.settings = settings

    def reset_exposure_header(self):
        self.comboBoxExposureHeader.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxExposureHeader, ["None"])

    def add_from_files_tree(self, file_path_label):
        files = self.parent.gui_functions.get_selected_files(self.parent.treeWidget)
        files_data = []
        for grp, children in files.items():
            for child in children:
                files_data.append(
                    (Path(child.child(0).text(1)) / Path(child.text(0))).absolute().__str__()
                )

        the_file, ok = self.parent.gui_functions.get_item("Select A File", "File", files_data)
        if ok:
            file_path_label.setText(the_file)
            if file_path_label is self.labelDarkFile:
                self.reload_exposure_header(the_file)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu:
            if source is self.pushButtonZeroFile:
                menu = QtWidgets.QMenu()
                menu.addAction("Add From list", lambda: self.add_from_files_tree(self.labelZeroFile))
                menu.exec_(event.globalPos())

            if source is self.pushButtonDarkFile:
                menu = QtWidgets.QMenu()
                menu.addAction("Add From list", lambda: self.add_from_files_tree(self.labelDarkFile))
                menu.exec_(event.globalPos())

            if source is self.pushButtonFlatFile:
                menu = QtWidgets.QMenu()
                menu.addAction("Add From list", lambda: self.add_from_files_tree(self.labelFlatFile))
                menu.exec_(event.globalPos())

            return True

        return super(CCDProcForm, self).eventFilter(source, event)

    def go(self):
        warn = 0

        master_zero = self.labelZeroFile.text()
        master_dark = self.labelDarkFile.text()
        master_flat = self.labelFlatFile.text()

        if master_zero == "" and master_dark == "" and master_flat == "":
            self.parent.gui_functions.error("No action")
            return

        force = self.checkBoxForce.isChecked()
        exposure_header = self.comboBoxExposureHeader.currentText()

        if exposure_header == "None":
            exposure = None
        else:
            exposure = exposure_header

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Calibrating ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Calibrated"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(save_directory) / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = Fits.from_data_header(fits.data(), fits.pure_header(), file_name.__str__())

                if master_zero:
                    new_fits = new_fits.zero_correction(
                        Fits.from_path(master_zero), output=new_fits.file.absolute().__str__(),
                        override=True, force=force,
                    )

                if master_dark:
                    new_fits = new_fits.dark_correction(
                        Fits.from_path(master_dark), exposure=exposure,
                        output=new_fits.file.absolute().__str__(), override=True, force=force
                    )

                if master_flat:
                    new_fits = new_fits.flat_correction(
                        Fits.from_path(master_flat), output=new_fits.file.absolute().__str__()
                        , override=True, force=force
                    )

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def show_image(self, file_label):
        file = file_label.text()
        if file == "":
            self.parent.gui_functions.error("Nothing to show")
            return

        fits = Fits.from_path(file)
        self.parent.show_window(DisplayForm(self.parent, FitsArray([fits])))

    def set_zero(self):
        file = self.parent.gui_functions.get_file("Zero File")
        if file:
            self.labelZeroFile.setText(file)

    def set_dark(self):
        file = self.parent.gui_functions.get_file("Dark File")
        if file:
            self.labelDarkFile.setText(file)
            self.reload_exposure_header(file)

    def reload_exposure_header(self, file):
        dark_fits = Fits.from_path(file)
        self.reset_exposure_header()
        self.parent.gui_functions.add_to_combo(self.comboBoxExposureHeader, list(dark_fits.header().columns))

    def set_flat(self):
        file = self.parent.gui_functions.get_file("Flat File")
        if file:
            self.labelFlatFile.setText(file)


# noinspection PyUnresolvedReferences
class HeditForm(QWidget, Ui_FormHedit):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(HeditForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.set_header()

        self.checkBoxUseFromValue.stateChanged.connect(self.toggle)
        self.tableWidgetHeaders.clicked.connect(self.get_header)
        self.pushButtonSaveUpdate.clicked.connect(self.save_update)
        self.pushButtonDelete.clicked.connect(self.delete_header)

    def set_header(self):
        header = self.fits_array[0].pure_header()
        data = []
        for key in header:
            if key not in ['COMMENT', 'HISTORY']:
                data.append([key, header[key], header.comments[key]])

        self.parent.gui_functions.clear_table(self.tableWidgetHeaders)
        self.parent.gui_functions.add_to_table(self.tableWidgetHeaders, data)
        self.comboBoxValue.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxValue,
                                               [f"{each[0]} = {each[1].__str__()[:12]}" for each in data])

    def delete_header(self):
        warn = 0
        key = self.lineEditKey.text()

        progress = QtWidgets.QProgressDialog("Deleting Header ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                fits.hedit(key, delete=True)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        self.set_header()

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def save_update(self):
        warn = 0
        is_key = self.checkBoxUseFromValue.isChecked()
        key = self.lineEditKey.text()
        if is_key:
            value = self.comboBoxValue.currentText().split("=")[0].strip()
        else:
            value = self.lineEditValue.text()
        comment = self.lineEditComment.text()

        if key.strip() == "":
            self.parent.gun_functions.error("No key was given")
            return

        progress = QtWidgets.QProgressDialog("Editing Header ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)
        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                fits.hedit(key, value, comment, value_is_key=is_key)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        self.set_header()

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def toggle(self):
        enabled = self.checkBoxUseFromValue.isChecked()
        self.lineEditValue.setEnabled(not enabled)
        self.comboBoxValue.setEnabled(enabled)

    def get_header(self):
        current_row = self.tableWidgetHeaders.currentRow()

        key = self.tableWidgetHeaders.item(current_row, 0).text()
        value = self.tableWidgetHeaders.item(current_row, 1).text()
        comment = self.tableWidgetHeaders.item(current_row, 2).text()

        self.lineEditKey.setText(key)
        self.lineEditValue.setText(value)
        self.lineEditComment.setText(comment)


# noinspection PyUnresolvedReferences
class CosmicCleanerForm(QWidget, Ui_FormCosmicCleaner):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(CosmicCleanerForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.pushButtonGO.clicked.connect(self.go)

        self.doubleSpinSigclip.valueChanged.connect(self.save_settings)
        self.doubleSpinSigfrac.valueChanged.connect(self.save_settings)
        self.doubleSpinObjlim.valueChanged.connect(self.save_settings)
        self.doubleSpinGain.valueChanged.connect(self.save_settings)
        self.doubleSpinReadnoise.valueChanged.connect(self.save_settings)
        self.doubleSpinSatlevel.valueChanged.connect(self.save_settings)
        self.spinBoxNiter.valueChanged.connect(self.save_settings)
        self.checkBoxSepmed.stateChanged.connect(self.save_settings)
        self.comboBoxCleantype.currentIndexChanged.connect(self.save_settings)
        self.comboBoxFsmode.currentIndexChanged.connect(self.save_settings)
        self.comboBoxPsfmodel.currentIndexChanged.connect(self.save_settings)
        self.doubleSpinPsffwhm.valueChanged.connect(self.save_settings)
        self.spinBoxPsfsize.valueChanged.connect(self.save_settings)
        self.doubleSpinPsfbeta.valueChanged.connect(self.save_settings)
        self.checkBoxGain_apply.stateChanged.connect(self.save_settings)
        self.load_settings()

    def load_settings(self):
        settings = self.parent.settings.settings
        self.doubleSpinSigclip.setValue(settings["edit"]["cosmic_clean"]["sigclip"])
        self.doubleSpinSigfrac.setValue(settings["edit"]["cosmic_clean"]["sigfrac"])
        self.doubleSpinObjlim.setValue(settings["edit"]["cosmic_clean"]["objlim"])
        self.doubleSpinGain.setValue(settings["edit"]["cosmic_clean"]["gain"])
        self.doubleSpinReadnoise.setValue(settings["edit"]["cosmic_clean"]["readnoise"])
        self.doubleSpinSatlevel.setValue(settings["edit"]["cosmic_clean"]["satlevel"])
        self.spinBoxNiter.setValue(settings["edit"]["cosmic_clean"]["niter"])
        self.checkBoxSepmed.setChecked(settings["edit"]["cosmic_clean"]["sepmed"])
        self.comboBoxCleantype.setCurrentIndex(settings["edit"]["cosmic_clean"]["cleantype"])
        self.comboBoxFsmode.setCurrentIndex(settings["edit"]["cosmic_clean"]["fsmode"])
        self.comboBoxPsfmodel.setCurrentIndex(settings["edit"]["cosmic_clean"]["psfmodel"])
        self.doubleSpinPsffwhm.setValue(settings["edit"]["cosmic_clean"]["psffwhm"])
        self.spinBoxPsfsize.setValue(settings["edit"]["cosmic_clean"]["psfsize"])
        self.doubleSpinPsfbeta.setValue(settings["edit"]["cosmic_clean"]["psfbeta"])
        self.checkBoxGain_apply.setChecked(settings["edit"]["cosmic_clean"]["gain_apply"])

    def save_settings(self):
        settings = self.parent.settings.settings
        settings["edit"]["cosmic_clean"]["sigclip"] = self.doubleSpinSigclip.value()
        settings["edit"]["cosmic_clean"]["sigfrac"] = self.doubleSpinSigfrac.value()
        settings["edit"]["cosmic_clean"]["objlim"] = self.doubleSpinObjlim.value()
        settings["edit"]["cosmic_clean"]["gain"] = self.doubleSpinGain.value()
        settings["edit"]["cosmic_clean"]["readnoise"] = self.doubleSpinReadnoise.value()
        settings["edit"]["cosmic_clean"]["satlevel"] = self.doubleSpinSatlevel.value()
        settings["edit"]["cosmic_clean"]["niter"] = self.spinBoxNiter.value()
        settings["edit"]["cosmic_clean"]["sepmed"] = self.checkBoxSepmed.isChecked()
        settings["edit"]["cosmic_clean"]["cleantype"] = self.comboBoxCleantype.currentIndex()
        settings["edit"]["cosmic_clean"]["fsmode"] = self.comboBoxFsmode.currentIndex()
        settings["edit"]["cosmic_clean"]["psfmodel"] = self.comboBoxPsfmodel.currentIndex()
        settings["edit"]["cosmic_clean"]["psffwhm"] = self.doubleSpinPsffwhm.value()
        settings["edit"]["cosmic_clean"]["psfsize"] = self.spinBoxPsfsize.value()
        settings["edit"]["cosmic_clean"]["psfbeta"] = self.doubleSpinPsfbeta.value()
        settings["edit"]["cosmic_clean"]["gain_apply"] = self.checkBoxGain_apply.isChecked()

        self.parent.settings.settings = settings

    def go(self):
        warn = 0

        sigclip = self.doubleSpinSigclip.value()
        sigfrac = self.doubleSpinSigfrac.value()
        objlim = self.doubleSpinObjlim.value()
        gain = self.doubleSpinGain.value()
        readnoise = self.doubleSpinReadnoise.value()
        satlevel = self.doubleSpinSatlevel.value()
        niter = self.spinBoxNiter.value()
        sepmed = self.checkBoxSepmed.isChecked()
        cleantype = self.comboBoxCleantype.currentText()
        fsmode = self.comboBoxFsmode.currentText()
        psfmodel = self.comboBoxPsfmodel.currentText()
        psffwhm = self.doubleSpinPsffwhm.value()
        psfsize = self.spinBoxPsfsize.value()
        psfbeta = self.doubleSpinPsfbeta.value()
        gain_apply = self.checkBoxGain_apply.isChecked()

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Cleaning ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Cleaned"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(save_directory) / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.cosmic_clean(
                    sigclip=sigclip, sigfrac=sigfrac, objlim=objlim, gain=gain, readnoise=readnoise,
                    satlevel=satlevel,
                    niter=niter, sepmed=sepmed, cleantype=cleantype, fsmode=fsmode, psfmodel=psfmodel,
                    psffwhm=psffwhm, psfsize=psfsize, psfbeta=psfbeta, gain_apply=gain_apply,
                    output=file_name.absolute().__str__(), override=True
                )

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)
            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")


# noinspection PyUnresolvedReferences
class StatisticsForm(QWidget, Ui_FormStatics):
    def __init__(self, parent: MainWindow, stats: List):
        super(StatisticsForm, self).__init__(parent)
        self.parent = parent
        self.stats = stats
        self.setupUi(self)

        self.load()

    def load(self):
        self.parent.gui_functions.add_to_table(self.tableWidgetStats, self.stats)


# noinspection PyUnresolvedReferences
class HSelectForm(QWidget, Ui_FormHSelect):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(HSelectForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.load()

        self.pushButtonExport.clicked.connect(self.export)

    def export(self):
        file = self.parent.gui_functions.save_file("Export HSelect", "Comma Seperated Values (*.csv)")
        if file:
            header = self.parent.gui_functions.get_from_table_selected(self.tableWidgetHeaders)
            table = self.fits_array.hselect([h[0] for h in header])
            table.to_csv(file, index=True)

    def load(self):
        fits = self.fits_array[0]
        header = fits.pure_header()
        data = []
        for key in header:
            if key not in ['COMMENT', 'HISTORY']:
                data.append([key, header[key], header.comments[key]])

        self.parent.gui_functions.clear_table(self.tableWidgetHeaders)
        self.parent.gui_functions.add_to_table(self.tableWidgetHeaders, data)


# noinspection PyUnresolvedReferences
class HeaderForm(QWidget, Ui_FormHeader):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(HeaderForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)
        self.set_files()

        self.setWindowIcon(QIcon(LOGO))

        self.display_header()
        self.listWidgetFiles.clicked.connect(self.display_header)

    def display_header(self):
        selected = self.listWidgetFiles.selectionModel().currentIndex().row()
        fits = self.fits_array[selected]
        header = fits.pure_header()
        data = []
        for key in header:
            if key not in ['COMMENT', 'HISTORY']:
                data.append([key, header[key], header.comments[key]])

        self.parent.gui_functions.clear_table(self.tableWidgetHeaders)
        self.parent.gui_functions.add_to_table(self.tableWidgetHeaders, data)

    def set_files(self):
        self.parent.gui_functions.add_to_list(self.listWidgetFiles,
                                              [each.file.absolute().name for each in self.fits_array])
        self.listWidgetFiles.item(0).setSelected(True)


# noinspection PyUnresolvedReferences
class ShiftForm(QWidget, Ui_FormShift):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(ShiftForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.canvas = CanvasView(render='widget')
        self.canvas.enable_autocuts('on')
        self.canvas.set_autocut_params('zscale')
        self.canvas.enable_autozoom('on')
        self.canvas.set_bg(0.2, 0.2, 0.2)
        self.canvas.ui_set_active(True)

        group_box_layout = QVBoxLayout()
        self.ginga_widget = self.canvas.get_widget()
        group_box_layout.addWidget(self.ginga_widget)
        self.groupBox.setLayout(group_box_layout)
        self.img = AstroImage(logger=self.parent.logger)
        self.img.load_data(self.fits_array[0].data())
        self.canvas.set_image(self.img)

        self.ginga_widget.installEventFilter(self)

        self.set_amount_table()
        self.iteration = 0
        self.current_angle = 0

        self.tableWidgetAmount.selectRow(self.iteration)
        self.reset_transform()

        self.tableWidgetAmount.clicked.connect(self.set_current)
        self.pushButtonGo.clicked.connect(self.go)

    def go(self):
        warn = 0

        ref = self.tableWidgetAmount.currentRow()

        ref_x = self.tableWidgetAmount.item(ref, 1).text()
        ref_y = self.tableWidgetAmount.item(ref, 2).text()

        amounts = self.parent.gui_functions.get_from_table(self.tableWidgetAmount)

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Shifting ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Shifted"])

        for iteration, (fits, (_, x, y)) in enumerate(zip(self.fits_array, amounts)):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(save_directory) / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.shift(int(float(x) - float(ref_x)), int(float(y) - float(ref_y)),
                                      output=file_name.absolute().__str__())

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def draw_aperture(self):

        current_row = self.tableWidgetAmount.currentRow()
        x = self.tableWidgetAmount.item(current_row, 1).text()
        y = self.tableWidgetAmount.item(current_row, 2).text()
        del self.canvas.canvas.objects[1:]
        try:
            x = float(x)
            y = float(y)
        except Exception as e:
            self.parent.logger.warning(e)
            return

        circle = Circle(x, y, 25, "red", 5)
        self.canvas.canvas.add(circle)

        circle = Circle(x, y, 35, "blue", 5)
        self.canvas.canvas.add(circle)

    def set_current(self):
        self.iteration = self.tableWidgetAmount.selectionModel().currentIndex().row()
        self.img.load_data(self.fits_array[self.iteration].data())
        self.tableWidgetAmount.selectRow(self.iteration)
        self.draw_aperture()

    def go_next(self):
        self.iteration += 1

        if self.iteration == self.tableWidgetAmount.rowCount():
            self.iteration = 0
            self.parent.gui_functions.warning("End of list")

        self.img.load_data(self.fits_array[self.iteration].data())
        self.tableWidgetAmount.selectRow(self.iteration)
        self.draw_aperture()

    def set_amount_table(self):
        self.parent.gui_functions.clear_table(self.tableWidgetAmount)
        self.parent.gui_functions.add_to_table(
            self.tableWidgetAmount,
            [[each.file.absolute().name, "", ""] for each in self.fits_array]
        )

    def rotate(self):
        angle, ok = self.parent.gui_functions.get_number("Angle", "Please provide angle to rotate", 0, 360)
        if ok:
            try:
                self.current_angle = float(angle)
                self.canvas.rotate(self.current_angle)
            except Exception as e:
                self.logger.warning(e)

    def reset_transform(self):
        x, y, swap = self.canvas.get_transforms()
        if x:
            self.canvas.flip_x()
        if y:
            self.canvas.flip_y()
        if swap:
            self.canvas.swap_xy()

    def set_contrast(self):
        number, ok = self.parent.gui_functions.get_number("Contrast", "Please provide contrast")
        if ok:
            self.canvas.set_contrast(number / 100)

    def reset(self):
        self.reset_transform()
        self.canvas.rotate(0)
        self.canvas.zoom_fit()
        self.canvas.set_color_algorithm('linear')
        self.canvas.restore_cmap()
        self.canvas.set_color_map('gray')
        self.canvas.restore_contrast()
        self.canvas.set_intensity_map('ramp')

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.canvas.set_pan(the_x, the_y)
                return True
            if event.button() == Qt.LeftButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.tableWidgetAmount.setItem(self.iteration, 1, QTableWidgetItem(the_x.__str__()))
                self.tableWidgetAmount.setItem(self.iteration, 2, QTableWidgetItem(the_y.__str__()))
                self.go_next()
                return True

        if QtCore.QEvent.Wheel == event.type():
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.current_angle += 1
                else:
                    self.current_angle -= 1

                self.current_angle %= 360
                self.canvas.rotate(self.current_angle)

                return True
            self.canvas.zoom_in(event.angleDelta().y() // 120)
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.ginga_widget:
            menu = QtWidgets.QMenu()

            transform_menu = QtWidgets.QMenu('Transform')
            transform_menu.addAction('Reset', lambda: (
                self.reset_transform(),
                self.canvas.rotate(0),
                self.canvas.zoom_fit()
            ))
            transform_menu.addSeparator()
            transform_flip_menu = QtWidgets.QMenu('Flip')
            transform_flip_menu.addAction('Reset', lambda: self.reset_transform())
            transform_flip_menu.addSeparator()
            transform_flip_menu.addAction('X', lambda: self.canvas.flip_x())
            transform_flip_menu.addAction('Y', lambda: self.canvas.flip_y())
            transform_flip_menu.addAction('Swap XY', lambda: self.canvas.swap_xy())

            transform_rotate_menu = QtWidgets.QMenu('Rotate')
            transform_rotate_menu.addAction('Reset', lambda: self.canvas.rotate(0))
            transform_rotate_menu.addSeparator()
            transform_rotate_menu.addAction('90', lambda: self.canvas.rotate(90))
            transform_rotate_menu.addAction('180', lambda: self.canvas.rotate(180))
            transform_rotate_menu.addAction('270', lambda: self.canvas.rotate(270))
            transform_rotate_menu.addAction('Custom', lambda: self.rotate())

            display_menu = QtWidgets.QMenu('Display')
            display_menu.addAction('Reset', lambda: (
                self.canvas.set_color_algorithm('linear'),
                self.canvas.restore_cmap(),
                self.canvas.set_color_map('gray'),
                self.canvas.restore_contrast(),
                self.canvas.set_intensity_map('ramp')
            ))
            display_menu.addSeparator()
            display_scale_menu = QtWidgets.QMenu('Scale')
            display_scale_menu.addAction('Reset', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addSeparator()
            display_scale_menu.addAction('Linear', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addAction('Log', lambda: self.canvas.set_color_algorithm('log'))
            display_scale_menu.addAction('Power', lambda: self.canvas.set_color_algorithm('power'))
            display_scale_menu.addAction('Square Root', lambda: self.canvas.set_color_algorithm('sqrt'))
            display_scale_menu.addAction('Squared', lambda: self.canvas.set_color_algorithm('squared'))
            display_scale_menu.addAction('Inverse Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('asinh'))
            display_scale_menu.addAction('Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('sinh'))
            display_scale_menu.addAction('Histogram Equalization', lambda: self.canvas.set_color_algorithm('histeq'))

            display_cmap_menu = QtWidgets.QMenu('Map')
            display_cmap_menu.addAction('Reset', lambda: (
                self.canvas.restore_cmap(), self.canvas.set_color_map('gray')
            ))
            display_cmap_menu.addAction('Reverse', lambda: self.canvas.invert_cmap())
            display_cmap_menu.addSeparator()
            display_cmap_menu.addAction('Accent', lambda: self.canvas.set_color_map('Accent'))
            display_cmap_menu.addAction('Autumn', lambda: self.canvas.set_color_map('autumn'))
            display_cmap_menu.addAction('Blue', lambda: self.canvas.set_color_map('blue'))
            display_cmap_menu.addAction('Blues', lambda: self.canvas.set_color_map('Blues'))
            display_cmap_menu.addAction('Bone', lambda: self.canvas.set_color_map('bone'))
            display_cmap_menu.addAction('Color', lambda: self.canvas.set_color_map('color'))
            display_cmap_menu.addAction('Cool', lambda: self.canvas.set_color_map('cool'))
            display_cmap_menu.addAction('Cool Warm', lambda: self.canvas.set_color_map('coolwarm'))
            display_cmap_menu.addAction('Copper', lambda: self.canvas.set_color_map('copper'))
            display_cmap_menu.addAction('Cube Helix', lambda: self.canvas.set_color_map('cubehelix'))
            display_cmap_menu.addAction('Dark', lambda: self.canvas.set_color_map('Dark2'))
            display_cmap_menu.addAction('DS9', lambda: self.canvas.set_color_map('ds9_a'))
            display_cmap_menu.addAction('DS9 Cool', lambda: self.canvas.set_color_map('ds9_cool'))
            display_cmap_menu.addAction('DS9 He', lambda: self.canvas.set_color_map('ds9_he'))
            display_cmap_menu.addAction('Flag', lambda: self.canvas.set_color_map('flag'))
            display_cmap_menu.addAction('Gist Earth', lambda: self.canvas.set_color_map('gist_earth'))
            display_cmap_menu.addAction('Gist Gray', lambda: self.canvas.set_color_map('gist_gray'))
            display_cmap_menu.addAction('Gist Heat', lambda: self.canvas.set_color_map('gist_heat'))
            display_cmap_menu.addAction('Gist Ncar', lambda: self.canvas.set_color_map('gist_ncar'))
            display_cmap_menu.addAction('Gist Rainbow', lambda: self.canvas.set_color_map('gist_rainbow'))
            display_cmap_menu.addAction('Gist Stern', lambda: self.canvas.set_color_map('gist_stern'))
            display_cmap_menu.addAction('Gist Yarg', lambda: self.canvas.set_color_map('gist_yarg'))
            display_cmap_menu.addAction('GnBu', lambda: self.canvas.set_color_map('GnBu'))
            display_cmap_menu.addAction('Gnuplot', lambda: self.canvas.set_color_map('gnuplot'))
            display_cmap_menu.addAction('Gray Clip', lambda: self.canvas.set_color_map('grayclip'))
            display_cmap_menu.addAction('Gray', lambda: self.canvas.set_color_map('gray'))
            display_cmap_menu.addAction('Green', lambda: self.canvas.set_color_map('green'))
            display_cmap_menu.addAction('Greens', lambda: self.canvas.set_color_map('Greens'))
            display_cmap_menu.addAction('Light', lambda: self.canvas.set_color_map('light'))
            display_cmap_menu.addAction('Magma', lambda: self.canvas.set_color_map('magma'))
            display_cmap_menu.addAction('Nipy Spectral', lambda: self.canvas.set_color_map('nipy_spectral'))
            display_cmap_menu.addAction('Ocean', lambda: self.canvas.set_color_map('ocean'))
            display_cmap_menu.addAction('Oranges', lambda: self.canvas.set_color_map('Oranges'))
            display_cmap_menu.addAction('Paired', lambda: self.canvas.set_color_map('Paired'))
            display_cmap_menu.addAction('Pastel', lambda: self.canvas.set_color_map('pastel'))
            display_cmap_menu.addAction('Random', lambda: self.canvas.set_color_map('random'))
            display_cmap_menu.addAction('Winter', lambda: self.canvas.set_color_map('winter'))

            display_imap_menu = QtWidgets.QMenu('Intensity')
            display_imap_menu.addAction('Reset', lambda: (
                self.canvas.set_intensity_map('ramp')
            ))
            display_imap_menu.addSeparator()
            display_imap_menu.addAction('Equa', lambda: self.canvas.set_intensity_map('equa'))
            display_imap_menu.addAction('Expo', lambda: self.canvas.set_intensity_map('expo'))
            display_imap_menu.addAction('Gamma', lambda: self.canvas.set_intensity_map('gamma'))
            display_imap_menu.addAction('Jigsaw', lambda: self.canvas.set_intensity_map('jigsaw'))
            display_imap_menu.addAction('Lasritt', lambda: self.canvas.set_intensity_map('lasritt'))
            display_imap_menu.addAction('Log', lambda: self.canvas.set_intensity_map('log'))
            display_imap_menu.addAction('Neg', lambda: self.canvas.set_intensity_map('neg'))
            display_imap_menu.addAction('NegLog', lambda: self.canvas.set_intensity_map('neglog'))
            display_imap_menu.addAction('Null', lambda: self.canvas.set_intensity_map('null'))
            display_imap_menu.addAction('Ramp', lambda: self.canvas.set_intensity_map('ramp'))
            display_imap_menu.addAction('Stairs', lambda: self.canvas.set_intensity_map('stairs'))
            display_imap_menu.addAction('UltraSmooth', lambda: self.canvas.set_intensity_map('ultrasmooth'))

            transform_menu.addMenu(transform_flip_menu)
            transform_menu.addMenu(transform_rotate_menu)

            display_menu.addMenu(display_scale_menu)
            display_menu.addMenu(display_cmap_menu)
            display_menu.addMenu(display_imap_menu)
            display_menu.addAction('Contrast', lambda: self.set_contrast())

            menu.addSeparator()

            menu.addMenu(display_menu)
            menu.addMenu(transform_menu)

            menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)


# noinspection PyUnresolvedReferences
class RotateForm(QWidget, Ui_FormRotate):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(RotateForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.canvas = CanvasView(render='widget')
        self.canvas.enable_autocuts('on')
        self.canvas.set_autocut_params('zscale')
        self.canvas.enable_autozoom('on')
        self.canvas.set_bg(0.2, 0.2, 0.2)
        self.canvas.ui_set_active(True)

        group_box_layout = QVBoxLayout()
        self.ginga_widget = self.canvas.get_widget()
        group_box_layout.addWidget(self.ginga_widget)
        self.groupBox.setLayout(group_box_layout)
        self.img = AstroImage(logger=self.parent.logger)
        self.img.load_data(self.fits_array[0].data())
        self.canvas.set_image(self.img)

        self.current_angle = 0
        self.iteration = 0

        self.ginga_widget.installEventFilter(self)

        self.start = None

        self.set_amount_table()

        self.tableWidgetAmount.clicked.connect(self.set_current)
        self.pushButtonGo.clicked.connect(self.go)

    def go(self):
        warn = 0

        amounts = self.parent.gui_functions.get_from_table(self.tableWidgetAmount)

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Rotating ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Rotated"])

        for iteration, (fits, (_, angle)) in enumerate(zip(self.fits_array, amounts)):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(save_directory) / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.rotate(
                    math.radians(-float(angle)), output=file_name.absolute().__str__(), override=True
                )

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def rerotate(self):
        current_row = self.tableWidgetAmount.currentRow()
        angle = self.tableWidgetAmount.item(current_row, 1).text()
        try:
            angle = float(angle)
        except Exception as e:
            self.parent.logger.warning(e)
            return

        self.canvas.rotate(angle)

    def set_current(self):
        self.iteration = self.tableWidgetAmount.selectionModel().currentIndex().row()
        self.img.load_data(self.fits_array[self.iteration].data())
        self.tableWidgetAmount.selectRow(self.iteration)
        self.rerotate()

    def go_next(self):
        self.iteration += 1

        if self.iteration == self.tableWidgetAmount.rowCount():
            self.iteration = 0
            self.parent.gui_functions.warning("End of list")

        self.img.load_data(self.fits_array[self.iteration].data())
        self.tableWidgetAmount.selectRow(self.iteration)
        self.rerotate()

    def set_amount_table(self):
        self.parent.gui_functions.clear_table(self.tableWidgetAmount)
        self.parent.gui_functions.add_to_table(
            self.tableWidgetAmount,
            [[each.file.absolute().name, ""] for each in self.fits_array]
        )

    def reset_transform(self):
        x, y, swap = self.canvas.get_transforms()
        if x:
            self.canvas.flip_x()
        if y:
            self.canvas.flip_y()
        if swap:
            self.canvas.swap_xy()

    def set_contrast(self):
        number, ok = self.parent.gui_functions.get_number("Contrast", "Please provide contrast")
        if ok:
            self.canvas.set_contrast(number / 100)

    def reset(self):
        self.reset_transform()
        self.canvas.rotate(0)
        self.canvas.zoom_fit()
        self.canvas.set_color_algorithm('linear')
        self.canvas.restore_cmap()
        self.canvas.set_color_map('gray')
        self.canvas.restore_contrast()
        self.canvas.set_intensity_map('ramp')

    def eventFilter(self, source, event):

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.canvas.set_pan(the_x, the_y)
                return True

            if event.button() == Qt.LeftButton:
                rot = self.canvas.get_rotation()
                self.tableWidgetAmount.setItem(self.iteration, 1, QTableWidgetItem(rot.__str__()))
                self.go_next()

        if event.type() == QtCore.QEvent.Wheel:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.current_angle += 1
                else:
                    self.current_angle -= 1

                self.current_angle %= 360
                self.canvas.rotate(self.current_angle)

                return True
            self.canvas.zoom_in(event.angleDelta().y() // 120)
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.ginga_widget:
            menu = QtWidgets.QMenu()

            transform_menu = QtWidgets.QMenu('Transform')
            transform_menu.addAction('Reset', lambda: (
                self.reset_transform(),
                self.canvas.rotate(0),
                self.canvas.zoom_fit()
            ))
            transform_menu.addSeparator()
            transform_flip_menu = QtWidgets.QMenu('Flip')
            transform_flip_menu.addAction('Reset', lambda: self.reset_transform())
            transform_flip_menu.addSeparator()
            transform_flip_menu.addAction('X', lambda: self.canvas.flip_x())
            transform_flip_menu.addAction('Y', lambda: self.canvas.flip_y())
            transform_flip_menu.addAction('Swap XY', lambda: self.canvas.swap_xy())

            transform_rotate_menu = QtWidgets.QMenu('Rotate')
            transform_rotate_menu.addAction('Reset', lambda: self.canvas.rotate(0))
            transform_rotate_menu.addSeparator()
            transform_rotate_menu.addAction('90', lambda: self.canvas.rotate(90))
            transform_rotate_menu.addAction('180', lambda: self.canvas.rotate(180))
            transform_rotate_menu.addAction('270', lambda: self.canvas.rotate(270))
            transform_rotate_menu.addAction('Custom', lambda: self.rotate())

            display_menu = QtWidgets.QMenu('Display')
            display_menu.addAction('Reset', lambda: (
                self.canvas.set_color_algorithm('linear'),
                self.canvas.restore_cmap(),
                self.canvas.set_color_map('gray'),
                self.canvas.restore_contrast(),
                self.canvas.set_intensity_map('ramp')
            ))
            display_menu.addSeparator()
            display_scale_menu = QtWidgets.QMenu('Scale')
            display_scale_menu.addAction('Reset', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addSeparator()
            display_scale_menu.addAction('Linear', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addAction('Log', lambda: self.canvas.set_color_algorithm('log'))
            display_scale_menu.addAction('Power', lambda: self.canvas.set_color_algorithm('power'))
            display_scale_menu.addAction('Square Root', lambda: self.canvas.set_color_algorithm('sqrt'))
            display_scale_menu.addAction('Squared', lambda: self.canvas.set_color_algorithm('squared'))
            display_scale_menu.addAction('Inverse Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('asinh'))
            display_scale_menu.addAction('Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('sinh'))
            display_scale_menu.addAction('Histogram Equalization', lambda: self.canvas.set_color_algorithm('histeq'))

            display_cmap_menu = QtWidgets.QMenu('Map')
            display_cmap_menu.addAction('Reset', lambda: (
                self.canvas.restore_cmap(), self.canvas.set_color_map('gray')
            ))
            display_cmap_menu.addAction('Reverse', lambda: self.canvas.invert_cmap())
            display_cmap_menu.addSeparator()
            display_cmap_menu.addAction('Accent', lambda: self.canvas.set_color_map('Accent'))
            display_cmap_menu.addAction('Autumn', lambda: self.canvas.set_color_map('autumn'))
            display_cmap_menu.addAction('Blue', lambda: self.canvas.set_color_map('blue'))
            display_cmap_menu.addAction('Blues', lambda: self.canvas.set_color_map('Blues'))
            display_cmap_menu.addAction('Bone', lambda: self.canvas.set_color_map('bone'))
            display_cmap_menu.addAction('Color', lambda: self.canvas.set_color_map('color'))
            display_cmap_menu.addAction('Cool', lambda: self.canvas.set_color_map('cool'))
            display_cmap_menu.addAction('Cool Warm', lambda: self.canvas.set_color_map('coolwarm'))
            display_cmap_menu.addAction('Copper', lambda: self.canvas.set_color_map('copper'))
            display_cmap_menu.addAction('Cube Helix', lambda: self.canvas.set_color_map('cubehelix'))
            display_cmap_menu.addAction('Dark', lambda: self.canvas.set_color_map('Dark2'))
            display_cmap_menu.addAction('DS9', lambda: self.canvas.set_color_map('ds9_a'))
            display_cmap_menu.addAction('DS9 Cool', lambda: self.canvas.set_color_map('ds9_cool'))
            display_cmap_menu.addAction('DS9 He', lambda: self.canvas.set_color_map('ds9_he'))
            display_cmap_menu.addAction('Flag', lambda: self.canvas.set_color_map('flag'))
            display_cmap_menu.addAction('Gist Earth', lambda: self.canvas.set_color_map('gist_earth'))
            display_cmap_menu.addAction('Gist Gray', lambda: self.canvas.set_color_map('gist_gray'))
            display_cmap_menu.addAction('Gist Heat', lambda: self.canvas.set_color_map('gist_heat'))
            display_cmap_menu.addAction('Gist Ncar', lambda: self.canvas.set_color_map('gist_ncar'))
            display_cmap_menu.addAction('Gist Rainbow', lambda: self.canvas.set_color_map('gist_rainbow'))
            display_cmap_menu.addAction('Gist Stern', lambda: self.canvas.set_color_map('gist_stern'))
            display_cmap_menu.addAction('Gist Yarg', lambda: self.canvas.set_color_map('gist_yarg'))
            display_cmap_menu.addAction('GnBu', lambda: self.canvas.set_color_map('GnBu'))
            display_cmap_menu.addAction('Gnuplot', lambda: self.canvas.set_color_map('gnuplot'))
            display_cmap_menu.addAction('Gray Clip', lambda: self.canvas.set_color_map('grayclip'))
            display_cmap_menu.addAction('Gray', lambda: self.canvas.set_color_map('gray'))
            display_cmap_menu.addAction('Green', lambda: self.canvas.set_color_map('green'))
            display_cmap_menu.addAction('Greens', lambda: self.canvas.set_color_map('Greens'))
            display_cmap_menu.addAction('Light', lambda: self.canvas.set_color_map('light'))
            display_cmap_menu.addAction('Magma', lambda: self.canvas.set_color_map('magma'))
            display_cmap_menu.addAction('Nipy Spectral', lambda: self.canvas.set_color_map('nipy_spectral'))
            display_cmap_menu.addAction('Ocean', lambda: self.canvas.set_color_map('ocean'))
            display_cmap_menu.addAction('Oranges', lambda: self.canvas.set_color_map('Oranges'))
            display_cmap_menu.addAction('Paired', lambda: self.canvas.set_color_map('Paired'))
            display_cmap_menu.addAction('Pastel', lambda: self.canvas.set_color_map('pastel'))
            display_cmap_menu.addAction('Random', lambda: self.canvas.set_color_map('random'))
            display_cmap_menu.addAction('Winter', lambda: self.canvas.set_color_map('winter'))

            display_imap_menu = QtWidgets.QMenu('Intensity')
            display_imap_menu.addAction('Reset', lambda: (
                self.canvas.set_intensity_map('ramp')
            ))
            display_imap_menu.addSeparator()
            display_imap_menu.addAction('Equa', lambda: self.canvas.set_intensity_map('equa'))
            display_imap_menu.addAction('Expo', lambda: self.canvas.set_intensity_map('expo'))
            display_imap_menu.addAction('Gamma', lambda: self.canvas.set_intensity_map('gamma'))
            display_imap_menu.addAction('Jigsaw', lambda: self.canvas.set_intensity_map('jigsaw'))
            display_imap_menu.addAction('Lasritt', lambda: self.canvas.set_intensity_map('lasritt'))
            display_imap_menu.addAction('Log', lambda: self.canvas.set_intensity_map('log'))
            display_imap_menu.addAction('Neg', lambda: self.canvas.set_intensity_map('neg'))
            display_imap_menu.addAction('NegLog', lambda: self.canvas.set_intensity_map('neglog'))
            display_imap_menu.addAction('Null', lambda: self.canvas.set_intensity_map('null'))
            display_imap_menu.addAction('Ramp', lambda: self.canvas.set_intensity_map('ramp'))
            display_imap_menu.addAction('Stairs', lambda: self.canvas.set_intensity_map('stairs'))
            display_imap_menu.addAction('UltraSmooth', lambda: self.canvas.set_intensity_map('ultrasmooth'))

            transform_menu.addMenu(transform_flip_menu)
            transform_menu.addMenu(transform_rotate_menu)

            display_menu.addMenu(display_scale_menu)
            display_menu.addMenu(display_cmap_menu)
            display_menu.addMenu(display_imap_menu)
            display_menu.addAction('Contrast', lambda: self.set_contrast())

            menu.addSeparator()

            menu.addMenu(display_menu)
            menu.addMenu(transform_menu)

            menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)


# noinspection PyUnresolvedReferences
class CropForm(QWidget, Ui_FormCrop):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(CropForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.canvas = CanvasView(render='widget')
        self.canvas.enable_autocuts('on')
        self.canvas.set_autocut_params('zscale')
        self.canvas.enable_autozoom('on')
        self.canvas.set_bg(0.2, 0.2, 0.2)
        self.canvas.ui_set_active(True)

        group_box_layout = QVBoxLayout()
        self.ginga_widget = self.canvas.get_widget()
        group_box_layout.addWidget(self.ginga_widget)
        self.groupBox.setLayout(group_box_layout)
        self.img = AstroImage(logger=self.parent.logger)
        self.img.load_data(self.fits_array[0].data())
        self.canvas.set_image(self.img)

        self.current_angle = 0
        self.iteration = 0
        self.start = None

        self.ginga_widget.installEventFilter(self)

        self.pushButtonGO.clicked.connect(self.go)

    def go(self):
        warn = 0

        x_amounts = self.spinBoxXAmount.value()
        y_amounts = self.spinBoxYAmount.value()
        w_amounts = self.spinBoxWAmount.value()
        h_amounts = self.spinBoxHAmount.value()

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return
        progress = QtWidgets.QProgressDialog("Cropping ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Cropped"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(save_directory) / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.crop(x_amounts, y_amounts, w_amounts, h_amounts,
                                     output=file_name.absolute().__str__())

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = new_fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def reset_transform(self):
        x, y, swap = self.canvas.get_transforms()
        if x:
            self.canvas.flip_x()
        if y:
            self.canvas.flip_y()
        if swap:
            self.canvas.swap_xy()

    def set_contrast(self):
        number, ok = self.parent.gui_functions.get_number("Contrast", "Please provide contrast")
        if ok:
            self.canvas.set_contrast(number / 100)

    def reset(self):
        self.reset_transform()
        self.canvas.rotate(0)
        self.canvas.zoom_fit()
        self.canvas.set_color_algorithm('linear')
        self.canvas.restore_cmap()
        self.canvas.set_color_map('gray')
        self.canvas.restore_contrast()
        self.canvas.set_intensity_map('ramp')

    def draw_rect(self, p1, p2, color='red', linestyle="solid"):
        del self.canvas.canvas.objects[1:]
        try:
            w, h = self.canvas.get_data_size()
            if p1[0] < 0:
                p1[0] = 0

            if p1[0] > w:
                p1[0] = w

            if p1[1] < 0:
                p1[1] = 0

            if p1[1] > h:
                p1[1] = h

            if p2[0] < 0:
                p2[0] = 0

            if p2[0] > w:
                p2[0] = w

            if p2[1] < 0:
                p2[1] = 0

            if p2[1] > h:
                p2[1] = h

            rect = Rectangle(*p1, *p2, color, 2, linestyle=linestyle)
            self.canvas.canvas.add(rect)
        except Exception as e:
            self.parent.logger.warning(e)
            return

    def eventFilter(self, source, event):

        if event.type() == QtCore.QEvent.MouseMove:
            if self.start is not None:
                end = self.canvas.get_data_xy(event.x(), event.y())
                self.draw_rect(self.start, end, 'red', "dash")

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.canvas.set_pan(the_x, the_y)
                return True

            if event.button() == Qt.LeftButton:
                self.start = self.canvas.get_data_xy(event.x(), event.y())
                return True

        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                end = self.canvas.get_data_xy(event.x(), event.y())
                self.draw_rect(self.start, end)
                rect: Rectangle = self.canvas.canvas.objects[1:][0]

                self.spinBoxXAmount.setValue(int(min(rect.x1, rect.x2)))
                self.spinBoxYAmount.setValue(int(min(rect.y1, rect.y2)))
                self.spinBoxWAmount.setValue(int(abs(rect.x2 - rect.x1)))
                self.spinBoxHAmount.setValue(int(abs(rect.y2 - rect.y1)))
                self.start = None
                return True

        if event.type() == QtCore.QEvent.Wheel:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.current_angle += 1
                else:
                    self.current_angle -= 1

                self.current_angle %= 360
                self.canvas.rotate(self.current_angle)

                return True
            self.canvas.zoom_in(event.angleDelta().y() // 120)
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.ginga_widget:
            menu = QtWidgets.QMenu()

            transform_menu = QtWidgets.QMenu('Transform')
            transform_menu.addAction('Reset', lambda: (
                self.reset_transform(),
                self.canvas.rotate(0),
                self.canvas.zoom_fit()
            ))
            transform_menu.addSeparator()
            transform_flip_menu = QtWidgets.QMenu('Flip')
            transform_flip_menu.addAction('Reset', lambda: self.reset_transform())
            transform_flip_menu.addSeparator()
            transform_flip_menu.addAction('X', lambda: self.canvas.flip_x())
            transform_flip_menu.addAction('Y', lambda: self.canvas.flip_y())
            transform_flip_menu.addAction('Swap XY', lambda: self.canvas.swap_xy())

            transform_rotate_menu = QtWidgets.QMenu('Rotate')
            transform_rotate_menu.addAction('Reset', lambda: self.canvas.rotate(0))
            transform_rotate_menu.addSeparator()
            transform_rotate_menu.addAction('90', lambda: self.canvas.rotate(90))
            transform_rotate_menu.addAction('180', lambda: self.canvas.rotate(180))
            transform_rotate_menu.addAction('270', lambda: self.canvas.rotate(270))
            transform_rotate_menu.addAction('Custom', lambda: self.rotate())

            display_menu = QtWidgets.QMenu('Display')
            display_menu.addAction('Reset', lambda: (
                self.canvas.set_color_algorithm('linear'),
                self.canvas.restore_cmap(),
                self.canvas.set_color_map('gray'),
                self.canvas.restore_contrast(),
                self.canvas.set_intensity_map('ramp')
            ))
            display_menu.addSeparator()
            display_scale_menu = QtWidgets.QMenu('Scale')
            display_scale_menu.addAction('Reset', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addSeparator()
            display_scale_menu.addAction('Linear', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addAction('Log', lambda: self.canvas.set_color_algorithm('log'))
            display_scale_menu.addAction('Power', lambda: self.canvas.set_color_algorithm('power'))
            display_scale_menu.addAction('Square Root', lambda: self.canvas.set_color_algorithm('sqrt'))
            display_scale_menu.addAction('Squared', lambda: self.canvas.set_color_algorithm('squared'))
            display_scale_menu.addAction('Inverse Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('asinh'))
            display_scale_menu.addAction('Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('sinh'))
            display_scale_menu.addAction('Histogram Equalization', lambda: self.canvas.set_color_algorithm('histeq'))

            display_cmap_menu = QtWidgets.QMenu('Map')
            display_cmap_menu.addAction('Reset', lambda: (
                self.canvas.restore_cmap(), self.canvas.set_color_map('gray')
            ))
            display_cmap_menu.addAction('Reverse', lambda: self.canvas.invert_cmap())
            display_cmap_menu.addSeparator()
            display_cmap_menu.addAction('Accent', lambda: self.canvas.set_color_map('Accent'))
            display_cmap_menu.addAction('Autumn', lambda: self.canvas.set_color_map('autumn'))
            display_cmap_menu.addAction('Blue', lambda: self.canvas.set_color_map('blue'))
            display_cmap_menu.addAction('Blues', lambda: self.canvas.set_color_map('Blues'))
            display_cmap_menu.addAction('Bone', lambda: self.canvas.set_color_map('bone'))
            display_cmap_menu.addAction('Color', lambda: self.canvas.set_color_map('color'))
            display_cmap_menu.addAction('Cool', lambda: self.canvas.set_color_map('cool'))
            display_cmap_menu.addAction('Cool Warm', lambda: self.canvas.set_color_map('coolwarm'))
            display_cmap_menu.addAction('Copper', lambda: self.canvas.set_color_map('copper'))
            display_cmap_menu.addAction('Cube Helix', lambda: self.canvas.set_color_map('cubehelix'))
            display_cmap_menu.addAction('Dark', lambda: self.canvas.set_color_map('Dark2'))
            display_cmap_menu.addAction('DS9', lambda: self.canvas.set_color_map('ds9_a'))
            display_cmap_menu.addAction('DS9 Cool', lambda: self.canvas.set_color_map('ds9_cool'))
            display_cmap_menu.addAction('DS9 He', lambda: self.canvas.set_color_map('ds9_he'))
            display_cmap_menu.addAction('Flag', lambda: self.canvas.set_color_map('flag'))
            display_cmap_menu.addAction('Gist Earth', lambda: self.canvas.set_color_map('gist_earth'))
            display_cmap_menu.addAction('Gist Gray', lambda: self.canvas.set_color_map('gist_gray'))
            display_cmap_menu.addAction('Gist Heat', lambda: self.canvas.set_color_map('gist_heat'))
            display_cmap_menu.addAction('Gist Ncar', lambda: self.canvas.set_color_map('gist_ncar'))
            display_cmap_menu.addAction('Gist Rainbow', lambda: self.canvas.set_color_map('gist_rainbow'))
            display_cmap_menu.addAction('Gist Stern', lambda: self.canvas.set_color_map('gist_stern'))
            display_cmap_menu.addAction('Gist Yarg', lambda: self.canvas.set_color_map('gist_yarg'))
            display_cmap_menu.addAction('GnBu', lambda: self.canvas.set_color_map('GnBu'))
            display_cmap_menu.addAction('Gnuplot', lambda: self.canvas.set_color_map('gnuplot'))
            display_cmap_menu.addAction('Gray Clip', lambda: self.canvas.set_color_map('grayclip'))
            display_cmap_menu.addAction('Gray', lambda: self.canvas.set_color_map('gray'))
            display_cmap_menu.addAction('Green', lambda: self.canvas.set_color_map('green'))
            display_cmap_menu.addAction('Greens', lambda: self.canvas.set_color_map('Greens'))
            display_cmap_menu.addAction('Light', lambda: self.canvas.set_color_map('light'))
            display_cmap_menu.addAction('Magma', lambda: self.canvas.set_color_map('magma'))
            display_cmap_menu.addAction('Nipy Spectral', lambda: self.canvas.set_color_map('nipy_spectral'))
            display_cmap_menu.addAction('Ocean', lambda: self.canvas.set_color_map('ocean'))
            display_cmap_menu.addAction('Oranges', lambda: self.canvas.set_color_map('Oranges'))
            display_cmap_menu.addAction('Paired', lambda: self.canvas.set_color_map('Paired'))
            display_cmap_menu.addAction('Pastel', lambda: self.canvas.set_color_map('pastel'))
            display_cmap_menu.addAction('Random', lambda: self.canvas.set_color_map('random'))
            display_cmap_menu.addAction('Winter', lambda: self.canvas.set_color_map('winter'))

            display_imap_menu = QtWidgets.QMenu('Intensity')
            display_imap_menu.addAction('Reset', lambda: (
                self.canvas.set_intensity_map('ramp')
            ))
            display_imap_menu.addSeparator()
            display_imap_menu.addAction('Equa', lambda: self.canvas.set_intensity_map('equa'))
            display_imap_menu.addAction('Expo', lambda: self.canvas.set_intensity_map('expo'))
            display_imap_menu.addAction('Gamma', lambda: self.canvas.set_intensity_map('gamma'))
            display_imap_menu.addAction('Jigsaw', lambda: self.canvas.set_intensity_map('jigsaw'))
            display_imap_menu.addAction('Lasritt', lambda: self.canvas.set_intensity_map('lasritt'))
            display_imap_menu.addAction('Log', lambda: self.canvas.set_intensity_map('log'))
            display_imap_menu.addAction('Neg', lambda: self.canvas.set_intensity_map('neg'))
            display_imap_menu.addAction('NegLog', lambda: self.canvas.set_intensity_map('neglog'))
            display_imap_menu.addAction('Null', lambda: self.canvas.set_intensity_map('null'))
            display_imap_menu.addAction('Ramp', lambda: self.canvas.set_intensity_map('ramp'))
            display_imap_menu.addAction('Stairs', lambda: self.canvas.set_intensity_map('stairs'))
            display_imap_menu.addAction('UltraSmooth', lambda: self.canvas.set_intensity_map('ultrasmooth'))

            transform_menu.addMenu(transform_flip_menu)
            transform_menu.addMenu(transform_rotate_menu)

            display_menu.addMenu(display_scale_menu)
            display_menu.addMenu(display_cmap_menu)
            display_menu.addMenu(display_imap_menu)
            display_menu.addAction('Contrast', lambda: self.set_contrast())

            menu.addSeparator()

            menu.addMenu(display_menu)
            menu.addMenu(transform_menu)

            menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)


# noinspection PyUnresolvedReferences
class BinForm(QWidget, Ui_FormBin):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(BinForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.are_the_same = True
        self.spinBoxXAmount.valueChanged.connect(self.fallow)
        self.spinBoxYAmount.valueChanged.connect(self.toggle)

        self.pushButtonGo.clicked.connect(self.go)

    def go(self):
        warn = 0

        x_amounts = self.spinBoxXAmount.value()
        y_amounts = self.spinBoxYAmount.value()

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Binning ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Binned"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = Path(save_directory) / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.bin([x_amounts, y_amounts], output=file_name.absolute().__str__(), override=True)

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def fallow(self):
        if self.are_the_same:
            self.spinBoxYAmount.setValue(self.spinBoxXAmount.value())

    def toggle(self):
        self.are_the_same = self.spinBoxYAmount.value() == self.spinBoxXAmount.value()


# noinspection PyUnresolvedReferences
class AlignForm(QWidget, Ui_FormAlign):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(AlignForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.set_reference()

        self.pushButtonShow.clicked.connect(self.show_reference)
        self.pushButtonGO.clicked.connect(self.go)

        self.load_settings()

        self.spinBoxMaxControlPoint.valueChanged.connect(self.save_settings)
        self.doubleSpinDetectionSigma.valueChanged.connect(self.save_settings)
        self.spinBoxMinArea.valueChanged.connect(self.save_settings)

    def load_settings(self):
        settings = self.parent.settings.settings
        self.spinBoxMaxControlPoint.setValue(settings["operations"]["transform"]["align"]["maximum_control_point"])
        self.doubleSpinDetectionSigma.setValue(settings["operations"]["transform"]["align"]["detection_sigma"])
        self.spinBoxMinArea.setValue(settings["operations"]["transform"]["align"]["minimum_area"])

    def save_settings(self):
        settings = self.parent.settings.settings
        settings["operations"]["transform"]["align"]["maximum_control_point"] = self.spinBoxMaxControlPoint.value()
        settings["operations"]["transform"]["align"]["detection_sigma"] = self.doubleSpinDetectionSigma.value()
        settings["operations"]["transform"]["align"]["minimum_area"] = self.spinBoxMinArea.value()

        self.parent.settings.settings = settings

    def go(self):
        warn = 0

        reference = self.fits_array[self.comboBoxReference.currentIndex()]
        max_control_points = self.spinBoxMaxControlPoint.value()
        detection_sigma = self.doubleSpinDetectionSigma.value()
        min_area = self.spinBoxMinArea.value()

        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        progress = QtWidgets.QProgressDialog("Aligning ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Aligned"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = save_directory / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                new_fits = fits.align(
                    reference, max_control_points=max_control_points, min_area=min_area,
                    output=file_name.absolute().__str__(), override=True
                )

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                statistics = fits.imstat()
                for key, value in statistics.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def show_reference(self):
        selected_file = self.fits_array[self.comboBoxReference.currentIndex()]
        self.parent.show_window(DisplayForm(self.parent, FitsArray([selected_file])))

    def set_reference(self):
        files = [each.file.name for each in self.fits_array]
        self.comboBoxReference.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxReference, files)


# noinspection PyUnresolvedReferences
class CombineForm(QWidget, Ui_FormCombine):
    def __init__(self, parent: MainWindow, fits_array: FitsArray, combine_type: str):
        super(CombineForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.combine_type = combine_type
        self.comboBoxWeight.currentIndexChanged.connect(self.set_weights)

        self.set_from_header()
        self.set_weights()

        self.load_settings()

        self.comboBoxMethod.currentIndexChanged.connect(self.save_settings)
        self.comboBoxClipping.currentIndexChanged.connect(self.save_settings)
        self.comboBoxWeight.currentIndexChanged.connect(self.save_settings)

    def load_settings(self):
        settings = self.parent.settings.settings

        self.comboBoxMethod.setCurrentIndex(settings["operations"]["combine"][self.combine_type]["method"])
        self.comboBoxClipping.setCurrentIndex(settings["operations"]["combine"][self.combine_type]["clipping"])

        try:
            self.comboBoxWeight.setCurrentText(settings["operations"]["combine"][self.combine_type]["weight"])
        except Exception as _:
            self.parent.logger.warning("Cannot set weight. Setting to default.")
            self.comboBoxWeight.setCurrentText("None")

    def save_settings(self):
        settings = self.parent.settings.settings
        settings["operations"]["combine"][self.combine_type]["method"] = self.comboBoxMethod.currentIndex()
        settings["operations"]["combine"][self.combine_type]["clipping"] = self.comboBoxClipping.currentIndex()
        settings["operations"]["combine"][self.combine_type]["weight"] = self.comboBoxWeight.currentText()

        self.parent.settings.settings = settings

    def set_from_header(self):
        header = self.fits_array[0].header()
        self.parent.gui_functions.add_to_combo(self.comboBoxWeight, list(header.columns))

        self.pushButtonGo.clicked.connect(self.go)

    def set_weights(self):
        weight = self.comboBoxWeight.currentText()
        weights = []
        if weight == "None":
            for f in self.fits_array:
                weights.append([f.file.name, 1.0])

        elif weight == "Custom":
            for f in self.fits_array:
                weights.append([f.file.name, ""])
        else:
            headers = self.fits_array.header()
            for index, row in headers.iterrows():
                each_weight = row[weight]
                if isinstance(each_weight, (float, int)):
                    weights.append([index, float(each_weight)])
                else:
                    weights.append([index, 1.0])

        self.parent.gui_functions.clear_table(self.tableWidgetWeights)
        self.parent.gui_functions.add_to_table(self.tableWidgetWeights, weights)

    def go(self):
        file = self.parent.gui_functions.save_file("Combine File Name", "fits, fit, fts (*.fits *.fit *.fts)")

        if not file:
            return

        method = self.comboBoxMethod.currentText()
        clipping = self.comboBoxClipping.currentText()
        clipping_to_use = None if clipping == "None" else clipping.lower()
        table_content = self.parent.gui_functions.get_from_table(self.tableWidgetWeights)
        try:
            weights = [float(each[1]) for each in table_content]
        except Exception as e:
            self.parent.logger.warning(e)
            self.parent.gui_functions.error("Cannot convert at least one of weights to numeric")
            return

        combined = self.fits_array.combine(
            method=method.lower(), clipping=clipping_to_use, weights=weights, output=file, override=True
        )
        group = Path(file).stem
        self.parent.gui_functions.add_to_files(
            [combined.file.absolute().__str__()], self.parent.treeWidget, grp=group
        )


# noinspection PyUnresolvedReferences
class DisplayForm(QWidget, Ui_FormDisplay):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(DisplayForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.canvas = CanvasView(render='widget')
        self.canvas.enable_autocuts('on')
        self.canvas.set_autocut_params('zscale')
        self.canvas.enable_autozoom('on')
        self.canvas.set_bg(0.2, 0.2, 0.2)
        self.canvas.ui_set_active(True)

        group_box_layout = QVBoxLayout()
        self.ginga_widget = self.canvas.get_widget()
        group_box_layout.addWidget(self.ginga_widget)
        self.groupBox.setLayout(group_box_layout)
        self.img = AstroImage(logger=self.parent.logger)
        self.img.load_data(self.fits_array[0].data())
        self.canvas.set_image(self.img)

        self.labelFile.setText(self.fits_array[0].file.name)
        self.labelObject.setText(list(self.fits_array[0].header().to_dict().get("OBJECT", {1: ''}).values())[0])

        self.ginga_widget.installEventFilter(self)

        self.iteration = 0
        self.current_angle = 0

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        if len(self.fits_array) > 1:
            settings = self.parent.settings.settings
            interval = settings["display"]["interval"]
            self.timer.start(interval)

    def info_update(self, x, y):
        fits = self.fits_array[self.iteration]
        if self.canvas.check_cursor_location():
            the_x, the_y = self.canvas.get_data_xy(x, y)
            w, h = self.canvas.get_data_size()
            if not 0 < the_x < w or not 0 < the_y < h:
                x_to_show, y_to_show = "---", "---"
                ra, dec = "---", "---"
            else:
                x_to_show, y_to_show = int(the_x), int(the_y)
                try:
                    sky = fits.pixels_to_skys(x_to_show, y_to_show)
                    ra = sky[sky].values[0].ra
                    dec = sky[sky].values[0].dec

                except (ValueError, Unsolvable):
                    ra, dec = "---", "---"

            if x_to_show != "---":
                value = self.canvas.get_data(x_to_show, y_to_show)
            else:
                value = "---"

            self.labelX.setText(x_to_show.__str__())
            self.labelY.setText(y_to_show.__str__())
            self.labelRa.setText(ra.__str__())
            self.labelDec.setText(dec.__str__())
            self.labelValue.setText(value.__str__())

    def animate(self):
        fits = self.fits_array[self.iteration]
        self.labelFile.setText(fits.file.name)
        self.labelObject.setText(list(self.fits_array[0].header().to_dict().get("OBJECT", {1: ""}).values())[0])
        self.img.load_data(fits.data())
        self.iteration += 1
        if self.iteration >= len(self.fits_array):
            self.iteration = 0

    def rotate(self):
        warn = 0
        angle, ok = self.parent.gui_functions.get_number("Angle", "Please provide angle to rotate", 0, 360)
        if ok:
            try:
                self.current_angle = float(angle)
                self.canvas.rotate(self.current_angle)
            except Exception as e:
                warn += 1
                self.logger.warning(e)

        if warn > 0:
            self.parent.gui_functions.toast(f"Something went wrong with rotating.\nSee log files.")

    def reset_transform(self):
        x, y, swap = self.canvas.get_transforms()
        if x:
            self.canvas.flip_x()
        if y:
            self.canvas.flip_y()
        if swap:
            self.canvas.swap_xy()

    def set_contrast(self):
        number, ok = self.parent.gui_functions.get_number("Contrast", "Please provide contrast")
        if ok:
            self.canvas.set_contrast(number / 100)

    def reset(self):
        self.reset_transform()
        self.canvas.rotate(0)
        self.canvas.zoom_fit()
        self.canvas.set_color_algorithm('linear')
        self.canvas.restore_cmap()
        self.canvas.set_color_map('gray')
        self.canvas.restore_contrast()
        self.canvas.set_intensity_map('ramp')

    def copy_xy(self, x, y):
        the_x, the_y = self.canvas.get_data_xy(x, y)
        pd.DataFrame([f'{the_x} {the_y}']).to_clipboard(index=False, header=False)

    def copy_wcs(self, fits: Fits, x, y):
        try:
            the_x, the_y = self.canvas.get_data_xy(x, y)
            sky = fits.pixels_to_skys(the_x, the_y)
            pd.DataFrame([f'{sky[sky].values[0].ra} {sky[sky].values[0].dec}']).to_clipboard(index=False, header=False)
        except (ValueError, Unsolvable):
            pd.DataFrame([f'']).to_clipboard(index=False, header=False)

    def copy_value(self, x, y):
        try:
            the_x, the_y = self.canvas.get_data_xy(x, y)
            value = self.canvas.get_data(the_x, the_y)
            pd.DataFrame([f'{value}']).to_clipboard(index=False, header=False)
        except (ValueError, Unsolvable):
            pd.DataFrame([f'']).to_clipboard(index=False, header=False)

    def eventFilter(self, source, event):
        fits = self.fits_array[self.iteration]
        if event.type() == QtCore.QEvent.MouseMove:
            self.info_update(event.x(), event.y())
            return True

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.canvas.set_pan(the_x, the_y)
            return True

        if event.type() == QtCore.QEvent.Wheel:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.current_angle += 1
                else:
                    self.current_angle -= 1

                self.current_angle %= 360
                self.canvas.rotate(self.current_angle)

                return True
            self.canvas.zoom_in(event.angleDelta().y() // 120)
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.ginga_widget:
            menu = QtWidgets.QMenu()
            # menu.addAction('Transform')

            copy_menu = QtWidgets.QMenu('Copy')
            copy_menu.addAction('WCS', lambda: self.copy_wcs(fits, event.x(), event.y()))
            copy_menu.addAction('Physical', lambda: self.copy_xy(event.x(), event.y()))
            copy_menu.addAction('Value', lambda: self.copy_value(event.x(), event.y()))

            transform_menu = QtWidgets.QMenu('Transform')
            transform_menu.addAction('Reset', lambda: (
                self.reset_transform(),
                self.canvas.rotate(0),
                self.canvas.zoom_fit()
            ))
            transform_menu.addSeparator()
            transform_flip_menu = QtWidgets.QMenu('Flip')
            transform_flip_menu.addAction('Reset', lambda: self.reset_transform())
            transform_flip_menu.addSeparator()
            transform_flip_menu.addAction('X', lambda: self.canvas.flip_x())
            transform_flip_menu.addAction('Y', lambda: self.canvas.flip_y())
            transform_flip_menu.addAction('Swap XY', lambda: self.canvas.swap_xy())

            transform_rotate_menu = QtWidgets.QMenu('Rotate')
            transform_rotate_menu.addAction('Reset', lambda: self.canvas.rotate(0))
            transform_rotate_menu.addSeparator()
            transform_rotate_menu.addAction('90', lambda: self.canvas.rotate(90))
            transform_rotate_menu.addAction('180', lambda: self.canvas.rotate(180))
            transform_rotate_menu.addAction('270', lambda: self.canvas.rotate(270))
            transform_rotate_menu.addAction('Custom', lambda: self.rotate())

            display_menu = QtWidgets.QMenu('Display')
            display_menu.addAction('Reset', lambda: (
                self.canvas.set_color_algorithm('linear'),
                self.canvas.restore_cmap(),
                self.canvas.set_color_map('gray'),
                self.canvas.restore_contrast(),
                self.canvas.set_intensity_map('ramp')
            ))
            display_menu.addSeparator()
            display_scale_menu = QtWidgets.QMenu('Scale')
            display_scale_menu.addAction('Reset', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addSeparator()
            display_scale_menu.addAction('Linear', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addAction('Log', lambda: self.canvas.set_color_algorithm('log'))
            display_scale_menu.addAction('Power', lambda: self.canvas.set_color_algorithm('power'))
            display_scale_menu.addAction('Square Root', lambda: self.canvas.set_color_algorithm('sqrt'))
            display_scale_menu.addAction('Squared', lambda: self.canvas.set_color_algorithm('squared'))
            display_scale_menu.addAction('Inverse Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('asinh'))
            display_scale_menu.addAction('Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('sinh'))
            display_scale_menu.addAction('Histogram Equalization', lambda: self.canvas.set_color_algorithm('histeq'))

            display_cmap_menu = QtWidgets.QMenu('Map')
            display_cmap_menu.addAction('Reset', lambda: (
                self.canvas.restore_cmap(), self.canvas.set_color_map('gray')
            ))
            display_cmap_menu.addAction('Reverse', lambda: self.canvas.invert_cmap())
            display_cmap_menu.addSeparator()
            display_cmap_menu.addAction('Accent', lambda: self.canvas.set_color_map('Accent'))
            display_cmap_menu.addAction('Autumn', lambda: self.canvas.set_color_map('autumn'))
            display_cmap_menu.addAction('Blue', lambda: self.canvas.set_color_map('blue'))
            display_cmap_menu.addAction('Blues', lambda: self.canvas.set_color_map('Blues'))
            display_cmap_menu.addAction('Bone', lambda: self.canvas.set_color_map('bone'))
            display_cmap_menu.addAction('Color', lambda: self.canvas.set_color_map('color'))
            display_cmap_menu.addAction('Cool', lambda: self.canvas.set_color_map('cool'))
            display_cmap_menu.addAction('Cool Warm', lambda: self.canvas.set_color_map('coolwarm'))
            display_cmap_menu.addAction('Copper', lambda: self.canvas.set_color_map('copper'))
            display_cmap_menu.addAction('Cube Helix', lambda: self.canvas.set_color_map('cubehelix'))
            display_cmap_menu.addAction('Dark', lambda: self.canvas.set_color_map('Dark2'))
            display_cmap_menu.addAction('DS9', lambda: self.canvas.set_color_map('ds9_a'))
            display_cmap_menu.addAction('DS9 Cool', lambda: self.canvas.set_color_map('ds9_cool'))
            display_cmap_menu.addAction('DS9 He', lambda: self.canvas.set_color_map('ds9_he'))
            display_cmap_menu.addAction('Flag', lambda: self.canvas.set_color_map('flag'))
            display_cmap_menu.addAction('Gist Earth', lambda: self.canvas.set_color_map('gist_earth'))
            display_cmap_menu.addAction('Gist Gray', lambda: self.canvas.set_color_map('gist_gray'))
            display_cmap_menu.addAction('Gist Heat', lambda: self.canvas.set_color_map('gist_heat'))
            display_cmap_menu.addAction('Gist Ncar', lambda: self.canvas.set_color_map('gist_ncar'))
            display_cmap_menu.addAction('Gist Rainbow', lambda: self.canvas.set_color_map('gist_rainbow'))
            display_cmap_menu.addAction('Gist Stern', lambda: self.canvas.set_color_map('gist_stern'))
            display_cmap_menu.addAction('Gist Yarg', lambda: self.canvas.set_color_map('gist_yarg'))
            display_cmap_menu.addAction('GnBu', lambda: self.canvas.set_color_map('GnBu'))
            display_cmap_menu.addAction('Gnuplot', lambda: self.canvas.set_color_map('gnuplot'))
            display_cmap_menu.addAction('Gray Clip', lambda: self.canvas.set_color_map('grayclip'))
            display_cmap_menu.addAction('Gray', lambda: self.canvas.set_color_map('gray'))
            display_cmap_menu.addAction('Green', lambda: self.canvas.set_color_map('green'))
            display_cmap_menu.addAction('Greens', lambda: self.canvas.set_color_map('Greens'))
            display_cmap_menu.addAction('Light', lambda: self.canvas.set_color_map('light'))
            display_cmap_menu.addAction('Magma', lambda: self.canvas.set_color_map('magma'))
            display_cmap_menu.addAction('Nipy Spectral', lambda: self.canvas.set_color_map('nipy_spectral'))
            display_cmap_menu.addAction('Ocean', lambda: self.canvas.set_color_map('ocean'))
            display_cmap_menu.addAction('Oranges', lambda: self.canvas.set_color_map('Oranges'))
            display_cmap_menu.addAction('Paired', lambda: self.canvas.set_color_map('Paired'))
            display_cmap_menu.addAction('Pastel', lambda: self.canvas.set_color_map('pastel'))
            display_cmap_menu.addAction('Random', lambda: self.canvas.set_color_map('random'))
            display_cmap_menu.addAction('Winter', lambda: self.canvas.set_color_map('winter'))

            display_imap_menu = QtWidgets.QMenu('Intensity')
            display_imap_menu.addAction('Reset', lambda: (
                self.canvas.set_intensity_map('ramp')
            ))
            display_imap_menu.addSeparator()
            display_imap_menu.addAction('Equa', lambda: self.canvas.set_intensity_map('equa'))
            display_imap_menu.addAction('Expo', lambda: self.canvas.set_intensity_map('expo'))
            display_imap_menu.addAction('Gamma', lambda: self.canvas.set_intensity_map('gamma'))
            display_imap_menu.addAction('Jigsaw', lambda: self.canvas.set_intensity_map('jigsaw'))
            display_imap_menu.addAction('Lasritt', lambda: self.canvas.set_intensity_map('lasritt'))
            display_imap_menu.addAction('Log', lambda: self.canvas.set_intensity_map('log'))
            display_imap_menu.addAction('Neg', lambda: self.canvas.set_intensity_map('neg'))
            display_imap_menu.addAction('NegLog', lambda: self.canvas.set_intensity_map('neglog'))
            display_imap_menu.addAction('Null', lambda: self.canvas.set_intensity_map('null'))
            display_imap_menu.addAction('Ramp', lambda: self.canvas.set_intensity_map('ramp'))
            display_imap_menu.addAction('Stairs', lambda: self.canvas.set_intensity_map('stairs'))
            display_imap_menu.addAction('UltraSmooth', lambda: self.canvas.set_intensity_map('ultrasmooth'))

            transform_menu.addMenu(transform_flip_menu)
            transform_menu.addMenu(transform_rotate_menu)

            display_menu.addMenu(display_scale_menu)
            display_menu.addMenu(display_cmap_menu)
            display_menu.addMenu(display_imap_menu)
            display_menu.addAction('Contrast', lambda: self.set_contrast())

            menu.addMenu(copy_menu)
            menu.addSeparator()

            menu.addMenu(display_menu)
            menu.addMenu(transform_menu)

            menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)


# noinspection PyUnresolvedReferences
class WCSForm(QWidget, Ui_FormWCS):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(WCSForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.canvas = CanvasView(render='widget')
        self.canvas.enable_autocuts('on')
        self.canvas.set_autocut_params('zscale')
        self.canvas.enable_autozoom('on')
        self.canvas.set_bg(0.2, 0.2, 0.2)
        self.canvas.ui_set_active(True)

        group_box_layout = QVBoxLayout()
        self.ginga_widget = self.canvas.get_widget()
        group_box_layout.addWidget(self.ginga_widget)
        self.groupBox.setLayout(group_box_layout)
        self.img = AstroImage(logger=self.parent.logger)
        self.img.load_data(self.fits_array[0].data())
        self.canvas.set_image(self.img)

        self.labelObject.setText(list(self.fits_array[0].header().to_dict().get("OBJECT", {1: ''}).values())[0])

        self.load_files()

        self.comboBoxFile.currentIndexChanged.connect(self.goto)
        self.pushButtonGO.clicked.connect(self.go)

        self.ginga_widget.installEventFilter(self)

        self.iteration = self.comboBoxFile.currentIndex()
        self.current_angle = 0

    def go(self):
        warn = 0

        reference = self.fits_array[self.comboBoxFile.currentIndex()]
        api_key = self.parent.settings.settings["edit"]["wcs"]["astrometry_apikey"]
        save_directory = self.parent.gui_functions.get_directory("Save Directory")

        if not save_directory:
            return

        if not api_key:
            ak = self.parent.gui_functions.get_text(
                "API Key", "I need your astrometry.net API Key", defalut=""
            )
            if not ak:
                self.parent.gui_functions.error("No API Key available. See: https://nova.astrometry.net/api_help")
                self.parent.logger.warning("No API Key available.")
                return
            api_key = ak

        progress = QtWidgets.QProgressDialog("Solving ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        try:
            solved = reference.solve_field(api_key, False)
        except Exception as e:

            progress.close()
            self.parent.gui_functions.error("Couldn't solve the reference image")
            self.parent.logger.warning(e)
            return

        group_layer = CustomQTreeWidgetItem(self.parent.treeWidget, ["Solved"])

        for iteration, fits in enumerate(self.fits_array):
            try:
                progress.setLabelText(f"Operating on {fits.file.name}")

                file_name = save_directory / Path(fits.file.name)
                if progress.wasCanceled():
                    progress.setLabelText("ABORT!")
                    break

                ref_w = WCS(solved.pure_header())
                t, (source_list, target_list) = astroalign.find_transform(
                    source=fits.data(),
                    target=solved.data()
                )

                xs = target_list[:, 0].flatten()
                ys = target_list[:, 1].flatten()

                new_xs = source_list[:, 0].flatten()
                new_ys = source_list[:, 1].flatten()

                skys = ref_w.pixel_to_world(xs.tolist(), ys.tolist())
                w = fit_wcs_from_points([new_xs, new_ys], skys)

                temp_header = Header()
                # temp_header.extend(fits.pure_header(), unique=True, update=True)
                temp_header.extend(w.to_header(), unique=True)
                new_fits = Fits.from_data_header(fits.data(), header=temp_header, output=file_name)

                group_layer.setFirstColumnSpanned(True)
                file_name_layer = CustomQTreeWidgetItem(group_layer, [new_fits.file.name])
                file_name_layer.setFirstColumnSpanned(True)

                item = CustomQTreeWidgetItem(file_name_layer, ["Path", new_fits.file.resolve().parent.__str__()])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                stats = fits.imstat()
                for key, value in stats.iloc[0].items():
                    item = CustomQTreeWidgetItem(file_name_layer, [key.capitalize(), f"{value:.2f}"])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                progress.setValue(iteration)

            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

        progress.close()
        if group_layer.childCount() == 0:
            self.parent.treeWidget.takeTopLevelItem(self.parent.treeWidget.indexOfTopLevelItem(group_layer))

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def load_files(self):
        files = [fits.file.name for fits in self.fits_array]
        self.comboBoxFile.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxFile, files)

    def info_update(self, x, y):
        fits = self.fits_array[self.iteration]
        if self.canvas.check_cursor_location():
            the_x, the_y = self.canvas.get_data_xy(x, y)
            w, h = self.canvas.get_data_size()
            if not 0 < the_x < w or not 0 < the_y < h:
                x_to_show, y_to_show = "---", "---"
                ra, dec = "---", "---"
            else:
                x_to_show, y_to_show = int(the_x), int(the_y)
                try:
                    sky = fits.pixels_to_skys(x_to_show, y_to_show)
                    ra = sky[sky].values[0].ra
                    dec = sky[sky].values[0].dec

                except (ValueError, Unsolvable):
                    ra, dec = "---", "---"

            if x_to_show != "---":
                value = self.canvas.get_data(x_to_show, y_to_show)
            else:
                value = "---"

            self.labelX.setText(x_to_show.__str__())
            self.labelY.setText(y_to_show.__str__())
            self.labelRa.setText(ra.__str__())
            self.labelDec.setText(dec.__str__())
            self.labelValue.setText(value.__str__())

    def goto(self):
        self.iteration = self.comboBoxFile.currentIndex()
        fits = self.fits_array[self.iteration]
        self.comboBoxFile.currentText()
        self.labelObject.setText(list(self.fits_array[0].header().to_dict().get("OBJECT", {1: ""}).values())[0])
        self.img.load_data(fits.data())

    def rotate(self):
        warn = 0
        angle, ok = self.parent.gui_functions.get_number("Angle", "Please provide angle to rotate", 0, 360)
        if ok:
            try:
                self.current_angle = float(angle)
                self.canvas.rotate(self.current_angle)
            except Exception as e:
                warn = 0
                self.logger.warning(e)

        if warn > 0:
            self.parent.gui_functions.toast(f"Something went wrong with rotating.\nSee log files.")

    def reset_transform(self):
        x, y, swap = self.canvas.get_transforms()
        if x:
            self.canvas.flip_x()
        if y:
            self.canvas.flip_y()
        if swap:
            self.canvas.swap_xy()

    def set_contrast(self):
        number, ok = self.parent.gui_functions.get_number("Contrast", "Please provide contrast")
        if ok:
            self.canvas.set_contrast(number / 100)

    def reset(self):
        self.reset_transform()
        self.canvas.rotate(0)
        self.canvas.zoom_fit()
        self.canvas.set_color_algorithm('linear')
        self.canvas.restore_cmap()
        self.canvas.set_color_map('gray')
        self.canvas.restore_contrast()
        self.canvas.set_intensity_map('ramp')

    def copy_xy(self, x, y):
        the_x, the_y = self.canvas.get_data_xy(x, y)
        pd.DataFrame([f'{the_x} {the_y}']).to_clipboard(index=False, header=False)

    def copy_wcs(self, fits: Fits, x, y):
        try:
            the_x, the_y = self.canvas.get_data_xy(x, y)
            sky = fits.pixels_to_skys(the_x, the_y)
            pd.DataFrame([f'{sky[sky].values[0].ra} {sky[sky].values[0].dec}']).to_clipboard(index=False, header=False)
        except (ValueError, Unsolvable):
            pd.DataFrame([f'']).to_clipboard(index=False, header=False)

    def copy_value(self, x, y):
        try:
            the_x, the_y = self.canvas.get_data_xy(x, y)
            value = self.canvas.get_data(the_x, the_y)
            pd.DataFrame([f'{value}']).to_clipboard(index=False, header=False)
        except (ValueError, Unsolvable):
            pd.DataFrame([f'']).to_clipboard(index=False, header=False)

    def eventFilter(self, source, event):
        fits = self.fits_array[self.iteration]
        if event.type() == QtCore.QEvent.MouseMove:
            self.info_update(event.x(), event.y())
            return True

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                the_x, the_y = self.canvas.get_data_xy(event.x(), event.y())
                self.canvas.set_pan(the_x, the_y)
            return True

        if event.type() == QtCore.QEvent.Wheel:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.angleDelta().y() > 0:
                    self.current_angle += 1
                else:
                    self.current_angle -= 1

                self.current_angle %= 360
                self.canvas.rotate(self.current_angle)

                return True
            self.canvas.zoom_in(event.angleDelta().y() // 120)
            return True

        if event.type() == QtCore.QEvent.ContextMenu and source is self.ginga_widget:
            menu = QtWidgets.QMenu()
            # menu.addAction('Transform')

            copy_menu = QtWidgets.QMenu('Copy')
            copy_menu.addAction('WCS', lambda: self.copy_wcs(fits, event.x(), event.y()))
            copy_menu.addAction('Physical', lambda: self.copy_xy(event.x(), event.y()))
            copy_menu.addAction('Value', lambda: self.copy_value(event.x(), event.y()))

            transform_menu = QtWidgets.QMenu('Transform')
            transform_menu.addAction('Reset', lambda: (
                self.reset_transform(),
                self.canvas.rotate(0),
                self.canvas.zoom_fit()
            ))
            transform_menu.addSeparator()
            transform_flip_menu = QtWidgets.QMenu('Flip')
            transform_flip_menu.addAction('Reset', lambda: self.reset_transform())
            transform_flip_menu.addSeparator()
            transform_flip_menu.addAction('X', lambda: self.canvas.flip_x())
            transform_flip_menu.addAction('Y', lambda: self.canvas.flip_y())
            transform_flip_menu.addAction('Swap XY', lambda: self.canvas.swap_xy())

            transform_rotate_menu = QtWidgets.QMenu('Rotate')
            transform_rotate_menu.addAction('Reset', lambda: self.canvas.rotate(0))
            transform_rotate_menu.addSeparator()
            transform_rotate_menu.addAction('90', lambda: self.canvas.rotate(90))
            transform_rotate_menu.addAction('180', lambda: self.canvas.rotate(180))
            transform_rotate_menu.addAction('270', lambda: self.canvas.rotate(270))
            transform_rotate_menu.addAction('Custom', lambda: self.rotate())

            display_menu = QtWidgets.QMenu('Display')
            display_menu.addAction('Reset', lambda: (
                self.canvas.set_color_algorithm('linear'),
                self.canvas.restore_cmap(),
                self.canvas.set_color_map('gray'),
                self.canvas.restore_contrast(),
                self.canvas.set_intensity_map('ramp')
            ))
            display_menu.addSeparator()
            display_scale_menu = QtWidgets.QMenu('Scale')
            display_scale_menu.addAction('Reset', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addSeparator()
            display_scale_menu.addAction('Linear', lambda: self.canvas.set_color_algorithm('linear'))
            display_scale_menu.addAction('Log', lambda: self.canvas.set_color_algorithm('log'))
            display_scale_menu.addAction('Power', lambda: self.canvas.set_color_algorithm('power'))
            display_scale_menu.addAction('Square Root', lambda: self.canvas.set_color_algorithm('sqrt'))
            display_scale_menu.addAction('Squared', lambda: self.canvas.set_color_algorithm('squared'))
            display_scale_menu.addAction('Inverse Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('asinh'))
            display_scale_menu.addAction('Hyperbolic Sine', lambda: self.canvas.set_color_algorithm('sinh'))
            display_scale_menu.addAction('Histogram Equalization', lambda: self.canvas.set_color_algorithm('histeq'))

            display_cmap_menu = QtWidgets.QMenu('Map')
            display_cmap_menu.addAction('Reset', lambda: (
                self.canvas.restore_cmap(), self.canvas.set_color_map('gray')
            ))
            display_cmap_menu.addAction('Reverse', lambda: self.canvas.invert_cmap())
            display_cmap_menu.addSeparator()
            display_cmap_menu.addAction('Accent', lambda: self.canvas.set_color_map('Accent'))
            display_cmap_menu.addAction('Autumn', lambda: self.canvas.set_color_map('autumn'))
            display_cmap_menu.addAction('Blue', lambda: self.canvas.set_color_map('blue'))
            display_cmap_menu.addAction('Blues', lambda: self.canvas.set_color_map('Blues'))
            display_cmap_menu.addAction('Bone', lambda: self.canvas.set_color_map('bone'))
            display_cmap_menu.addAction('Color', lambda: self.canvas.set_color_map('color'))
            display_cmap_menu.addAction('Cool', lambda: self.canvas.set_color_map('cool'))
            display_cmap_menu.addAction('Cool Warm', lambda: self.canvas.set_color_map('coolwarm'))
            display_cmap_menu.addAction('Copper', lambda: self.canvas.set_color_map('copper'))
            display_cmap_menu.addAction('Cube Helix', lambda: self.canvas.set_color_map('cubehelix'))
            display_cmap_menu.addAction('Dark', lambda: self.canvas.set_color_map('Dark2'))
            display_cmap_menu.addAction('DS9', lambda: self.canvas.set_color_map('ds9_a'))
            display_cmap_menu.addAction('DS9 Cool', lambda: self.canvas.set_color_map('ds9_cool'))
            display_cmap_menu.addAction('DS9 He', lambda: self.canvas.set_color_map('ds9_he'))
            display_cmap_menu.addAction('Flag', lambda: self.canvas.set_color_map('flag'))
            display_cmap_menu.addAction('Gist Earth', lambda: self.canvas.set_color_map('gist_earth'))
            display_cmap_menu.addAction('Gist Gray', lambda: self.canvas.set_color_map('gist_gray'))
            display_cmap_menu.addAction('Gist Heat', lambda: self.canvas.set_color_map('gist_heat'))
            display_cmap_menu.addAction('Gist Ncar', lambda: self.canvas.set_color_map('gist_ncar'))
            display_cmap_menu.addAction('Gist Rainbow', lambda: self.canvas.set_color_map('gist_rainbow'))
            display_cmap_menu.addAction('Gist Stern', lambda: self.canvas.set_color_map('gist_stern'))
            display_cmap_menu.addAction('Gist Yarg', lambda: self.canvas.set_color_map('gist_yarg'))
            display_cmap_menu.addAction('GnBu', lambda: self.canvas.set_color_map('GnBu'))
            display_cmap_menu.addAction('Gnuplot', lambda: self.canvas.set_color_map('gnuplot'))
            display_cmap_menu.addAction('Gray Clip', lambda: self.canvas.set_color_map('grayclip'))
            display_cmap_menu.addAction('Gray', lambda: self.canvas.set_color_map('gray'))
            display_cmap_menu.addAction('Green', lambda: self.canvas.set_color_map('green'))
            display_cmap_menu.addAction('Greens', lambda: self.canvas.set_color_map('Greens'))
            display_cmap_menu.addAction('Light', lambda: self.canvas.set_color_map('light'))
            display_cmap_menu.addAction('Magma', lambda: self.canvas.set_color_map('magma'))
            display_cmap_menu.addAction('Nipy Spectral', lambda: self.canvas.set_color_map('nipy_spectral'))
            display_cmap_menu.addAction('Ocean', lambda: self.canvas.set_color_map('ocean'))
            display_cmap_menu.addAction('Oranges', lambda: self.canvas.set_color_map('Oranges'))
            display_cmap_menu.addAction('Paired', lambda: self.canvas.set_color_map('Paired'))
            display_cmap_menu.addAction('Pastel', lambda: self.canvas.set_color_map('pastel'))
            display_cmap_menu.addAction('Random', lambda: self.canvas.set_color_map('random'))
            display_cmap_menu.addAction('Winter', lambda: self.canvas.set_color_map('winter'))

            display_imap_menu = QtWidgets.QMenu('Intensity')
            display_imap_menu.addAction('Reset', lambda: (
                self.canvas.set_intensity_map('ramp')
            ))
            display_imap_menu.addSeparator()
            display_imap_menu.addAction('Equa', lambda: self.canvas.set_intensity_map('equa'))
            display_imap_menu.addAction('Expo', lambda: self.canvas.set_intensity_map('expo'))
            display_imap_menu.addAction('Gamma', lambda: self.canvas.set_intensity_map('gamma'))
            display_imap_menu.addAction('Jigsaw', lambda: self.canvas.set_intensity_map('jigsaw'))
            display_imap_menu.addAction('Lasritt', lambda: self.canvas.set_intensity_map('lasritt'))
            display_imap_menu.addAction('Log', lambda: self.canvas.set_intensity_map('log'))
            display_imap_menu.addAction('Neg', lambda: self.canvas.set_intensity_map('neg'))
            display_imap_menu.addAction('NegLog', lambda: self.canvas.set_intensity_map('neglog'))
            display_imap_menu.addAction('Null', lambda: self.canvas.set_intensity_map('null'))
            display_imap_menu.addAction('Ramp', lambda: self.canvas.set_intensity_map('ramp'))
            display_imap_menu.addAction('Stairs', lambda: self.canvas.set_intensity_map('stairs'))
            display_imap_menu.addAction('UltraSmooth', lambda: self.canvas.set_intensity_map('ultrasmooth'))

            transform_menu.addMenu(transform_flip_menu)
            transform_menu.addMenu(transform_rotate_menu)

            display_menu.addMenu(display_scale_menu)
            display_menu.addMenu(display_cmap_menu)
            display_menu.addMenu(display_imap_menu)
            display_menu.addAction('Contrast', lambda: self.set_contrast())

            menu.addMenu(copy_menu)
            menu.addSeparator()

            menu.addMenu(display_menu)
            menu.addMenu(transform_menu)

            menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)


# noinspection PyUnresolvedReferences
class HCalcForm(QWidget, Ui_FormHeaderCalculator):
    def __init__(self, parent: MainWindow, fits_array: FitsArray):
        super(HCalcForm, self).__init__(parent)
        self.parent = parent
        self.fits_array = fits_array
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.load()

        self.pushButtonGO.clicked.connect(self.go)

    def go(self):
        warn = 0

        if not self.groupBoxTime.isChecked() and not self.groupBoxJDAirmass.isChecked():
            self.parent.gui_functions.error("No action. Nothing to do!")
            return

        progress = QtWidgets.QProgressDialog("Calculating ...", "Abort", 0, len(self.fits_array), self)

        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setFixedSize(progress.sizeHint() + QSize(400, 0))
        progress.setWindowTitle('MYRaf: Please Wait')
        progress.setAutoClose(True)

        for iteration, fits in enumerate(self.fits_array):
            progress.setLabelText(f"Operating on {fits.file.name}")
            if progress.wasCanceled():
                progress.setLabelText("ABORT!")
                break

            try:
                current_time = Time(fits.pure_header()[self.comboBoxTimeInHeader.currentText()])
                amount = self.doubleSpinBoxTimeAmount.value()
                if self.groupBoxTime.isChecked():
                    time_format = self.comboBoxTimeType.currentText()
                    if time_format == "Second":
                        time_delta = relativedelta(seconds=amount)
                    elif time_format == "Minute":
                        time_delta = relativedelta(minutes=amount)
                    elif time_format == "Hour":
                        time_delta = relativedelta(hours=amount)
                    elif time_format == "Day":
                        time_delta = relativedelta(days=amount)
                    elif time_format == "Month":
                        time_delta = relativedelta(months=amount)
                    elif time_format == "Year":
                        time_delta = relativedelta(years=amount)
                    else:
                        self.parent.gui_functions.error("Unrecognized time format.")
                        return
                    new_time = Time(current_time.to_datetime() + time_delta)
                    fits.hedit("MY-DATE", new_time.strftime("%Y-%m-%d %H:%M:%S.%f"), comments="Calculated By MYRaf")

                if self.groupBoxJDAirmass.isChecked():
                    observatory = fits.pure_header()[self.comboBoxObservatoryInHeader.currentText()]
                    obj = fits.pure_header()[self.comboBoxObjectInHeader.currentText()]
                    sky_object = SkyCoord.from_name(obj)
                    location = ObservatoriesForm.get(observatory)

                    ltt_heli = current_time.light_travel_time(sky_object, location=location, kind="heliocentric")
                    hjd = current_time + ltt_heli
                    ltt_bary = current_time.light_travel_time(sky_object, location=location, kind="barycentric")
                    bjd = current_time + ltt_bary

                    altaz_frame = AltAz(obstime=current_time, location=location)
                    altaz = sky_object.transform_to(altaz_frame)
                    airmass = altaz.secz
                    fits.hedit(["my_bjd", "my_hjd", "my_armss"], [hjd.jd, bjd.jd, airmass.value],
                               comments=["Calculated By MYRaf", "Calculated By MYRaf", "Calculated By MYRaf"])
            except Exception as e:
                warn += 1
                self.parent.logger.warning(e)

            progress.setValue(iteration)
        progress.close()

        if warn > 0:
            self.parent.gui_functions.toast(f"There were problems with {warn} files.\nCheck logs.")

    def load(self):
        header = self.fits_array[0].header()

        self.comboBoxTimeInHeader.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxTimeInHeader, list(header.columns))

        self.comboBoxObjectInHeader.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxObjectInHeader, list(header.columns))

        self.comboBoxObservatoryInHeader.clear()
        self.parent.gui_functions.add_to_combo(self.comboBoxObservatoryInHeader, list(header.columns))


# noinspection PyUnresolvedReferences
class ObservatoriesForm(QWidget, Ui_FormObservatory):
    def __init__(self, parent: MainWindow):
        super(ObservatoriesForm, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.astropy_observatories = EarthLocation.get_site_names()
        self.my_observatories = []

        self.load()

        self.comboBoxObservatory.currentIndexChanged.connect(self.show_observatory)
        self.pushButtonSave.clicked.connect(self.save_observatory)
        self.pushButtonRremove.clicked.connect(self.remove)

    @staticmethod
    def get(name):

        observatory_file = database_dir() / "settings.json"
        if observatory_file.exists():
            with open(observatory_file, "r") as f:
                local_observatories = json.load(f)
        else:
            local_observatories = DEFAULT_OBSERVATORIES

        if name in local_observatories:
            values = local_observatories[name]
            return EarthLocation(
                lat=values["lat"],
                lon=values["lon"],
                height=values["height"]
            )

        observatory = EarthLocation.of_site(name)
        return observatory

    def remove(self):
        name = self.comboBoxObservatory.currentText()
        self.observatory_remove(name)

    def save_observatory(self):
        name = self.lineEditName.text()
        lat = self.doubleSpinBoxLatitude.value()
        lon = self.doubleSpinBoxLongitude.value()
        height = self.doubleSpinBoxAltitude.value()

        if name == "":
            self.parent.logger.warning("No observatory name")
            self.parent.gui_functions.error("No observatory name was given")
            return

        if name == "NEW":
            self.parent.logger.warning("Are you serious?\n`NEW` is reserved...")
            self.parent.gui_functions.error("Are you serious?\n`NEW` is reserved...")
            return

        if name in self.astropy_observatories:
            self.parent.logger.warning("Observatory with this name already exists. And it cannot be updated")
            self.parent.gui_functions.error("Observatory with this name already exists. And it cannot be updated")
            return

        self.observatories = {
            name: {
                "lat": lat,
                "lon": lon,
                "height": height
            }
        }

        self.load()
        self.comboBoxObservatory.setCurrentText(name)

    def load(self):
        added_observatories = list(self.observatories)
        self.comboBoxObservatory.clear()
        self.parent.gui_functions.add_to_combo(
            self.comboBoxObservatory, added_observatories + self.astropy_observatories
        )

    def show_observatory(self):
        self.pushButtonSave.setEnabled(False)
        self.pushButtonRremove.setEnabled(False)

        if self.comboBoxObservatory.currentIndex() == 0:
            self.lineEditName.setText("")
            self.doubleSpinBoxLatitude.setValue(0)
            self.doubleSpinBoxLongitude.setValue(0)
            self.doubleSpinBoxAltitude.setValue(0)
            self.pushButtonSave.setEnabled(True)
            self.pushButtonRremove.setEnabled(False)
            return

        name = self.comboBoxObservatory.currentText()

        if name == "":
            return

        observatories = self.observatories

        if name in observatories:
            obs = observatories[name]
            self.lineEditName.setText(name)
            self.doubleSpinBoxLatitude.setValue(obs["lat"])
            self.doubleSpinBoxLongitude.setValue(obs["lon"])
            self.doubleSpinBoxAltitude.setValue(obs["height"])
            self.pushButtonSave.setEnabled(True)
            self.pushButtonRremove.setEnabled(True)
            return

        observatory = EarthLocation.of_site(name)
        self.lineEditName.setText(name)
        self.doubleSpinBoxLatitude.setValue(observatory.lat.degree)
        self.doubleSpinBoxLongitude.setValue(observatory.lon.degree)
        self.doubleSpinBoxAltitude.setValue(observatory.height.value)

    @classmethod
    def observatory_file(cls) -> Path:
        return database_dir() / "observatories.json"

    @property
    def observatories(self) -> dict:
        observatory_file = self.observatory_file()
        if not observatory_file.exists():
            with open(observatory_file, "w") as f:
                json.dump(DEFAULT_OBSERVATORIES, f)

        try:
            with open(observatory_file, "r") as f:
                return json.load(f)
        except Exception as e:
            self.parent.logger.warning(e)
            return DEFAULT_OBSERVATORIES

    @observatories.setter
    def observatories(self, obs):
        observatories = self.observatories
        observatory_file = self.observatory_file()
        with open(observatory_file, "w") as f:
            observatories.update(obs)
            json.dump(observatories, f)

    def observatory_remove(self, name):
        if not self.parent.gui_functions.ask("Delete Observatory", "Are you sure?"):
            return

        observatories = self.observatories
        observatories.pop(name)
        observatory_file = self.observatory_file()
        with open(observatory_file, "w") as f:
            json.dump(observatories, f)

        self.load()


# noinspection PyUnresolvedReferences
class Setting:
    def __init__(self, logger: Logger):
        self.logger = logger

    @classmethod
    def settings_file(cls):
        return database_dir() / "settings.json"

    @property
    def settings(self) -> dict:
        settings_file = self.settings_file()
        if not settings_file.exists():
            with open(settings_file, "w") as f:
                json.dump(DEFAULT_SETTINGS, f)
        try:
            with open(settings_file, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(e)
            return DEFAULT_SETTINGS

    @settings.setter
    def settings(self, setting):
        observatory_file = self.settings_file()
        with open(observatory_file, "w") as f:
            json.dump(setting, f)


# noinspection PyUnresolvedReferences
class SettingsForm(QWidget, Ui_FormSettings):
    def __init__(self, parent: MainWindow):
        super(SettingsForm, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        self.spinBoxDisplayInterval.valueChanged.connect(self.save_settings)
        self.doubleSpinBoxZMag.valueChanged.connect(self.save_settings)
        self.lineEditAstrometryNetApiKey.textChanged.connect(self.save_settings)
        self.checkBoxAstrometryNetSaveKey.stateChanged.connect(self.save_settings)
        self.load_settings()

    def load_settings(self):
        settings = self.parent.settings.settings
        self.spinBoxDisplayInterval.setValue(settings["display"]["interval"])
        self.doubleSpinBoxZMag.setValue(settings["ZMag"])

    def save_settings(self):

        settings = self.parent.settings.settings
        settings["display"]["interval"] = self.spinBoxDisplayInterval.value()
        settings["ZMag"] = self.doubleSpinBoxZMag.value()
        settings["edit"]["wcs"]["save"] = self.checkBoxAstrometryNetSaveKey.isChecked()
        if settings["edit"]["wcs"]["save"]:
            settings["edit"]["wcs"]["astrometry_apikey"] = self.lineEditAstrometryNetApiKey.text()
        else:
            settings["edit"]["wcs"]["astrometry_apikey"] = ""

        self.parent.settings.settings = settings


# noinspection PyUnresolvedReferences
class AboutForm(QWidget, Ui_FormAbout):
    def __init__(self, parent: MainWindow):
        super(AboutForm, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

        self.setWindowIcon(QIcon(LOGO))

        pixmap = QPixmap(LOGO)
        scaled_pixmap = pixmap.scaled(90, 90, Qt.KeepAspectRatio)
        self.labelLogo.setPixmap(scaled_pixmap)


# noinspection PyUnresolvedReferences
class LogForm(QWidget, Ui_FormLog):
    def __init__(self, parent: MainWindow):
        super(LogForm, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.refresh()

        self.pushButtonRefresh.clicked.connect(self.refresh)
        self.pushButtonSave.clicked.connect(self.save)
        self.pushButtonClear.clicked.connect(self.clear)

    def clear(self):
        if Path(self.parent.log_file).exists():
            with open(self.parent.log_file, "w") as f:
                f.write("")
            self.refresh()

    def refresh(self):
        if self.parent.log_file is not None:
            with open(self.parent.log_file, 'r') as f:
                self.listWidget.clear()
                self.parent.gui_functions.add_to_list(self.listWidget, list(map(str.strip, f.readlines())))
                self.listWidget.scrollToBottom()

    def save(self):
        file = self.parent.gui_functions.save_file("Save", "log (*.log);")
        if file:
            dest = Path(file)
            src = Path(self.parent.log_file)
            dest.write_text(src.read_text())


# noinspection PyUnresolvedReferences
def main():
    parser = argparse.ArgumentParser(description='MYRaf V3 Beta')
    parser.add_argument("--logger", "-ll", default=10, type=int,
                        help="Logger level: CRITICAL=50, ERROR=40, WARNING=30, INFO=20, DEBUG=10, NOTSET=0")
    parser.add_argument("--logfile", "-lf", default=None, type=str, help="Path to log file")

    args = parser.parse_args()

    app = QtWidgets.QApplication(argv)
    qdarktheme.setup_theme(theme='dark', custom_colors=SCHEMA, corner_shape="sharp")
    window = MainWindow(logger_level=args.logger, log_file=args.logfile)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
