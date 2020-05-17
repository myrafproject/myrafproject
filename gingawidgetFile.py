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
    print("{}. Can't import PyQt5.".format(e))
    exit(0)
    
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
except Exception as e:
    print("{}. Can't import matplotlib.".format(e))
    exit(0)
    

class MplCanvas(FigureCanvas):

    def __init__(self):
        
        # create a regular matplotlib figure
        try:
            self.fig = plt.figure()
            FigureCanvas.__init__(self, self.fig)
            FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
        except Exception as e:
            print(e)

class gingaWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        try:
            QtWidgets.QWidget.__init__(self, parent)
            self.canvas = MplCanvas()
            self.vbl = QtWidgets.QVBoxLayout()
            self.vbl.addWidget(self.canvas)
            self.setLayout(self.vbl)
            self.parent = parent
        except Exception as e:
            print(e)
