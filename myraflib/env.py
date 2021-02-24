# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:43:58 2019

@author: msh, yk
"""
import tempfile
from json import dump, loads
from os import remove, mkdir
from os.path import getsize, abspath, isfile, exists, expanduser, realpath, dirname, basename, splitext
from glob import glob
from shutil import copy2, move

from numpy import array as ar, genfromtxt, savetxt


class File():
    def __init__(self, logger):
        self.logger = logger
        self.tmp_dir = tempfile.gettempdir()

    def temp_cleaner(self, files="myraf*.*"):
        """Removes myraf files in /tmp"""
        files = self.list_of_fiels(self.tmp_dir, files)
        for file in files:
            self.rm(file)

    def get_size(self, path):
        """Return size of a given file"""
        try:
            if self.is_file(path):
                return getsize(path)
        except Exception as e:
            self.logger.error(e)

    def abs_path(self, path):
        """Return Absolute path of a given path"""
        try:
            return abspath(path)
        except Exception as e:
            self.logger.error(e)

    def list_in_path(self, path):
        """Returns file/directory in a given path"""
        try:
            pt = self.abs_path(path)
            return sorted(glob(pt))
        except Exception as e:
            self.logger.error(e)

    def list_of_fiels(self, path, ext="*"):
        """Returns file in a given path with given extension"""
        try:
            if self.is_dir(path):
                pt = self.abs_path("{}/{}".format(path, ext))
                return sorted(glob(pt))
        except Exception as e:
            self.logger.error(e)

    def is_file(self, src):
        """Checks if given path is file"""
        self.logger.info("Checking if file {0} exist".format(src))
        try:
            return isfile(src)
        except Exception as e:
            self.logger.error(e)
            return False

    def is_dir(self, src):
        """Checks if given path is directory"""
        self.logger.info("Checking if directory {0} exist".format(src))
        try:
            return (not self.is_file(src)) and exists(src)
        except Exception as e:
            self.logger.error(e)
            return False

    def get_home_dir(self):
        """Return users home directory"""
        self.logger.info("Getting Home dir path")
        try:
            return expanduser("~")
        except Exception as e:
            self.logger.error(e)

    def get_base_name(self, src):
        """Returns base path of a given file"""
        self.logger.info("Finding path and file name for {0}".format(src))
        try:
            pn = dirname(realpath(src))
            fn = basename(realpath(src))
            return pn, fn
        except Exception as e:
            self.logger.error(e)

    def get_extension(self, src):
        """Returns extension of a given file"""
        self.logger.info("Finding extension for {0}".format(src))
        try:
            return splitext(src)
        except Exception as e:
            self.logger.error(e)

    def split_file_name(self, src):
        """Retuns path and name of a file"""
        self.logger.info("Chopping path {0}".format(src))
        try:
            path, name = self.get_base_name(src)
            name, extension = self.get_extension(name)
            return path, name, extension
        except Exception as e:
            self.logger.error(e)

    def cp(self, src, dst):
        """Copies a given file"""
        self.logger.info("Copying file {0} to {1}".format(src, dst))
        try:
            copy2(src, dst)
        except Exception as e:
            self.logger.error(e)

    def rm(self, src):
        """Removes a given file"""
        self.logger.info("Removing file {0}".format(src))
        try:
            remove(src)
        except Exception as e:
            self.logger.error(e)

    def mv(self, src, dst):
        """Moves a given file"""
        self.logger.info("Moving file {0} to {1}".format(src, dst))
        try:
            move(src, dst)
        except Exception as e:
            self.logger.error(e)

    def mkdir(self, path):
        """Makes a directory"""
        try:
            if not self.is_dir:
                mkdir(path)
        except Exception as e:
            self.logger.error(e)

    def read_pysexcat(self, file):
        """Reads pysexcat file and returns as an array"""
        try:
            if self.is_file(file):
                the_file = open(file, "r")
                ret = []
                for line in the_file:
                    if not line.startswith("#"):
                        ln = line.replace("\n", "").split()
                        if float(ln[2]) != 99 and float(ln[3]) != 99:
                            ret.append(ar([float(ln[0]), float(ln[1]),
                                           float(ln[2]), float(ln[3]),
                                           float(ln[4]), float(ln[5]),
                                           float(ln[6]), float(ln[7])]))

                return ar(ret)
        except Exception as e:
            self.logger.error(e)

    def read_array(self, src, dm=" ", dtype=float):
        """Reads an array from a file"""
        self.logger.info("Reading {0}".format(src))
        try:
            return genfromtxt(src, comments='#', delimiter=dm, dtype=dtype)
        except Exception as e:
            self.logger.error(e)

    def write_array(self, src, arr, dm=" ", h=""):
        """Writes an array to a file"""
        self.logger.info("Writing to {0}".format(src))
        try:
            arr = ar(arr)
            savetxt(src, arr, delimiter=dm, newline='\n', header=h)
        except Exception as e:
            self.logger.error(e)

    def read_lis(self, src):
        try:
            ret = []
            with open(src, "r") as the_file:
                for the_line in the_file:
                    ret.append(the_line.strip())

            return ret
        except Exception as e:
            self.logger.error(e)

    def write_list(self, dest, the_list, dm=","):
        """Writes a list of a file"""
        with open(dest, "w") as f:
            for i in the_list:
                if type(i) == list:
                    f.write("{}\n".format(dm.join(i)))
                else:
                    f.write("{}\n".format(i))

    def write_json(self, file, dic):
        """Writes a dictionary ro a json file"""
        try:
            with open(file, 'w') as set_file:
                dump(dic, set_file, indent=1)
        except Exception as e:
            self.logger.error(e)

    def read_json(self, file):
        """Returns a dictionary from a json file"""
        try:
            with open(file, 'r') as myfile:
                data = myfile.read()

            settings = loads(data)

            return settings
        except Exception as e:
            self.logger.error(e)

    def read_myraf_result_file(self, file):
        if file:
            print(file)
            df = pd.read_csv(file)
            df = df[(df.occulted_star_mag != 'INDEF') & (df.occulted_star_mag_err != 'INDEF') &
                    (df.comp_star_mag != 'INDEF') & (df.comp_star_mag_err != 'INDEF') &
                    (df.check_star_mag != 'INDEF') & (df.check_star_mag_err != 'INDEF')]

            filters = df.Filter.unique()
            image_names = df.image.unique()
            self.filter_comboBox.clear()
            for filter in filters:
                print(filter)
                self.filter_comboBox.addItem(filter)

            self.GDevice.replace_list_con(self.file_list, image_names)
            self.opened_file_path.setText(file)
        else:
            self.logger.warning("No file selected")

        return True
