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
    from ccdproc import cosmicray_lacosmic as cosla
except Exception as e:
    print("{}: Can't import ccdproc".format(e))
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


class Astronomy:
    def __init__(self):
        pass
    
    class Time:
        def __init__(self, logger):
            self.logger = logger
        
        def str_to_time(self, date):
            """Returns a date object from a string"""
            if date is not None:
                try:
                    if "T" in date:
                        frmt = '%Y-%m-%dT%H:%M:%S'
                    elif " " in date:
                        frmt = '%Y-%m-%d %H:%M:%S'
                    else:
                        self.logger.info("Unknown date format")
                        frmt = None
                        
                    if frmt is not None:
                        datetime_object = datetime.strptime(date, frmt)
                        return datetime_object
                        
                except Exception as e:
                    self.logger.error(e)
        
        def time_diff(self, time, time_offset=-3, offset_type="hours"):
            """Time Calculator"""
            if time is not None and time_offset is not None:
                try:
                    if "HOURS".startswith(offset_type.upper()):
                        return time + timedelta(hours=time_offset)
                    elif "MINUTES".startswith(offset_type.upper()):
                        return time + timedelta(minutes=time_offset)
                    elif "SECONDS".startswith(offset_type.upper()):
                        return time + timedelta(seconds=time_offset)
                        
                except Exception as e:
                    self.logger.error(e)
            else:
                self.logger.warning("False Type: One of the values is not correct")
        
        def jd(self, utc):
            """Calculates JD from UTC"""
            if utc is not None:
                try:
                    ret = tm(utc, scale='utc')
                    return ret.jd
                except Exception as e:
                    self.logger.error(e)
            else:
                self.logger.warning("False Type: The value is not date")
                
        def jd_r(self, jd):
            """Returns UTC from JD"""
            try:
                t = tm(jd, format='jd', scale='tai')
                return t.to_datetime()
            except Exception as e:
                self.logger.error(e)
            
    class Fits:
        def __init__(self, logger):
            self.logger = logger

        def cosmic_cleaner(self, file, output, sigclip=12, sigfrac=0.3,
                           objlim=5.0, gain=1.0, readnoise=6.5,
                           satlevel=65535.0, pssl=0.0, iteration=4,
                           sepmed=True, cleantype='meanmask', fsmode='median',
                           psfmodel='gauss', psffwhm=2.5, psfsize=7, psfk=None,
                           psfbeta=4.765, verbose=False):
            """Cleaning cosmic rays from given file"""
            try:
                data = self.data(file)
                
                new_data, cos = cosla(data, sigclip=sigclip, sigfrac=sigfrac,
                                      objlim=objlim, gain=gain,
                                      readnoise=readnoise, satlevel=satlevel,
                                      pssl=pssl, niter=iteration,
                                      sepmed=sepmed, cleantype=cleantype,
                                      fsmode=fsmode, psfmodel=psfmodel,
                                      psffwhm=psffwhm, psfsize=psfsize,
                                      psfk=psfk, psfbeta=psfbeta,
                                      verbose=verbose)
                self.write(output, new_data, header=self.header(file,
                                                                field="?"))
            except Exception as e:
                self.logger.error(e)
            
        def align(self, image, ref, output):
            """Aligning an image with respect of given referance"""
            identifications = alipy.ident.run(ref, [image], visu=False,
                                              sexkeepcat=False, verbose=False)
            outputshape = alipy.align.shape(ref)
            for the_id in identifications:
                if the_id.ok == True:
                    the_id.ukn.name, the_id.trans, the_id.medfluxratio
                    alipy.align.affineremap(the_id.ukn.filepath, the_id.trans,
                                            shape=outputshape, outdir=output)
                
        def star_finder(self, image, max_star=500):
            """returns x, y and fwhm of objects on a given fits image"""
            self.logger.info("Star finder started for {}".format(image))
            try:
                img = imgcat.ImgCat(image)
                img.makecat(rerun=True, keepcat=False, verbose=False)
                img.makestarlist(skipsaturated=False, n=max_star,
                                 verbose=False)
                ret = []
                for star in img.starlist:
                    ret.append([star.x, star.y, star.fwhm])
                    
                return ar(ret)
            except Exception as e:
                self.logger.error(e)
                
        def subtract(self, img1, img2):
            """Subtacts two image array"""
            self.logger.info("Subtraction for {} - {}".format(img1, img2))
            try:
                data1 = self.data(img1)
                data2 = self.data(img2)
                if data1 is not None and data2 is not None:
                    return data1 - data2
            except Exception as e:
                self.logger.error(e)
            
        def combine(self, files, combine_method):
            """Combines (median, average, sum) given files"""
            self.logger.info("Combine for {} files with {} methdo".format(
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
                        return medi
                            
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
                        return mean
                            
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
                        return ssum
                            
                    else:
                        raise Exception('No enough file for sum method')
                else:
                    raise Exception('Unknown method')

            except Exception as e:
                self.logger.error(e)
                return False
            
        def check(self, file):
            """Checks if file is fit"""
            self.logger.info("Check if file({}) is fits".format(file))
            try:
                hdu = fts.open(file, "readonly")
                hdu.close()
                return True
            except Exception as e:
                self.logger.error(e)
                return False
                
        def header(self, file, field="*"):
            """Returns header(s) from file"""
            self.logger.info("Getting Header from {}".format(file))
            ret = []
            try:
                hdu = fts.open(file, mode='readonly')
                header = hdu[0].header
                hdu.close()
                for i in header:
                    if not i == "":
                        ret.append([i, header[i]])
                    
                if field == "*":
                    return ret
                elif field == "?":
                    return header
                else:
                    return header[field]
            except Exception as e:
                self.logger.error(e)
                
        def data(self, file, rot=None):
            """Return data from a given fits file"""
            self.logger.info("Getting data from {}".format(file))
            try:
                hdu = fts.open(file, mode='readonly')
                data = hdu[0].data
                hdu.close()
                if rot is not None:
                    data = rot90(data, rot)
                
                data = data.astype(f64)
                return data
            except Exception as e:
                self.logger.error(e)
                
        def delete_header(self, file, key):
            """Removes a key from header"""
            self.logger.info("Deleting {}'s Header".format(file))
            try:
                hdu = fts.open(file, mode='update')
                del hdu[0].header[key]
                return hdu.close()
            except Exception as e:
                self.logger.error(e)
                
        def update_header(self, src, key, value):
            """Adds/Updates a header to a given fits file"""
            self.logger.info("Updating {}'s Header, {}={}".format(src,
                            key, value))
            try:
                hdu = fts.open(src, mode='update')
                hdu[0].header[key] = value
                return hdu.close()
            except Exception as e:
                self.logger.error(e)
                
        def mupdate_header(self, src, key_values):
            """Adds/Updates a header to multiple fits files"""
            self.logger.info("Updating multiple headers in {}".format(src))
            try:
                hdu = fts.open(src, mode='update')
                for key_val in key_values:
                    hdu[0].header[key_val[0]] = key_val[1]
                return hdu.close()
            except Exception as e:
                self.logger.error(e)
                
        def stats(self, file):
            """Returns statistics of a given fit file."""
            self.logger.info("Getting Stats from {}".format(file))
            try:
                hdu = fts.open(file)
                image_data = hdu[0].data
                return {'Min': nmin(image_data),
                        'Max': nmax(image_data),
                        'Median': nmed(image_data),
                        'Mean': nmea(image_data),
                        'Stdev': nstd(image_data)}
            except Exception as e:
                self.logger.error(e)
                
        def write(self, dest, data, header=None, ow=True):
            """Writes data to a fits file"""
            self.logger.info("Writeing data to file({})".format(dest))
            try:
                fts.writeto(dest, data, header=header, overwrite=ow)
            except Exception as e:
                self.logger.error(e)
                
        def photometry(self, file, x_coor, y_coor, zmag=25.0,
                       aper_radius=15.0, gain=1.21):
            """Python photometry"""
            try:
                data = self.data(file)
                bkg = Background(data)
                data_sub = data - bkg
                flx, ferr, flag = sum_circle(data_sub, x_coor, y_coor,
                                             aper_radius, err=bkg.globalrms,
                                             gain=gain)
                mag, merr = self.sma.flux_to_mag(flx, ferr)
                return [str(x_coor), str(y_coor), str(float(flx)),
                        str(float(ferr)), str(float(flag)),
                        str(mag + zmag), str(merr)]
            except Exception as e:
                self.logger.error(e)
                
        def mphotometry(self, file, coors, zmag=25.0,
                       apertures=[10.0 ,15.0], gain=1.21):
            """Python multiple photometry"""
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
                        self.logger.error(e)
                return ret
            except Exception as e:
                self.logger.error(e)
                
        def psf(self, image):
            """PSF photometry"""
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
            epsf_builder = EPSFBuilder(oversampling=4, maxiters=3,
                                       progress_bar=False)
            epsf, fitted_stars = epsf_builder(stars)
            print(epsf)
