# -*- coding: utf-8 -*-
#
# fPlot.py -- Plotting function for embedded matplotlib widget with Ginga.
#
# Thanks for Eric Jeschke (eric@naoj.org), https://github.com/ejeschke/ginga
# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org) and
#                Mohammad Niaei Shameoni (mshemuni@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.
    
try:
    from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas
    from ginga.mplw.FigureCanvasQt import setup_Qt
    from ginga.AstroImage import AstroImage
    from ginga.misc import log
except Exception as e:
    print("{}: Can't import ginga.".format(e))
    exit(0)

class FitsPlot:
    def __init__(self, chartDev, logger):
        self.logger = logger
        self.chartDev = chartDev
        self.fig = self.chartDev.fig
        self.logger.info("fplot is doing something.")
        self.images = []
        try:
            # create a ginga object and tell it about the figure
            self.chartDev.fig.clf()
            fi = ImageViewCanvas(self.logger)
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
            self.logger.error(e)
            
    def get_xy(self):
        return self.fitsimage.get_last_data_xy()
        
    def get_data_size(self):
        return self.fitsimage.get_data_size()
        
    def get_data(self, point=True):
        try:
            if point:
                x, y = self.get_xy()
                w, h = self.get_data_size()
                if 0 < x < w and 0 < y < h:
                    return self.fitsimage.get_data(int(x), int(y))
                else:
                    return None
            else:
                return self.fitsimage.get_data()
        except Exception as e:
            self.logger.error(e)

    def get_image_data(self):
        return self.fitsimage.get_data()

    def clear(self):
        try:
            self.fitsimage.clear()
        except Exception as e:
            self.logger.error(e)

    def load(self, fitspath):
        self.logger.info("fplot is loading image.")
        try:
            # clear plotting area
            self.chartDev.fig.gca().cla()
            # load an image
            self.image = AstroImage(logger=self.logger)
            self.image.load_file(fitspath)
            self.fitsimage.set_image(self.image)
            self.fitsimage.add_axes()
        except Exception as e:
            self.logger.error(e)
            
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
