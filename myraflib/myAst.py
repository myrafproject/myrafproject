# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 19:48:32 2018

@author: mshem
"""
#Importing needed functions
try:
    from astropy import units as U
    from astropy import coordinates
    from astropy.time import Time
    from astropy.wcs import WCS
    from astropy.io import fits as fts
    from astropy.table import Table as TBL
    from astropy.coordinates import SkyCoord
    from astropy.coordinates import EarthLocation
    from astropy.coordinates import AltAz
except Exception as e:
    print("{}. Astropy is not installed?".format(e))
    exit(0)

try:
    from astroquery.vizier import Vizier
except Exception as e:
    print("{}. Astroquery is not installed?".format(e))
    exit(0)

try:
    from scipy.ndimage.interpolation import shift
except Exception as e:
    print("{}. Scipy is not installed?".format(e))
    exit(0)

try:
    import alipy
except Exception as e:
    print("{}. Alipy is not installed?".format(e))
#    exit(0)
    
try:
    from numpy import min as nmin
    from numpy import max as nmax
    from numpy import mean as nmea
    from numpy import median as nmed
    from numpy import std as nstd
    from numpy import log10 as nlog10
    from numpy import asarray
    from numpy import float64 as nf64
    from numpy import sort as nsort
    from numpy import power
    from numpy import argmin
except Exception as e:
    print("{}. Numpy is not installed?".format(e))
    exit(0)
    
from math import pow as mpow
from math import sqrt as msqrt

try:
    from sep import Background
    from sep import sum_circle
    from sep import extract
except Exception as e:
    print("{}. SEP is not installed?".format(e))
    exit(0)

from datetime import datetime
from datetime import timedelta

from glob import glob

try:
    from pyraf import iraf
    from iraf import imred, ccdred
except Exception as e:
    print("{}. Pyraf is not installed?".format(e))
    exit(0)



#Importing myraf's needed modules
try:
    from . import myEnv
except Exception as e:
    print("{}. Cannot find myEnv.py".format(e))
    exit(0)

class fits():
    def __init__(self, verb=True):
        self.verb = verb
        self.etc = myEnv.etc(verb=self.verb)
        self.fop = myEnv.file_op(verb=self.verb)
        
    def is_fit(self, src):
        self.etc.log("Check if {} is a fits file".format(src))
        try:
            ret = False
            if self.fop.is_file(src):
                hdu = fts.open(src, mode='readonly')
                hdu.close()
                ret = True
            
            return(ret)
        except Exception as e:
            self.etc.log(e)
        
    def pure_header(self, src):
        try:
            hdu = fts.open(src, mode='readonly')
            return(hdu[0].header)
        except Exception as e:
            self.etc.log(e)
        
    def get_header(self, src):
        try:
            return(fts.getheader(src))
        except Exception as e:
            self.etc.log(e)
        
    def header(self, src, field="*"):
        self.etc.log("Getting Header from {}".format(src))
        ret = []
        try:
            hdu = fts.open(src, mode='readonly')
            for i in hdu[0].header:
                if not i == "":
                    ret.append([i, hdu[0].header[i]])
                
            if field == "*":
                return(ret)
            else:
                return([field, hdu[0].header[field]])
        except Exception as e:
            self.etc.log(e)
            
    def data(self, src, table=True):
        self.etc.log("Getting Data from {}".format(src))
        try:
            hdu = fts.open(src, mode='readonly')
            data = hdu[0].data
            data = data.byteswap().newbyteorder()
            if table:                
                return(TBL(data))
            else:
                data = data.byteswap().newbyteorder()
                data = data.astype(nf64)
                return(data)
        except Exception as e:
            self.etc.log(e)
            
    def delete_header(self, src, key):
        self.etc.log("Updating {}'s Header".format(src))
        try:
            hdu = fts.open(src, mode='update')
            del hdu[0].header[key]
            return(hdu.close())
        except Exception as e:
            self.etc.log(e)
    
    def update_header(self, src, key, value):
        self.etc.log("Updating {}'s Header, {}={}".format(src, key, value))
        try:
            hdu = fts.open(src, mode='update')
            hdu[0].header[key] = value
            return(hdu.close())
        except Exception as e:
            self.etc.log(e)

    def fits_stat(self, src):
        self.etc.log("Getting Stats from {}".format(src))
        try:
            hdu = fts.open(src)
            image_data = hdu[0].data
            return({'Min': nmin(image_data),
                    'Max': nmax(image_data),
                    'Mean': nmea(image_data),
                    'Stdev': nstd(image_data)})
        except Exception as e:
            self.etc.log(e)
            
    def shift(self, dest, src, x, y):
        self.etc.log("Shifting Image {}".format(src))
        try:
            data = self.data(src, table=False)
            header = self.pure_header(src)
            new_data = self.shift_ar(data, x, y)
            self.write(dest, new_data, header)
        except Exception as e:
            self.etc.log(e)
            
    def shift_ar(self, data, x, y):
        self.etc.log("Shifting array x={}, y={}".format(x, y))
        try:
            return(shift(data, [x, y]))
        except Exception as e:
            self.etc.log(e)
        
    def autolign(self, in_file, ref_file, out_file):
        self.etc.log("Aligning {} using {} as reference".format(in_file, ref_file))

        images_to_align = sorted(glob(in_file))
        ref_image = ref_file
        
        ids = alipy.ident.run(ref_image, images_to_align, visu=False)
        print("============================")
        print(ids)
        outputshape = alipy.align.shape(ref_image)
        for the_id in ids:
            if the_id.ok:
                self.etc.log("{} : {} flux ratio {}".format(
                        the_id.ukn.name, the_id.trans,
                        the_id.medfluxratio))

                alipy.align.affineremap(the_id.ukn.filepath, the_id.trans,
                                        shape=outputshape, outdir=out_file,
                                        makepng=False, verbose=False)
            else:
                self.etc.log("{} : no transformation found !".format(
                        the_id.ukn.name))
                

            
    def write(self, dest, data, header=None, ow=True):
        self.etc.log("Writeing data to file({})".format(dest))
        try:
            if ow and self.fop.is_file(dest):
                self.etc.log("Over Write is Enabled for {}".format(dest))
            fts.writeto(dest, data, header=header, overwrite=ow)
        except Exception as e:
            self.etc.log(e)

class calc():
    def __init__(self, verb=True):
        self.verb = verb
        self.etc = myEnv.etc(verb=self.verb)
        self.fit = fits(verb=self.verb)
        
    def sex2deg(self, deg, hour=False, sep=":"):
        try:
            degree, minute, second = deg.split(sep)
            if degree.startswith("-"):
                ret = float(degree) - float(minute) / 60 - float(second) / 3600
            else:
                ret = float(degree) + float(minute) / 60 + float(second) / 3600
                
            if hour:
                ret = ret / 15
                
            return(ret)
                
        except Exception as e:
            self.etc.log(e)
        
    def get_closest_index(self, xs, ys, searched):
        try:
            x_diff = abs(xs - searched[0])
            y_diff = abs(ys - searched[1])
            
            dists = power(power(x_diff, 2) + power(y_diff, 2), 0.5)
            
            for it, i in enumerate(dists):
                print(it, i)
                
            print(argmin(dists))
            
            return(argmin(dists))
            
        except Exception as e:
            self.etc.log(e)
        
    def distence(self, coor1, coor2):
        try:
            dist = power(power(abs(coor1[0] - coor2[0]), 2
                               ) + power(abs(coor1[1] - coor2[1]), 2), 0.5)
            
            return(dist)
        except Exception as e:
            self.etc.log(e)
        
        
    def airmass(self, ra, dec, lat, lon, alt, time, utc_offset):
        self.etc.log("Calculating airmass for ra({}), dec({}), lat({}), log({}), alt({}), time({}), utc offset({})".format(ra, dec, lat, lon, alt, time, utc_offset))
        try:
            object_wcs = SkyCoord(ra * U.deg, dec * U.deg, frame='icrs')
            observatory = EarthLocation(lat=lat*U.deg,
                                        lon=lon*U.deg, height=alt*U.m)
            utcoffset = utc_offset * U.hour
            utc = Time(time) - utcoffset
            date_loc = AltAz(obstime=utc, location=observatory)
            object_date_loc = object_wcs.transform_to(date_loc)
            return(object_date_loc.secz)
        except Exception as e:
            self.etc.log(e)
        
    def flux2magmerr(self, flux, fluxerr):
        self.etc.log("Calculating Mag and Merr")
        try:
            mag = -2.5 * nlog10(flux)
            magerr = 2.5 / nlog10(10.0) * fluxerr / flux
            return(mag, magerr)
        except Exception as e:
            self.etc.log(e)
            
    def radec2wcs(self, ra, dec):
        self.etc.log("Converting coordinates to WCS")
        try:
            c = SkyCoord('{0} {1}'.format(ra, dec), unit=(U.hourangle, U.deg),
                         frame='icrs')
            return(c)
        except Exception as e:
            self.etc.log(e)
            
    def xy2sky(self, file_name, x, y):
        self.etc.log("Converting physical coordinates to WCS")
        try:
            header = fts.getheader(file_name)
            w = WCS(header)
            astcoords_deg = w.wcs_pix2world([[x, y]], 0)
            c = coordinates.SkyCoord(astcoords_deg * U.deg, frame='icrs')
            #the_coo = c.to_string(style='hmsdms', sep=sep, precision=4)[0]
            return(c.ra.deg[0], c.dec.deg[0])
        except Exception as e:
            self.etc.log(e)
            
    def is_close_arc(self, coor1, coor2, max_dist=10):
        self.etc.log("Calculating proximity(WCS)")
        try:
            c1 = self.radec2wcs(coor1[0], coor1[1])
            c2 = self.radec2wcs(coor2[0], coor2[1])
            
            ret = c1.separation(c2)
            return(ret.arcsecond < max_dist)
        except Exception as e:
            self.etc.log(e)

    def is_close_phy(self, coor1, coor2, max_dist=15):
        self.etc.log("Calculating proximity(PHY)")
        try:
            dX = coor1[0] - coor2[0]
            dY = coor1[1] - coor2[1]
            dist = msqrt(mpow(dX, 2) + mpow(dY, 2))
            return(dist < max_dist)
        except Exception as e:
            self.etc.log(e)
        
    def jd(self, timestamp):
        self.etc.log("Calculating JD from timestamp({})".format(timestamp))
        try:
            if "T" not in timestamp:
                timestamp = str(timestamp).replace(" ", "T")
            
            t_jd = Time(timestamp, format='isot', scale='utc')
    
            return(t_jd.jd)
        except Exception as e:
            self.etc.log(e)
        
    def mjd(self, timestamp):
        self.etc.log("Calculating MJD from timestamp({})".format(timestamp))
        try:
            if "T" not in timestamp:
                timestamp = str(timestamp).replace(" ", "T")
            
            t_jd = Time(timestamp, format='isot', scale='utc')
    
            return(t_jd.mjd)
        except Exception as e:
            self.etc.log(e)
            
    def imexamine(self, src):
        try:
            data = self.fit.data(src, table=False)
            the_min = nmin(data)
            the_max = nmax(data)
            the_mea = nmea(data)
            the_std = nstd(data)
            the_med = nmed(data)
            return([the_mea, the_med, the_std, the_min, the_max])
        except Exception as e:
            self.etc.log(e)
            
        
class phot():
    def __init__(self, verb=True):
        self.verb = verb
        self.etc = myEnv.etc(verb=self.verb)
        self.fop = myEnv.file_op(verb=self.verb)
        self.calc = calc(verb=self.verb)
        
    def do(self, data, x_coor, y_coor, aper_radius=10.0, gain=1.21):
        self.etc.log("Starting Photometry for x({}), y({}) with aperture({}) and gain({})".format(x_coor, y_coor, aper_radius, gain))
        try:
            bkg = Background(data)
            data_sub = data - bkg
            flux, fluxerr, flag = sum_circle(data_sub, x_coor, y_coor,
                                             aper_radius, err=bkg.globalrms,
                                             gain=gain)
            return(flux, fluxerr, flag)
        except Exception as e:
            self.eetc.log(e)
        
    def do_mag(self, data, x_coor, y_coor, aper_radius=10.0, gain=1.21):
        self.etc.log("Starting (MAG) Photometry")
        try:
            flux, fluxerr, flag = self.do(data, x_coor,
                                          y_coor, aper_radius=10.0, gain=1.21)
            return(calc.flux2magmerr(self, flux, fluxerr))
        except Exception as e:
            self.etc.log(e)
            
class time():
    def __init__(self, verb=True):
        self.verb = verb
        self.etc = myEnv.etc(verb=self.verb)
        self.fop = myEnv.file_op(verb=self.verb)
        self.calc = calc(verb=self.verb)
        
    def time_stamp(self, utc=False):
        try:
            if utc:
                return(str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")))
            else:
                return(str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))
        except Exception as e:
            self.eetc.log(e)
            
    def time_offset(self, time, offset, diff_type="seconds"):
        self.etc.log("Time offset calculation for {} with {} {}".format(
                time, offset, diff_type))
        the_time = None
        try:
            the_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            self.etc.log("{}: 2dn Try".format(e))
            try:
                the_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                self.etc.log(e)
        try:
            ret = None
            if the_time is not None:
                if diff_type == "seconds":
                    ret = the_time + timedelta(seconds=offset)
                elif diff_type == "minutes":
                    ret = the_time + timedelta(minutes=offset)
                elif diff_type == "hours":
                    ret = the_time + timedelta(hours=offset)
                    
            return(ret)
        except Exception as e:
            self.etc.log(e)
        
        
    
    def jd(self, utc=False):
        try:
            return(self.calc.jd(self.time_stamp(utc=utc)))
        except Exception as e:
            self.eetc.log(e)
        
    def mjd(self, utc=False):
        try:
            return(self.calc.mjd(self.time_stamp(utc=utc)))
        except Exception as e:
            self.eetc.log(e)
        
class sextractor():
    def __init__(self, verb=True):
        self.verb = verb
        self.etc = myEnv.etc(verb=self.verb)
        
    def find(self, data, threshold=1.5, table=True, only_best=True):
        try:
            bkg = Background(data)
            data_sub = data - bkg
            all_objects = asarray(extract(data_sub, threshold,
                                          err=bkg.globalrms))
            if only_best:
                all_objects = all_objects[all_objects['flag'] == 0]
                
            if table:            
                return(TBL(all_objects))
            else:
                return(all_objects)
        except Exception as e:
            self.etc.log(e)
            
    def find_limited(self, data, threshold=1.5, table=True,
                     only_best=True, max_sources=200):
        try:
            bkg = Background(data)
            data_sub = data - bkg
            all_objects = asarray(extract(data_sub, threshold,
                                          err=bkg.globalrms))
            if only_best:
                all_objects = all_objects[all_objects['flag'] == 0]
            
            ord_objects = nsort(all_objects, order=['flux'])
            
            if len(ord_objects) <= max_sources:
                max_sources = len(ord_objects)
                objects = ord_objects[::-1][:max_sources]
            if len(ord_objects) > max_sources:
                objects = ord_objects[::-1][:max_sources]
            elif not max_sources:
                objects = ord_objects[::-1]
                
            if table:            
                return(TBL(objects))
            else:
                return(objects)
        except Exception as e:
            self.etc.log(e)
            
    def extract_xy(self, src):
        try:
            return(TBL([src['x'], src['y']]))
        except Exception as e:
            self.etc.log(e)
              
class cat():
    def __init__(self, verb=True):
        self.verb = verb
        self.etc = myEnv.etc(verb=self.verb)
        
    def gaia(self, ra, dec, radius=0.0027, max_sources=1):
        self.etc.log("Getting data from Gaia for ra({}), dec({}) and radius({})".format(ra, dec, radius))
        try:
            field = coordinates.SkyCoord(ra=ra,dec=dec, unit=(U.deg, U.deg),
                                         frame='icrs')
            
            vquery = Vizier(columns=['Source', 'RA_ICRS', 'DE_ICRS',
                                     'e_RA_ICRS','e_DE_ICRS',
                                     'phot_g_mean_mag', 'pmRA', 'pmDE',
                                     'e_pmRA', 'e_pmDE', 'Epoch', 'Plx'],
                row_limit=max_sources)
            
            return(vquery.query_region(field, width="{:f}d".format(radius),
                                       catalog="I/337/gaia")[0])
        except Exception as e:
            self.etc.log(e)
            
    def nomad(self, ra, dec, radius=0.0027, max_sources=1):
        self.etc.log("Getting data from Nomad for ra({}), dec({}) and radius({})".format(ra, dec, radius))
        try:
            c = coordinates.SkyCoord(ra, dec, unit=(U.deg, U.deg),
                                     frame='icrs')
            r = radius * U.deg

            vquery = Vizier(columns=['NOMAD1', 'RAJ2000', 'DEJ2000', 'Bmag',
                                     'Vmag', 'Rmag'], row_limit=max_sources)

            result = vquery.query_region(c, radius=r, catalog="NOMAD")[0]

            return(result)
        except Exception as e:
            self.etc.log(e)
            
    def usno(self, ra, dec, radius=0.0027, max_sources=1):
        self.etc.log("Getting data from Usno for ra({}), dec({}) and radius({})".format(ra, dec, radius))
        try:
            c = coordinates.SkyCoord(ra, dec,
                                           unit=(U.deg, U.deg),
                                           frame='icrs')
            r = radius * U.deg

            vquery = Vizier(columns=['USNO', 'RAJ2000', 'DEJ2000', 'Bmag',
                                     'Rmag'], row_limit=max_sources)

            result = vquery.query_region(c, radius=r, catalog="USNO-A2.0")[0]

            return(result)
        except Exception as e:
            self.etc.log(e)
            
class calibration():
    def __init__(self, verb=True):
        self.verb = verb
        self.fit = fits(verb=self.verb)
        self.etc = myEnv.etc(verb=self.verb)
        self.fop = myEnv.file_op(verb=self.verb)
        
    def the_zerocombine(self, in_file_list, out_file, method="median", rejection="minmax", ccdtype="",
                        gain="", rdnoise=""):

        self.etc.log("Zerocombine started for {} files using combine({}) and rejection({})".format(len(in_file_list), method, rejection))

        try:
            if self.fop.is_file(out_file):
                self.fop.rm(out_file)
                
            files = []
            for file in in_file_list:
                if self.fit.is_fit(file):
                    files.append(file)
            
            if not len(files) == 0:
                biases = ",".join(files)
                # Load packages
                # Unlearn settings
                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.zerocombine.unlearn()

                ccdred.instrument = "ccddb$kpno/camera.dat"
                iraf.imred()
                iraf.ccdred()

                iraf.zerocombine(input=biases,
                                 output=out_file,
                                 combine=method,
                                 reject=rejection,
                                 ccdtype=ccdtype,
                                 Stdout="/dev/null")
            else:
                self.etc.log("No files to combine")
            
        except Exception as e:
            self.etc.log(e)
            
    def the_darkcombine(self, in_file_list, out_file, zero=None,
                        method="median", rejection="minmax",
                        ccdtype="", scale="exposure", overscan = "no", trim="no"):
        self.etc.log("Darkcombine started for {} files using combine({}), rejection({}) and scale({}) and zero({})".format(len(in_file_list), method, rejection, scale, zero))
        try:
            if self.fop.is_file(out_file):
                self.fop.rm(out_file)

            files = []
            for file in in_file_list:
                if self.fit.is_fit(file):
                    files.append(file)

            if not len(files) == 0:
                darks = ",".join(files)
                # Load packages
                # Unlearn settings
                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.darkcombine.unlearn()

                ccdred.instrument = "ccddb$kpno/camera.dat"
                iraf.imred()
                iraf.ccdred()

                iraf.darkcombine(input=darks,
                                 output=out_file,
                                 combine=method,
                                 reject=rejection,
                                 ccdtype=ccdtype,
                                 scale=scale,
                                 process="no",
                                 Stdout="/dev/null")

                if zero is not None and self.fop.is_file(zero):
                    iraf.ccdproc(images=darks, ccdtype='', fixpix='no', oversca=overscan, trim=trim, zerocor='yes',
                                 darkcor='no', flatcor='no', zero=zero, Stdout="/dev/null")

            else:
                self.etc.log("No files to combine")
        except Exception as e:
            self.etc.log(e)

    def the_flatcombine(self, in_file_list, out_file, dark=None, zero=None, ccdtype="",
                        method="Median", rejection="minmax", subset="yes", overscan = "no", trim="no"):
        self.etc.log("Flatcombine started for {} files using combine({}), rejection({}) and subset=({}) and zero({}) and dark({})".format(len(in_file_list), method, rejection, subset, zero, dark))
        try:
            if self.fop.is_file("{}*".format(out_file)):
                self.fop.rm("{}*".format(out_file))
                
            files = []
            for file in in_file_list:
                if self.fit.is_fit(file):
                    files.append(file)
            
            if not len(files) == 0:
                flats = ",".join(files)
                # Load packages
                # Unlearn settings
                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.flatcombine.unlearn()

                ccdred.instrument = "ccddb$kpno/camera.dat"
                iraf.imred()
                iraf.ccdred()

                iraf.flatcombine(input=flats,
                                 output=out_file,
                                 combine=method,
                                 reject=rejection,
                                 ccdtype=ccdtype,
                                 subset=subset,
                                 process="no",
                                 Stdout="/dev/null")

                if dark is not None or zero is not None:
                    if zero is not None and self.fop.is_file(zero):
                        zerocor='yes'
                    else:
                        zerocor = 'no'

                    if dark is not None and self.fop.is_file(dark):
                        darkcor = 'yes'
                    else:
                        darkcor = 'no'

                    iraf.ccdproc(images=flats, ccdtype='', fixpix='no',
                                 oversca=overscan, trim=trim, zerocor=zerocor,
                                 darkcor=darkcor, flatcor='no', zero=zero, dark=dark,
                                 Stdout="/dev/null")
            self.etc.log("flatcombine is done!")
            
        except Exception as e:
            self.etc.log(e)
            
        
    def the_calibration(self, in_file, out_file, zero=None, dark=None,
                        flat=None, subset="yes"):
        self.etc.log("Calibration started for {} with zero({}), dark({}) and flat({}) and subset({})".format(in_file, zero, dark, flat, subset))
        try:
            cp = ccdproc
            cp.images = in_file
            
            cp.output = out_file
            cp.ccdtype = ""
            cp.fixpix = "no"
            cp.overscan = "no"
            cp.trim = "no"
            cp.zerocor = "no"
            cp.darkcor = "no"
            cp.flatcor = "no"
            
            if zero is not None:
                cp.zerocor = "yes"
                cp.zero = zero
                
            if dark is not None:
                cp.darkcor = "yes"
                cp.dark = dark
                
            if flat is not None:
                cp.flatcor = "yes"
                cp.flat = flat
                
            if subset == "no" and flat is not None:
                tmp_subset = self.fit.header(in_file, "SUBSET")
                if tmp_subset is not None:
                    self.fit.update_header(in_file, "MYSEUBS", tmp_subset)
                self.fit.delete_header(in_file, "SUBSET")
            
            cp(images = str(in_file))
            
            if subset == "no" and flat is not None:
                tmp_subset = self.fit.header(in_file, "MYSEUBS")
                if tmp_subset is not None:
                    self.fit.update_header(in_file, "SUBSET", tmp_subset)
                self.fit.delete_header(in_file, "MYSEUBS")
                
            
        except Exception as e:
            self.etc.log(e)
