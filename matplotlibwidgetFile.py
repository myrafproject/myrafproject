try:
    from PyQt5 import QtCore, QtWidgets
except Exception as e:
    print("{}. Can't import PyQt5.".format(e))
    exit(0)

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

    from matplotlib.figure import Figure
    from matplotlib import gridspec as gridspec
    from pylab import rcParams
except Exception as e:
    print("{}. Can't import matplotlib.".format(e))
    exit(0)


class MplCanvas(FigureCanvas):

    def __init__(self):

        self.fig = Figure(facecolor='#FFFFFF')
        self.fig.subplots_adjust(left=0.048, bottom=0.061, right=0.857, top=0.960)
        rcParams['lines.linestyle'] = ""
        gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
        self.axlc1 = self.fig.add_subplot(gs[0])
        self.axlc2 = self.fig.add_subplot(gs[1], sharex=self.axlc1)
        self.axlc1.get_xaxis().get_major_formatter().set_scientific(False)
        self.axlc2.get_xaxis().get_major_formatter().set_scientific(False)
        self.xtitle = "Time"
        self.ytitle = "Diff. Mag. (V - C)"
        self.y2title = "Diff. Mag. (C - R)"
        self.PlotTitle = "Photometry Plot, MYRaf Project v3.0.0"
        self.grid_status = True
        self.xaxis_style = 'linear'
        self.yaxis_style = 'linear'
        self.format_labels()
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fig.tight_layout()

    def format_labels(self):
        self.axlc1.set_title(self.PlotTitle)
        self.axlc1.title.set_fontsize(10)
        self.axlc2.set_xlabel(self.xtitle, fontsize=9)
        self.axlc1.set_ylabel(self.ytitle, fontsize=9)
        self.axlc2.set_ylabel(self.y2title, fontsize=9)

        labels_x1 = self.axlc1.get_xticklabels()
        labels_y1 = self.axlc1.get_yticklabels()

        labels_x2 = self.axlc2.get_xticklabels()
        labels_y2 = self.axlc2.get_yticklabels()

        for xlabel in labels_x1:
            xlabel.set_fontsize(8)
            xlabel.set_color('b')
        for ylabel in labels_y1:
            ylabel.set_fontsize(8)
            ylabel.set_color('b')

        for xlabel in labels_x2:
            xlabel.set_fontsize(8)
            xlabel.set_color('b')
        for ylabel in labels_y2:
            ylabel.set_fontsize(8)
            ylabel.set_color('b')

        return True


class matplotlibWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
        self.parent = parent