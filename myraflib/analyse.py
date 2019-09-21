# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:35:56 2019

@author: msh, yk
"""

try:
    from subprocess import PIPE
except Exception as e:
    print("{}: Can't import subprocess".format(e))
    exit(0)

try:
    from sep import Background
    from sep import sum_circle
except Exception as e:
    print("{}: Can't import sep".format(e))
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
    from numpy import float64 as f64
    from numpy import power
    from numpy import sqrt
    from numpy import argmin
except Exception as e:
    print("{}: Can't import numpy.".format(e))
    exit(0)
    
try:
    from datetime import datetime
    from datetime import timedelta
except Exception as e:
    print("{}: Can't import datetime?".format(e))
    exit(0)
    
try:
    from astropy.io import fits as fts
    from astropy.time import Time as tm
    from astropy.coordinates import EarthLocation
    from astropy.coordinates import SkyCoord
    from astropy.coordinates import AltAz
    import astropy.units as U
    from astropy.table import Table
    from astropy.nddata import NDData
except Exception as e:
    print("{}: Can't import astropy.".format(e))
    exit(0)
    
try:
    from photutils import EPSFBuilder
    from photutils.psf import extract_stars
except Exception as e:
    print("{}: Can't import photutils.".format(e))
    exit(0)

try:
    from pyraf import iraf
    from iraf import imred
    from iraf import ccdred
    from iraf import digiphot
    from iraf import daophot
    from iraf import ptools
except Exception as e:
    print("{}: Can't import pyraf/iraf.".format(e))
    exit(0)

try:
    import alipy
    from alipy import imgcat
except Exception as e:
    print("{}: Can't import alipy.".format(e))
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
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
        
        def str_to_time(self, date):
            if date is not None:
                try:
                    if "T" in date:
                        frmt = '%Y-%m-%dT%H:%M:%S'
                    elif " " in date:
                        frmt = '%Y-%m-%d %H:%M:%S'
                    else:
                        self.logger.log("Unknown date format")
                        frmt = None
                        
                    if frmt is not None:
                        datetime_object = datetime.strptime(date, frmt)
                        return(datetime_object)
                        
                except Exception as e:
                    self.logger.log(e)
        
        def time_diff(self, time, time_offset=-3, offset_type="hours"):
            if time is not None and time_offset is not None:
                try:
                    if "HOURS".startswith(offset_type.upper()):
                        return(time + timedelta(hours=time_offset))
                    elif "MINUTES".startswith(offset_type.upper()):
                        return(time + timedelta(minutes=time_offset))
                    elif "SECONDS".startswith(offset_type.upper()):
                        return(time + timedelta(seconds=time_offset))
                        
                except Exception as e:
                    self.logger.log(e)
            else:
                self.logger.log("False Type: One of the values is not correct")
        
        def jd(self, utc):
            if utc is not None:
                try:
                    ret = tm(utc, scale='utc')
                    return(ret.jd)
                except Exception as e:
                    self.logger.log(e)
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
                
        def phot(self, file, output, coords, apertures, annulus=5, dannulus=5, zmag=25):
            try:
                coord_file = "{}/myraf_coord.coo".format(self.logger.tmp_dir)
                with open(coord_file, "w") as f:
                    for coord in coords:
                        f.write("{} {}\n".format(coord[0], coord[1]))
                        
                apertures = list(map(str, apertures))
                
                iraf.photpars.weighting = "constant"
                iraf.photpars.aperture = ",".join(apertures)
                iraf.photpars.zmag = zmag
                iraf.photpars.mkapert = "no"
                
                iraf.daophot.phot.interactive = "no"
                iraf.daophot.phot.verify = "no"
                iraf.daophot.phot.verbose = "no"
                
                iraf.fitskypars.salgo = "centroid"
                iraf.fitskypars.annu = annulus
                iraf.fitskypars.dannu = dannulus
                iraf.fitskypars.skyval = 0
                iraf.fitskypars.smaxi = 10
                iraf.fitskypars.sloc = 0
                iraf.fitskypars.shic = 0
                iraf.fitskypars.snrej = 50
                iraf.fitskypars.slorej = 3.
                iraf.fitskypars.shirej = 3.
                iraf.fitskypars.khist = 3
                iraf.fitskypars.binsi = 0.1
                
                if self.fop.is_file(output):
                    self.fop.rm(output)
                    
                iraf.phot.coords = coord_file
                iraf.phot.output = output
                iraf.daophot.phot.verify = "no"
                iraf.daophot.phot.interactive = "no"
                iraf.daophot.phot.radplots = "no"
                
                iraf.daophot.phot(file, output=output, coords=coord_file, verbose="no", verify="no", interactive="no")
                return True
            except Exception as e:
                self.logger.log(e)
                return False

        def textdump(self, file, fields=["id", "mag", "merr"]):
            try:
                ret = []
                txdump = iraf.txdump
                the_fields = ",".join(fields)
                res = txdump(file, the_fields, "yes", Stdout=PIPE)
                for r in res:
                    ret.append(r.split())
                    
                return ret
            except Exception as e:
                self.logger.log(e)
            
    class Fits:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
            self.fop = env.File(verb=self.verb, debugger=self.debugger)
            self.sma = Statistics.Math(verb=self.verb, debugger=self.debugger)
            
        def astrometry(self, file, out_file,
                       server="http://nova.astrometry.net/api/",
                       apikey="abhfixfhhxsignyo"):
            try:
                command = ["python3", "myraf_astrometry.py",
                           "--apikey={}".format(apikey),
                           "--server={}".format(server),
                           "--upload={}".format(file),
                           "--newfits={}".format(out_file)]
                
                for output in self.logger.execute(command):
                    self.logger.log(output.strip())
                    
            except Exception as e:
                self.logger.log(e)
                
        def solve_field(self, file, out_file):
            try:
                
                command = ["solve-field", "--temp-axy",
                           "--no-plots", "--overwrite", "--dir={}".format(
                                   self.logger.tmp_dir),
                           "--new-fits={}".format(out_file)]
                
                if self.debugger:
                    command.append("-v")
                    
                command.append(file)
                
                for output in self.logger.execute(command):
                    self.logger.log(output.strip())
                
            except Exception as e:
                self.loggrt.log(e)
                
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
                
                data = data.astype(f64)
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
                
        def mupdate_header(self, src, key_values):
            self.logger.log("Updating multiple headers in {}".format(src))
            try:
                hdu = fts.open(src, mode='update')
                for key_val in key_values:
                    hdu[0].header[key_val[0]] = key_val[1]
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
                        'Median': nmed(image_data),
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
                            flx, ferr, flag = sum_circle(data_sub, x_coor,
                                                         y_coor, aper,
                                                         err=bkg.globalrms,
                                                         gain=gain)
                            
                            mag, merr = self.sma.flux_to_mag(flx, ferr)
                            ret.append([str(x_coor), str(y_coor), str(aper),
                                        str(float(flx)), str(float(ferr)),
                                        str(float(flag)), str(mag + zmag),
                                        str(merr)])
                    except Exception as e:
                        self.logger.log(e)
                return(ret)
            except Exception as e:
                self.logger.log(e)
                
        def psf(self, image):
            data = self.data(image)
            bkg = Background(data)
            pure_data = data - bkg
            nddata = NDData(data=pure_data)
            sources = self.star_finder(image)
            stars_tbl = Table()
            size = nmea(sources[:, 2])
            for source in sources:
                stars_tbl['x'] = source[0]
                stars_tbl['y'] = source[1]
                
            stars = extract_stars(nddata, stars_tbl, size=size*10)
            epsf_builder = EPSFBuilder(oversampling=4, maxiters=3, progress_bar=self.verb)
            epsf, fitted_stars = epsf_builder(stars)
            print(epsf)
        
    class Coordinates:
        def __init__(self, verb=False, debugger=False):
            self.verb = verb
            self.debugger = debugger
            self.logger = env.Logger(verb=self.verb, debugger=self.debugger)
            
        def create_site(self, lati, long, alti):
            try:
                site = EarthLocation(lat=float(lati)*U.deg,
                                     lon=float(long)*U.deg,
                                     height=float(alti)*U.m)
                return(site)
            except Exception as e:
                self.logger.log(e)
                
        def create_object(self, ra, dec):
            try:
                return(SkyCoord(ra=ra*U.hour, dec=dec*U.deg))
            except Exception as e:
                self.logger.log(e)
                
        def radec_to_alt_az(self, site, obj, utc):
            try:
                frame_of_sire = AltAz(obstime=utc, location=site)
                object_alt_az = obj.transform_to(frame_of_sire)
                return(object_alt_az)
            except Exception as e:
                self.logger.log(e)
                
        def airmass(self, object_altaz):
            try:
                return(object_altaz.secz)
            except Exception as e:
                self.logger.log(e)
                
        def convert_sex_to_deg(self, angle):
            try:
                an = angle.split(":")
                if angle.startswith("-"):
                    return(float(an[0]) - float(an[1])/60 - float(an[2])/3600)
                else:
                    return(float(an[0]) + float(an[1])/60 + float(an[2])/3600)
            except Exception as e:
                self.logger.log(e)
            
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
                
        def mean(self, array):
            numpy_array = ar(array)
            return(nmea(numpy_array))