# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:35:56 2019

@author: msh, yk
"""
try:
    from sep import Background
    from sep import sum_circle
except Exception as e:
    
    print("Can't import sep: {}".format(e))
    exit(0)

try:
    from numpy import min as nmin
    from numpy import max as nmax
    from numpy import mean as nmea
    from numpy import median as nmed
    from numpy import sum as nsum
    from numpy import std as nstd
    from numpy import array as ar
    from numpy import rot90
    from numpy import log10
    from numpy import log
    from numpy import float64
    from numpy import power
    from numpy import sqrt
    from numpy import argmin
except:
    print("Can't import numpy.")
    exit(0)

try:
    from astropy.io import fits as fts
    from astropy.time import Time as tm
except:
    print("Can't import astropy.")
    exit(0)

try:
    from pyraf import iraf
    from iraf import imred
    from iraf import ccdred
except:
    print("Can't import pyraf/iraf.")
    exit(0)

try:
    import alipy
    from alipy import imgcat
except:
    print("Can't import alipy.")
    exit(0)

from . import env
from . import cosm

class Astronomy:
    def __init__(self):
        pass
    
    class Time:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
        
        def jd(self, utc):
            if utc is not None:
                try:
                    ret = tm(utc, scale='utc')
                    return(ret.jd)
                except Exception as e:
                    self.etc.log(e)
            else:
                self.logger.log("False Type: The value is not date")
                
        def jd_r(self, jd):
            try:
                t = tm(jd, format='jd', scale='tai')
                return(t.to_datetime())
            except Exception as e:
                self.logger.log(e)
        
    
    class Iraf:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
            self.fop = env.File(verb=self.verb, debugger=self.debugger)
            
        def imshift(self, file, output, dx, dy):
            try:
                iraf.imshift.unlearn()
                iraf.imshift(input=file, output=output, x=dx, y=dy)
                return(True)
            except Exception as e:
                self.logger.log(e)
                return(False)
            
            
        def zerocombine(self, files, output, method="median",
                        rejection="minmax", ccdtype=""):
            self.logger.log("Zerocombine Started")
            try:
                biases = ",".join(files)
                iraf.ccdred.zerocombine.unlearn()
                ccdred.instrument = "ccddb$kpno/camera.dat"
                out_file = "{}/myraf_biases.flist".format(self.logger.tmp_dir)
                f2w = open(out_file, "w")
                for i in files:
                    f2w.write("{}\n".format(i))
                f2w.close()
                biases = "@{}".format(out_file)
                
                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.zerocombine.unlearn()
                
                iraf.zerocombine(input=biases, output=output, combine=method,
                                 reject=rejection, ccdtype=ccdtype,
                                 Stdout="/dev/null")
                return(True)
            except Exception as e:
                self.logger.log(e)
                return(False)
            
        
        def darkcombine(self, files, output, zero=None, method="median",
                        rejection="minmax", ccdtype="", scale="exposure"):
            self.logger.log("Darkcombine Started")
            try:
                darks = ",".join(files)
                iraf.imred.unlearn()
                ccdred.instrument = "ccddb$kpno/camera.dat"
                
                
                out_file = "{}/myraf_darks.flist".format(self.logger.tmp_dir)
                f2w = open(out_file, "w")
                for i in files:
                    f2w.write("{}\n".format(i))
                f2w.close()
                darks = "@{}".format(out_file)
                
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.darkcombine.unlearn()
                
                if zero is not None:
                    iraf.ccdproc(images=darks, ccdtype='', fixpix='no',
                                 oversca="no", trim="no", zerocor='yes',
                                 darkcor='no', flatcor='no', zero=zero,
                                 Stdout="/dev/null")

                iraf.darkcombine(input=darks, output=output, combine=method,
                                 reject=rejection, ccdtype=ccdtype,
                                 scale=scale, process="no", Stdout="/dev/null")
                    
                return(True)
            except Exception as e:
                self.logger.log(e)
                return(False)
        
        def flatcombine(self, files, output, dark=None, zero=None, ccdtype="",
                        method="Median", rejection="minmax", subset="no"):
            self.logger.log("Flatcombine Started")
            try:
                flats = ",".join(files)
                iraf.imred.unlearn()
                ccdred.instrument = "ccddb$kpno/camera.dat"
                
                out_file = "{}/myraf_flats.flist".format(self.logger.tmp_dir)
                f2w = open(out_file, "w")
                for i in files:
                    f2w.write("{}\n".format(i))
                f2w.close()
                flats = "@{}".format(out_file)    
                
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.flatcombine.unlearn()
                
                iraf.flatcombine(input=flats, output=output, combine=method,
                                 reject=rejection, ccdtype=ccdtype,
                                 subset=subset, process="no",
                                 Stdout="/dev/null")
                
                if dark is not None:
                    darkcor = 'yes'
                else:
                    darkcor = 'no'
                
                if zero is not None:
                    zerocor='yes'
                else:
                    zerocor='no'
                    
                iraf.ccdproc(images=flats, ccdtype='', fixpix='no',
                             oversca="no", trim="no", zerocor=zerocor,
                             darkcor=darkcor, flatcor='no', zero=zero,
                             dark=dark, Stdout="/dev/null")
                return(True)
            except Exception as e:
                self.logger.log(e)
                return(False)
                
        def ccdproc(self, file, output=None, zero=None, dark=None, flat=None):
            self.logger.log("Ccdproc Started")
            try:
                iraf.imred.unlearn()
                ccdred.instrument = "ccddb$kpno/camera.dat"
                
                if output is None:
                    output = ""
                    
                if zero is None:
                    zeroCor = "no"
                else:
                    zeroCor = "yes"
                    
                if dark is None:
                    darkCor = "no"
                else:
                    darkCor = "yes"
                    
                if flat is None:
                    flatCor = "no"
                else:
                    flatCor = "yes"
                    
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                
                iraf.ccdproc(images=file, output=output, ccdtype='',
                             fixpix='no', oversca="no", trim="no",
                             zerocor=zeroCor, darkcor=darkCor,
                             flatcor=flatCor, zero=zero, dark=dark,
                             flat=flat, Stdout="/dev/null")
                return(True)
            except Exception as e:
                self.logger.log(e)
                return(False)
            
    class Fits:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
            self.fop = env.File(verb=self.verb, debugger=self.debugger)
            self.sma = Statistics.Math(verb=self.verb, debugger=self.debugger)
            
        def solve_field(self, file, out_file):
            pass
            
        def cosmic_cleaner(self, image, output, gain=2.2, readout_noise=10.0,
                           sigma_clip=5, sigma_fraction=0.3, object_limit=5,
                           max_iter=4, mask=False):
            
            data, header = cosm.fromfits(image)
            if data.ndim == 2:
                cos = cosm.cosmicsimage(data, gain=gain,
                                        readnoise=readout_noise,
                                        sigclip=sigma_clip,
                                        sigfrac=sigma_fraction,
                                        objlim=object_limit, verbose=self.verb)
                
                cos.run(maxiter=max_iter)
                cosm.tofits(output, cos.cleanarray, header)
                if mask:
                    pn, fn, ex = self.fop.split_file_name(output)
                    cosm.tofits("{}/{}_mask{}".format(pn, fn, ex),
                                cos.mask, header)
            pass
            
        def align(self, image, ref, output):
            identifications = alipy.ident.run(ref, [image], visu=False,
                                              sexkeepcat=False, verbose=False)
            outputshape = alipy.align.shape(ref)
            for the_id in identifications:
                if the_id.ok == True:
                    the_id.ukn.name, the_id.trans, the_id.medfluxratio
                    alipy.align.affineremap(the_id.ukn.filepath, the_id.trans,
                                            shape=outputshape, outdir=output)
                
        def star_finder(self, image, max_star=500):
            self.logger.log("Star finder started for {}".format(image))
            try:
                img = imgcat.ImgCat(image)
                img.makecat(rerun=True, keepcat=False, verbose=self.verb)
                img.makestarlist(skipsaturated=False, n=max_star,
                                 verbose=self.verb)
                ret = []
                for star in img.starlist:
                    ret.append([star.x, star.y, star.fwhm])
                    
                return(ar(ret))
            except Exception as e:
                self.logger.log(e)
                
        def subtract(self, img1, img2):
            self.logger.log("Subtraction for {} - {}".format(img1, img2))
            try:
                data1 = self.data(img1)
                data2 = self.data(img2)
                if data1 is not None and data2 is not None:
                    return(data1 - data2)
            except Exception as e:
                self.logger.log(e)
            
        def combine(self, files, combine_method):
            self.logger.log("Combine for {} files with {} methdo".format(
                    len(files), combine_method))
            try:
                if combine_method == "median":
                    if len(files) > 2:
                        arrays = []
                        for file in files:
                            data = self.data(file)
                            if data is not None:
                                arrays.append(data)
                                
                        arrays = ar(arrays)
                        medi = nmed(arrays, axis=0)
                        return(medi)
                            
                    else:
                        raise Exception('No enough file for median method')
                        
                elif combine_method == "average":
                    if len(files) > 1:
                        arrays = []
                        for file in files:
                            data = self.data(file)
                            if data is not None:
                                arrays.append(data)
                                
                        arrays = ar(arrays)
                        mean = nmea(arrays, axis=0)
                        return(mean)
                            
                    else:
                        raise Exception('No enough file for average method')
                        
                elif combine_method == "sum":
                    if len(files) > 1:
                        arrays = []
                        for file in files:
                            data = self.data(file)
                            if data is not None:
                                arrays.append(data)
                                
                        arrays = ar(arrays)
                        ssum = nsum(arrays, axis=0)
                        return(ssum)
                            
                    else:
                        raise Exception('No enough file for sum method')
                else:
                    raise Exception('Unknown method')

            except Exception as e:
                self.logger.log(e)
                return(False)
            
        def check(self, file):
            self.logger.log("Check if file({}) is fits".format(file))
            try:
                hdu = fts.open(file, "readonly")
                hdu.close()
                return(True)
            except Exception as e:
                self.logger.log(e)
                return(False)
                
        def header(self, file, field="*"):
            self.logger.log("Getting Header from {}".format(file))
            ret = []
            try:
                hdu = fts.open(file, mode='readonly')
                header = hdu[0].header
                hdu.close()
                for i in header:
                    if not i == "":
                        ret.append([i, header[i]])
                    
                if field == "*":
                    return(ret)
                else:
                    return(header[field])
            except Exception as e:
                self.logger.log(e)
                
        def data(self, file, rot=None):
            self.logger.log("Getting data from {}".format(file))
            try:
                hdu = fts.open(file, mode='readonly')
                data = hdu[0].data
                hdu.close()
                if rot is not None:
                    data = rot90(data, rot)
                
                data = data.astype(float64)
                return(data)
            except Exception as e:
                self.logger.log(e)
                
        def delete_header(self, file, key):
            self.logger.log("Deleting {}'s Header".format(file))
            try:
                hdu = fts.open(file, mode='update')
                del hdu[0].header[key]
                return(hdu.close())
            except Exception as e:
                self.logger.log(e)
                
        def update_header(self, src, key, value):
            self.logger.log("Updating {}'s Header, {}={}".format(src,
                            key, value))
            try:
                hdu = fts.open(src, mode='update')
                hdu[0].header[key] = value
                return(hdu.close())
            except Exception as e:
                self.logger.log(e)
                
        def stats(self, file):
            self.logger.log("Getting Stats from {}".format(file))
            try:
                hdu = fts.open(file)
                image_data = hdu[0].data
                return({'Min': nmin(image_data),
                        'Max': nmax(image_data),
                        'Mean': nmea(image_data),
                        'Stdev': nstd(image_data)})
            except Exception as e:
                self.logger.log(e)
                
        def write(self, dest, data, header=None, ow=True):
            self.logger.log("Writeing data to file({})".format(dest))
            try:
                if ow and self.fop.is_file(dest):
                    self.logger.log("Over Write is Enabled for {}".format(
                            dest))
                fts.writeto(dest, data, header=header, overwrite=ow)
            except Exception as e:
                self.logger.log(e)
                
        def photometry(self, file, x_coor, y_coor, zmag=25.0,
                       aper_radius=15.0, gain=1.21):
            try:
                data = self.data(file)
                bkg = Background(data)
                data_sub = data - bkg
                flx, ferr, flag = sum_circle(data_sub, x_coor, y_coor,
                                             aper_radius, err=bkg.globalrms,
                                             gain=gain)
                mag, merr = self.sma.flux_to_mag(flx, ferr)
                return(str(x_coor), str(y_coor), str(float(flx)),
                       str(float(ferr)), str(float(flag)),
                       str(mag + zmag), str(merr))
            except Exception as e:
                self.logger.log(e)
                
        def mphotometry(self, file, coors, zmag=25.0,
                       apertures=[10.0 ,15.0], gain=1.21):
            try:
                data = self.data(file)
                bkg = Background(data)
                data_sub = data - bkg
                ret = []
                for coor in coors:
                    try:
                        x_coor, y_coor = list(map(int, coor))
                        for aper in apertures:
                            flx, ferr, flag = sum_circle(data_sub, x_coor, y_coor, aper, err=bkg.globalrms, gain=gain)
                            mag, merr = self.sma.flux_to_mag(flx, ferr)
                            ret.append([str(x_coor), str(y_coor), str(aper), str(float(flx)), str(float(ferr)), str(float(flag)), str(mag + zmag), str(merr)])
                    except Exception as e:
                        self.logger.log(e)
                return(ret)
            except Exception as e:
                self.logger.log(e)
        
    class Coordinates:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            
        def phtsical_distence(self, coord1, coord2):
            try:
                return(sqrt(power(coord1[0] - coord2[0], 2) +
                            power(coord1[1] - coord2[1], 2)))
            except Exception as e:
                self.logger.log(e)
                
        def find_closest(self, coordinates, coord):
            try:
                dists = sqrt(power(coordinates[:, 0] - coord[0], 2) +
                             power(coordinates[:, 1] - coord[1], 2))
                if dists is not None:
                    return(argmin(dists))
            except Exception as e:
                self.logger.log(e)
    
    class Query:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            
class Statistics:
    def __init__(self):
        pass
    
    class Math:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
            
        def flux_to_mag(self, flux, fluxerr):
            try:
                mag, magerr = -2.5 * log10(flux), 2.5/log(10.0)*fluxerr/flux
                return(mag, magerr)
            except Exception as e:
                self.logger.log(e)
        
    class Array:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
            self.fop = env.File(verb=self.verb, debugger=self.debugger)
        
        def rotate90(self, array, number=0):
            if not number == 0 or number is not None:
                return(rot90(array, number))
            else:
                return(array)