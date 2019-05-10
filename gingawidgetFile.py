# -*- coding: utf-8 -*-
#
# gingawidgetFile.py --
#        Plotting function for embedded matplotlib widget with Ginga.
#
# Thanks for Eric Jeschke (eric@naoj.org), https://github.com/ejeschke/ginga
# and
# https://gist.github.com/Maduranga/ for embedding matplotlibWidget into PyQt4

# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org) and
#        Mohammad Niaei Shameoni (mshemuni@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.

try:
    from PyQt5 import QtWidgets
except Exception as e:
    print("{}. PyQt5 is not installed?".format(e))
    exit(0)
    
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
except Exception as e:
    print("{}. Mtplotlib is not installed?".format(e))
    exit(0)
    
try:
    from myraflib import env
except Exception as e:
    print("{}. Cannot find myraflib".format(e))
    exit(0)
    

class MplCanvas(FigureCanvas):

    def __init__(self, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        
        if not self.fop.is_dir(self.logger.log_dir):
            self.fop.mkdir(self.logger.log_dir)
        
        # create a regular matplotlib figure
        self.logger.log("gingawidgetFile is doing something(MplCanvas).")
        try:
            self.fig = plt.figure()
            FigureCanvas.__init__(self, self.fig)
            FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
        except Exception as e:
            self.logger.log(e)

class gingaWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.fop = env.File(verb=self.verb, debugger=self.debugger)
        
        if not self.fop.is_dir(self.logger.log_dir):
            self.fop.mkdir(self.logger.log_dir)
        
        self.logger.log("gingawidgetFile is doing something(gingaWidget).")
        try:
            QtWidgets.QWidget.__init__(self, parent)
            self.canvas = MplCanvas()
            self.vbl = QtWidgets.QVBoxLayout()
            self.vbl.addWidget(self.canvas)
            self.setLayout(self.vbl)
            self.parent = parent
        except Exception as e:
            self.logger.log(e)