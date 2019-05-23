# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:43:58 2019

@author: msh, yk
"""
try:
    import string
except Exception as e:
    print("{}: Can't import string?".format(e))
    exit(0)

try:
    from subprocess import Popen
    from subprocess import PIPE
    from subprocess import CalledProcessError
except Exception as e:
    print("{}: Can't import subprocess?".format(e))
    exit(0)
    
try:
    from json import dump
    from json import loads
except Exception as e:
    print("{}: Can't import json?".format(e))
    exit(0)
    
try:
    import random
except Exception as e:
    print("{}: Can't import random?".format(e))
    exit(0)

try:
    from numpy import genfromtxt
    from numpy import savetxt
    from numpy import array as ar
except Exception as e:
    print("{}: Can't import numpy.".format(e))
    exit(0)

try:
    from os.path import expanduser
    from os.path import exists
    from os.path import isfile
    from os.path import dirname
    from os.path import basename
    from os.path import realpath
    from os.path import splitext
    from os.path import abspath
    from os.path import getsize
    from os import remove
    from os import mkdir
except Exception as e:
    print("{}: Can't import os?".format(e))
    exit(0)

try:
    from glob import glob
except Exception as e:
    print("{}: Can't import glob?".format(e))
    exit(0)

try:
    from shutil import copy2
    from shutil import move
except Exception as e:
    print("{}: Can't import shutil?".format(e))
    exit(0)

try:
    from datetime import datetime
except Exception as e:
    print("{}: Can't import datetime?".format(e))
    exit(0)

try:
    from getpass import getuser
except Exception as e:
    print("{}: Can't import getpass?".format(e))
    exit(0)

try:
    from platform import uname
    from platform import system
except Exception as e:
    print("{}: Can't import platform?".format(e))
    exit(0)

try:
    from inspect import currentframe
    from inspect import getouterframes
except Exception as e:
    print("{}: Can't import inspect?".format(e))
    exit(0)

try:
    import tempfile
except Exception as e:
    print("{}: Can't import tempfile?".format(e))
    exit(0)
    
class Logger():
    def __init__(self, verb=True, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.log_dir = abspath("{}/mylog/".format(expanduser("~")))
        self.obs_dir = abspath("{}/myobservat/".format(expanduser("~")))
        self.log_file = abspath("{}/log.my".format(self.log_dir))
        self.mini_log_file = abspath("{}/mlog.my".format(self.log_dir))
        self.tmp_dir = tempfile.gettempdir()
        
        if not(exists(self.log_dir) and not isfile(self.log_dir)):
            mkdir(self.log_dir)
            
        if not(exists(self.obs_dir) and not isfile(self.obs_dir)):
            mkdir(self.obs_dir)
            
        self.setting_file = abspath("{}/.myset".format(expanduser("~")))
        
        self.cos_set_file = abspath("{}/.myset_cosmiccleaner.set".format(
                expanduser("~")))
        self.cos_set = {"gain": 2.2, "reno": 10.0, "sicl": 5.5, "sifr": 0.3,
                        "obli": 5.0, "mait": 2, "crma": False}
        
        self.pho_set_file = abspath("{}/.myset_photometry.set".format(
                expanduser("~")))
        self.pho_set = {"std_mag": False, "std_mag_nomad": True,
                        "std_mag_usno": True, "std_mag_gaia": True,
                        "std_mag_radius": 10.0, "datapar_exposure": "exptime",
                        "datapar_filter": "subset",
                        "photpar_aperture": "10.0, 15.0", "photpar_zmag": 25.0,
                        "photpar_gain": "gain", "wcs_ra": "ra",
                        "wcs_dec": "dec", "lot_obse": "observat",
                        "lot_time": "JD", "stf_thr": 2.0, "stf_max": 500,
                        "header_to_use": ""}
        
        self.cal_set_file = abspath("{}/.myset_calibration.set".format(
                expanduser("~")))
        self.cal_set = {"b_combine": 1, "b_rejection": 0,
                        "d_combine": 0, "d_rejection": 0, "d_scale": 1,
                        "f_combine": 0, "f_rejection": 0}
        
        self.cal_ast_file = abspath("{}/.myset_astrometry.set".format(
                expanduser("~")))
        self.cal_ast = {"online": False,
                        "server": "http://nova.astrometry.net/api/",
                        "apike": "abhfixfhhxsignyo"}
        
        self.observat_dir = abspath("./observat/")
        
    def execute(self, cmd):
        try:
            p = Popen(cmd, stdout=PIPE, universal_newlines=True)
            for stdout_line in iter(p.stdout.readline, ""):
                yield stdout_line 
            p.stdout.close()
            return_code = p.wait()
            if return_code:
                raise CalledProcessError(return_code, cmd)
        except Exception as e:
            self.log(e)
        
    def random_string(self, length):
        return(''.join(random.choices(
                string.ascii_uppercase + string.digits, k=length)))
        
    def time_stamp(self):
        return(str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")))
        
    def time_stamp_(self):
        return(str(datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")))
    
    def user_name(self):
        return(str(getuser()))
    
    def system_info(self):
        si = uname()
        return("{}, {}, {}, {}".format(si[0], si[2], si[5], self.user_name()))
        
    def caller_function(self, pri=False):
        curframe = currentframe()
        calframe = getouterframes(curframe, 2)
        caller = calframe
        self.system_info()
        if pri:
            return("{}>{}>{}".format(
                    caller[0][3], caller[1][3], caller[2][3]))
        else:
            return(caller)
            
    def print_if(self, text):
        if self.verb:
            print("[{}|{}] --> {}".format(self.time_stamp(),
                  self.system_info(), text))
            
    def log(self, text):
        try:
            self.print_if(text)
            if self.debugger:
                log_file = open(self.log_file, "a")
                log_file.write("Time: {}\n".format(self.time_stamp()))
                log_file.write("System Info: {}\n".format(self.system_info()))
                log_file.write("Log: {}\n".format(text))
                log_file.write("Function: {}\n\n\n".format(
                        self.caller_function()))
                log_file.close()
                self.mini_log(text)
        except Exception as e:
            print(e)
        
    def mini_log(self, text):
        mini_log_file = open(self.mini_log_file, "a")
        mini_log_file.write("[{}|{}] --> {}\n".format(self.time_stamp(),
                            self.system_info(), text))
        mini_log_file.close()
        
    def dump_mlog(self):
        try:
            self.log("Deleting the Mini Log file.")
            mini_log_file = open(self.mini_log_file, "w")
            mini_log_file.close()
        except Exception as e:
            print(e)
        
    def dump_log(self):
        try:
            self.log("Deleting the Log file.")
            log_file = open(self.log_file, "w")
            log_file.close()
        except Exception as e:
            print(e)
        
    def is_it_windows(self):
        self.log("Checking if the OS is Windows")
        return(system() == 'Windows')
        
    def is_it_linux(self):
        self.log("Checking if the OS is Linux")
        return(system() == 'Linux')
        
    def is_it_other(self):
        self.log("Checking if the OS is Other")
        return(not (self.is_it_linux() or self.is_it_windows()))
        
    def beep(self):
        print("\a")
        
class File():
    def __init__(self, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = Logger(verb=self.verb, debugger=self.debugger)
            
    def list_of_observatories(self):
        try:
            if self.is_dir(self.logger.obs_dir):
                observatories = self.list_of_fiels(self.logger.obs_dir, "*")
                return(observatories)
            else:
                self.mkdir(self.logger.obs_dir)
        except Exception as e:
            self.logger.log(e)
        
    def temp_cleaner(self):
        files = self.list_of_fiels(self.logger.tmp_dir, "myraf*.fits")
        for file in files:
            self.rm(file)
        
    def get_size(self, path):
        try:
            if self.is_file(path):
                return(getsize(path))
        except Exception as e:
            self.logger.log(e)
        
    def abs_path(self, path):
        try:
            return(abspath(path))
        except Exception as e:
            self.logger.log(e)
            

    def list_in_path(self, path):
        try:
            pt = self.abs_path(path)
            return(sorted(glob(pt)))
        except Exception as e:
            self.logger.log(e) 

    def list_of_fiels(self, path, ext="*"):
        try:
            if self.is_dir(path):
                pt = self.abs_path("{}/{}".format(path, ext))
                return(sorted(glob(pt)))
        except Exception as e:
            self.logger.log(e)  
            
    def is_file(self, src):
        self.logger.log("Checking if file {0} exist".format(src))
        try:
            return(isfile(src))
        except Exception as e:
            self.logger.log(e)
            return(False)
        
    def is_dir(self, src):
        self.logger.log("Checking if directory {0} exist".format(src))
        try:
            return((not self.is_file(src)) and exists(src))
        except Exception as e:
            self.logger.log(e)
            return(False)
    
    def get_home_dir(self):
        self.logger.log("Getting Home dir path")
        try:
            return(expanduser("~"))
        except Exception as e:
            self.logger.log(e)
    
    def get_base_name(self, src):
        self.logger.log("Finding path and file name for {0}".format(src))
        try:
            pn = dirname(realpath(src))
            fn = basename(realpath(src))
            return(pn, fn)
        except Exception as e:
            self.logger.log(e)
    
    def get_extension(self, src):
        self.logger.log("Finding extension for {0}".format(src))
        try:
            return(splitext(src))
        except Exception as e:
            self.logger.log(e)
            
    def split_file_name(self, src):
        self.logger.log("Chopping path {0}".format(src))
        try:
            path, name = self.get_base_name(src)
            name, extension = self.get_extension(name)
            return(path, name, extension)
        except Exception as e:
            self.logger.log(e)
            
    def cp(self, src, dst):
        self.logger.log("Copying file {0} to {1}".format(src, dst))
        try:
            copy2(src, dst)
        except Exception as e:
            self.logger.log(e)
            
    def rm(self, src):
        self.logger.log("Removing file {0}".format(src))
        try:
            remove(src)
        except Exception as e:
            self.logger.log(e)
            
    def mv(self, src, dst):
        self.logger.log("Moving file {0} to {1}".format(src, dst))
        try:
            move(src, dst)
        except Exception as e:
            self.logger.log(e)
            
    def mkdir(self, path):
        try:
            if not self.is_dir:
                mkdir(path)
        except Exception as e:
            self.logger.log(e)
            
    def read_pysexcat(self, file):
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
            
                return(ar(ret))
        except Exception as e:
            self.logger.log(e)
            
    def read_array(self, src, dm=" ", dtype=float):
        self.logger.log("Reading {0}".format(src))
        try:
            return(genfromtxt(src, comments='#', delimiter=dm, dtype=dtype))
        except Exception as e:
            self.logger.log(e)
            
    def write_array(self, src, arr, dm=" ", h=""):
        self.logger.log("Writing to {0}".format(src))
        try:
            arr = ar(arr)
            savetxt(src, arr, delimiter=dm, newline='\n', header=h)
        except Exception as e:
            self.logger.log(e)
    def write_list(self, dest, the_list):
        f = open(dest, "w")
        for i in the_list:
            f.write("{}\n".format(i))
        
        f.close()
        
    def write_json(self, file, dic):
        try:
            with open(file, 'w') as set_file:
                dump(dic, set_file)
        except Exception as e:
            print("hata")
            self.logger.log(e)
            
    def read_json(self, file):
        try:
            with open(file, 'r') as myfile:
                data=myfile.read()
                
            settings = loads(data)
            
            return(settings)
        except Exception as e:
            self.logger.log(e)
            
    def write_set(self, dic, typ):
        if typ == "cos":
            self.write_json(self.logger.cos_set_file, dic)
        elif typ == "pho":
            self.write_json(self.logger.pho_set_file, dic)
        elif typ == "cal":
            self.write_json(self.logger.cal_set_file, dic)
        elif typ == "ast":
            self.write_json(self.logger.cal_ast_file, dic)
            
    def read_set(self, typ):
        if typ == "cos":
            try:
                dic = self.read_json(self.logger.cos_set_file)
                for key, value in dic.items():
                    if value is None:
                        dic[value] = self.logger.cos_set[value]
                return(dic)
            except Exception as e:
                self.logger.log(e)
                return(self.logger.cos_set)
                
        elif typ == "pho":
            try:
                dic = self.read_json(self.logger.pho_set_file)
                for key, value in dic.items():
                    if value is None:
                        dic[value] = self.logger.pho_set[value]
                return(dic)
            except Exception as e:
                self.logger.log(e)
                return(self.logger.pho_set)
                
        elif typ == "cal":
            try:
                dic = self.read_json(self.logger.cal_set_file)
                for key, value in dic.items():
                    if value is None:
                        dic[value] = self.logger.cal_set[value]
                return(dic)
            except Exception as e:
                self.logger.log(e)
                return(self.logger.cal_set)
                
        elif typ == "ast":
            try:
                dic = self.read_json(self.logger.cal_ast_file)
                for key, value in dic.items():
                    if value is None:
                        dic[value] = self.logger.cal_ast[value]
                return(dic)
            except Exception as e:
                self.logger.log(e)
                return(self.logger.cal_ast)