# -*- coding: utf-8 -*-
#
# fPlot.py -- Plotting function for embedded matplotlib widget with Ginga.
#
# Thanks for Eric Jeschke (eric@naoj.org), https://github.com/ejeschke/ginga
# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org) and
#                Mohammad Niaei Shameoni (mshemuni@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.

from myraflib import env

from ginga.mplw.ImageViewCanvasMpl import ImageViewCanvas
from ginga.mplw.FigureCanvasQt import setup_Qt
from ginga.AstroImage import AstroImage
from ginga.misc import log


class FitsPlot(object):
    def __init__(self, chartDev, verb=False, debugger=False):
        self.verb = verb
        self.debugger = debugger
        self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        self.chartDev = chartDev
        use_logger = debugger
        self.logger.log("fplot is doning something.")
        self.images = []
        try:
            logger = log.get_logger(null=not use_logger, log_stderr=True)
            # create a ginga object and tell it about the figure
            self.chartDev.fig.clf()
            fi = ImageViewCanvas(logger)
            fi.enable_autocuts('on')
            fi.set_autocut_params('zscale')
    
            fi.set_figure(self.chartDev.fig)
    
            fi.ui_setActive(True)
            self.fitsimage = fi
            setup_Qt(chartDev, fi)
    
            # enable all interactive features
            fi.get_bindings().enable_all(True)
            self.fitsimage = fi
        except Exception as e:
            self.logger.log(e)
            
    def get_xy(self):
        return(self.fitsimage.get_last_data_xy())
        
    def get_data_size(self):
        return(self.fitsimage.get_data_size())
        
    def get_data(self, point=True):
        if point:
            x, y = self.get_xy()
            w, h = self.get_data_size()
            if 0 < x < w and 0 < y < h:
                return(self.fitsimage.get_data(int(x), int(y)))
            else:
                return(float('NaN'))
        else:
            return(self.fitsimage.get_data())

    def clear(self):
        try:
            self.fitsimage.clear()
        except Exception as e:
            self.logger.log(e)

    def load(self, fitspath):
        self.logger.log("fplot is loading image.")
        try:
            # clear plotting area
            self.chartDev.fig.gca().cla()
            # load an image
            image = AstroImage()
            image.load_file(fitspath)
            self.fitsimage.set_image(image)
            self.fitsimage.add_axes()
        except Exception as e:
            self.logger.log(e)
            
    def load_array(self, fitspath):
        self.chartDev.fig.gca().cla()
        self.images = []
        for file in fitspath:
            self.images.append(AstroImage())
            self.images[-1].load_file(file)
        
        
    def show_from_all(self, number):
        if self.images is not None:
            if 0 <= number < len(self.images):
                self.fitsimage.set_image(self.images[number])
                self.fitsimage.add_axes()
        