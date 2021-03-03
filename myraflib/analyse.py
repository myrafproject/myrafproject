# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:35:56 2019

@author: msh, yk
"""

import os

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
    from astropy.coordinates import AltAz, Angle
    from astropy import units
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
    import astroalign as aa
except Exception as e:
    print("{}: Can't import astroalign.".format(e))
    exit(0)

try:
    import alipy
except Exception as e:
    print("{}: Can't import alipy.".format(e))
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

from . import env


class Astronomy:
    def __init__(self):
        pass

    class Iraf:
        def __init__(self, logger):
            self.logger = logger
            self.fts = Astronomy.Fits(self.logger)
            self.fop = env.File(self.logger)
            self.instrument_path = ""

        def imshift(self, file, output, dx, dy, overwrite=True):
            """Shifts a given fits file with given dx and dy"""
            try:
                iraf.imshift.unlearn()
                if self.fop.is_file(output) and overwrite:
                    self.logger.warning("Over Writing file({})".format(output))
                    self.fop.rm(output)
                iraf.imshift(input=file, output=output, x=dx, y=dy)
                return True
            except Exception as e:
                self.logger.error(e)
                return False

        def zerocombine(self, files, output, method="median", rejection="minmax", ccdtype="", overwrite=True):
            """IRAF zerocombine"""
            self.logger.info("Zerocombine Started")
            try:
                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.zerocombine.unlearn()
                iraf.ccdred.zerocombine.unlearn()
                ccdred.instrument = self.instrument_path

                biases = ",".join(files)

                out_file = "{}/myraf_biases.flist".format(self.fop.tmp_dir)
                with open(out_file, "w") as f2w:
                    for i in files:
                        f2w.write("{}\n".format(i))

                biases = "@{}".format(out_file)

                if self.fop.is_file(output) and overwrite:
                    self.logger.warning("Over Writing file({})".format(output))
                    self.fop.rm(output)

                iraf.zerocombine(input=biases, output=output, combine=method,
                                 reject=rejection, ccdtype=ccdtype,
                                 Stdout="/dev/null")
                return True
            except Exception as e:
                self.logger.error(e)
                return False

        def darkcombine(self, files, output, zero=None, method="median",
                        rejection="minmax", ccdtype="", scale="exposure", overwrite=True):
            """IRAF darkcombine"""
            self.logger.info("Darkcombine Started")
            try:
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.darkcombine.unlearn()
                iraf.imred.unlearn()

                ccdred.instrument = self.instrument_path

                darks = ",".join(files)

                out_file = "{}/myraf_darks.flist".format(self.fop.tmp_dir)
                with open(out_file, "w") as f2w:
                    for i in files:
                        f2w.write("{}\n".format(i))

                darks = "@{}".format(out_file)

                if zero is not None:
                    iraf.ccdproc(images=darks, ccdtype='', fixpix='no',
                                 oversca="no", trim="no", zerocor='yes',
                                 darkcor='no', flatcor='no', zero=zero,
                                 Stdout="/dev/null")

                if self.fop.is_file(output) and overwrite:
                    self.logger.warning("Over Writing file({})".format(output))
                    self.fop.rm(output)

                iraf.darkcombine(input=darks, output=output, combine=method,
                                 reject=rejection, ccdtype=ccdtype,
                                 scale=scale, process="no", Stdout="/dev/null")

                return True
            except Exception as e:
                self.logger.error(e)
                return False

        def flatcombine(self, files, output, dark=None, zero=None, ccdtype="",
                        method="Median", rejection="minmax", subset="no", overwrite=True):
            """IRAF flatcombine"""
            self.logger.info("Flatcombine Started")
            try:
                flats = ",".join(files)

                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()
                iraf.ccdred.combine.unlearn()
                iraf.ccdred.flatcombine.unlearn()

                ccdred.instrument = self.instrument_path

                out_file = "{}/myraf_flats.flist".format(self.fop.tmp_dir)
                with open(out_file, "w") as f2w:
                    for i in files:
                        f2w.write("{}\n".format(i))

                flats = "@{}".format(out_file)

                if self.fop.is_file(output) and overwrite:
                    self.logger.warning("Over Writing file({})".format(output))
                    self.fop.rm(output)

                iraf.flatcombine(input=flats, output=output, combine=method,
                                 reject=rejection, ccdtype=ccdtype,
                                 subset=subset, process="no",
                                 Stdout="/dev/null")

                if dark is not None:
                    darkcor = 'yes'
                else:
                    darkcor = 'no'

                if zero is not None:
                    zerocor = 'yes'
                else:
                    zerocor = 'no'

                iraf.ccdproc(images=flats, ccdtype='', fixpix='no',
                             oversca="no", trim="no", zerocor=zerocor,
                             darkcor=darkcor, flatcor='no', zero=zero,
                             dark=dark, Stdout="/dev/null")
                return True
            except Exception as e:
                self.logger.error(e)
                return False

        def ccdproc(self, file, output=None, zero=None, dark=None, flat=None, subset="no"):
            """
            Does IRAF calibration
            IRAF ccdproc
            """
            self.logger.info("Ccdproc Started")
            try:
                iraf.imred.unlearn()
                iraf.ccdred.unlearn()
                iraf.ccdred.ccdproc.unlearn()

                ccdred.instrument = self.instrument_path

                yes_no = {True: "no", False: "yes"}

                if output is None:
                    output = ""

                zeroCor = yes_no[zero is None]
                darkCor = yes_no[dark is None]
                flatCor = yes_no[flat is None]

                if flat is not None:
                    if subset == "no":
                        self.fts.update_header(flat, "subset", "")

                iraf.ccdred.flatcombine.subset = subset

                if subset == "no":
                    self.fts.update_header(file, "subset", "")

                iraf.ccdproc(images=file, output=output, ccdtype='',
                             fixpix='no', oversca="no", trim="no",
                             zerocor=zeroCor, darkcor=darkCor,
                             flatcor=flatCor, zero=zero, dark=dark,
                             flat=flat, Stdout="/dev/null")
                return True
            except Exception as e:
                self.logger.error(e)
                return False

        def phot(self, file, output, coords, apertures, annulus=5, dannulus=5, zmag=25):
            """
            Does IRAF photometry
            IRAF phot
            """
            try:
                coord_file = "{}/myraf_coord.coo".format(self.fop.tmp_dir)
                with open(coord_file, "w") as f:
                    for coord in coords:
                        f.write("{}\n".format(coord.replace(",", " ")))

                apertures = list(map(str, apertures))

                ccdred.instrument = self.instrument_path

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
                    self.logger.warning("Over Writing file({})".format(output))
                    self.fop.rm(output)

                iraf.phot.coords = coord_file
                iraf.phot.output = output
                iraf.daophot.phot.verify = "no"
                iraf.daophot.phot.interactive = "no"
                iraf.daophot.phot.radplots = "no"

                iraf.daophot.phot(file, output=output, coords=coord_file,
                                  verbose="no", verify="no", interactive="no")
            #     return True
            except Exception as e:
                self.logger.error(e)
            #     return False

        def textdump(self, file, fields=["id", "mag", "merr"]):
            """
            Returns an array from IRAF mag file
            IRAF txdump
            """
            try:
                ret = []
                txdump = iraf.txdump
                the_fields = ",".join(fields)
                res = txdump(file, the_fields, "yes", Stdout=PIPE)
                for r in res:
                    ret.append(r.split())

                return ret
            except Exception as e:
                self.logger.error(e)

    class Time:
        def __init__(self, logger):
            self.logger = logger

        def str_to_time(self, date):
            """Returns a date object from a string"""
            if date is not None:
                try:
                    if "T" in date:
                        if "." in date:
                            frmt = '%Y-%m-%dT%H:%M:%S.%f'
                        else:
                            frmt = '%Y-%m-%dT%H:%M:%S'
                    elif " " in date:
                        if "." in date:
                            frmt = '%Y-%m-%d %H:%M:%S.%f'
                        else:
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

        def jd2bjd(self, jd, ra, dec):
            obj = SkyCoord(ra, dec, unit=(U.hourangle, U.deg), frame='icrs')
            greenwich = EarthLocation.of_site('greenwich')
            jd = tm(jd, format="jd", location=greenwich)
            ltt_bary = jd.light_travel_time(obj)

            return jd + ltt_bary

        def jd2hjd(self, jd, ra, dec):
            obj = SkyCoord(ra, dec, unit=(U.hourangle, U.deg), frame='icrs')
            greenwich = EarthLocation.of_site('greenwich')
            jd = tm(jd, format="jd", location=greenwich)
            ltt_helio = jd.light_travel_time(obj, 'heliocentric')

            return jd + ltt_helio

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

    class Coordinates:
        """Coordinate Class"""

        def __init__(self, logger):
            self.logger = logger

        def create_angle(self, angle):
            """Convert String to angle"""
            try:
                return Angle(angle)
            except Exception as e:
                self.logger.error(e)

        def alt_az(self, alt, az):
            try:
                alt = self.create_angle(alt)
                az = self.create_angle(az)
                return SkyCoord(AltAz(az, alt))
            except Exception as e:
                self.logger.error(e)

        def ra_dec(self, ra, dec):
            try:
                ra = self.create_angle(ra)
                dec = self.create_angle(dec)
                return SkyCoord(ra=ra, dec=dec)
            except Exception as e:
                self.logger.error(e)

    class Site:
        """Site Class"""

        def __init__(self, logger, lati, long, alti, name="Obervatory"):
            self.logger = logger
            self._lati_ = lati
            self._long_ = long
            self._alti_ = alti
            self._name_ = name

        def create(self):
            """Create site"""
            try:
                return EarthLocation(lat=self._lati_, lon=self._long_, height=self._alti_ * units.m)
            except Exception as e:
                self.logger.error(e)

        def altaz(self, site, obj, utc):
            """Return AltAz for a given object and time for this site"""
            try:
                frame_of_sire = AltAz(obstime=utc, location=site)
                object_alt_az = obj.transform_to(frame_of_sire)
                return object_alt_az
            except Exception as e:
                self.logger.error(e)

    class Obj:
        """Object Class"""

        def __init__(self, logger, ra, dec):
            self.logger = logger
            self._ra_ = ra
            self._dec_ = dec

        def create(self):
            """Create Object"""
            try:
                return SkyCoord(ra=self._ra_, dec=self._dec_)
            except Exception as excpt:
                self.logger.error(excpt)

        def altaz(self, obj, site, utc):
            """Return AltAz for a site object and time for this object"""
            try:
                frame_of_sire = AltAz(obstime=utc, location=site)
                object_alt_az = obj.transform_to(frame_of_sire)
                return object_alt_az
            except Exception as excpt:
                self.logger.error(excpt)

    class Fits:
        def __init__(self, logger):
            self.logger = logger
            self.fop = env.File(logger)

        def cosmic_cleaner(self, file, output, sigclip=12, sigfrac=0.3, objlim=5.0, gain=1.0, readnoise=6.5,
                           satlevel=65535.0, pssl=0.0, iteration=4, sepmed=True, cleantype='meanmask', fsmode='median',
                           psfmodel='gauss', psffwhm=2.5, psfsize=7, psfk=None, psfbeta=4.765):
            """Cleaning cosmic rays from given file"""
            try:
                data = self.data(file)

                new_data, cos = cosla(data, sigclip=sigclip, sigfrac=sigfrac, objlim=objlim, gain=gain,
                                      readnoise=readnoise, satlevel=satlevel, pssl=pssl, niter=iteration,
                                      sepmed=sepmed, cleantype=cleantype, fsmode=fsmode, psfmodel=psfmodel,
                                      psffwhm=psffwhm, psfsize=psfsize, psfk=psfk, psfbeta=psfbeta)

                self.write(output, new_data, header=self.header(file, field="?"))

            except Exception as e:
                self.logger.error(e)

        def align(self, image, ref, output, overwrite=True):
            """Aligning an image with respect of given referance"""
            self.logger.info("Aligning image({}) with reference({})".format(image, ref))
            try:
                image_data = self.data(image)
                image_header = self.header(image, field="?")

                ref_data = self.data(ref)

                img_aligned, _ = aa.register(image_data, ref_data)

                self.write(output, img_aligned, header=image_header, overwrite=overwrite)
                return True
            except Exception as e:
                self.logger.error(e)
                return False

        def alipy_align(self, image, reference, output):
            '''
            Aligns the given FITS images using alipy.
            '''
            self.logger.info("Aligning image({}) with reference({})".format(image, reference))
            try:
                images = [image]

                identifications = alipy.ident.run(reference, images, visu=False,
                                                  sexkeepcat=False, verbose=False)

                outshape = alipy.align.shape(reference, verbose=False)

                for idn in identifications:

                    if idn.ok:
                        alipy.align.affineremap(idn.ukn.filepath, idn.trans,
                                                shape=outshape, alifilepath=output,
                                                makepng=False, verbose=False)

                if os.path.isfile(output) and os.access(output, os.R_OK):
                    return True
                else:
                    self.logger.warning("Alipy is failed!")
                    return False
            except Exception as e:
                self.logger.error(e)
                return False

        def star_find(self, image, default_later=0):
            """Finds sources on image"""
            self.logger.info("Finding sources on image({})".format(image))
            try:
                image_data = self.data(image)
                if len(image_data.shape) > 2:
                    return aa._find_sources(image_data[default_later])

                return aa._find_sources(image_data)
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
                with fts.open(file, ignore_missing_end=True, output_verify='ignore') as hdu:
                    hdu.verify('fix')
                    head = hdu[0].header

                    for i in head:
                        if not i == "":
                            ret.append([i, head[i]])

                    if field == "*":
                        return ret
                    elif field == "?":
                        return head
                    else:
                        return head[field]
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
                hdu[0].header[key[0:8]] = value
                return hdu.close()
            except Exception as e:
                self.logger.error(e)

        def mupdate_header(self, src, key_values):
            """Adds/Updates a header to multiple fits files"""
            self.logger.info("Updating multiple headers in {}".format(src))
            try:
                hdu = fts.open(src, mode='update')
                for key_val in key_values:
                    hdu[0].header[key_val[0][0:8]] = key_val[1]
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

        def write(self, dest, data, header=None, overwrite=True):
            """Writes data to a fits file"""
            self.logger.info("Writeing data to file({})".format(dest))
            try:
                fts.writeto(dest, data, header=header, overwrite=overwrite)
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
                        apertures=[10.0, 15.0], gain=1.21):
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

        # def psf(self, image):
        #     """PSF photometry"""
        #     data = self.data(image)
        #     bkg = Background(data)
        #     pure_data = data - bkg
        #     nddata = NDData(data=pure_data)
        #     sources = self.star_finder(image)
        #     stars_tbl = Table()
        #     size = nmea(sources[:, 2])
        #     for source in sources:
        #         stars_tbl['x'] = source[0]
        #         stars_tbl['y'] = source[1]
        #
        #     stars = extract_stars(nddata, stars_tbl, size=size * 10)
        #     epsf_builder = EPSFBuilder(oversampling=4, maxiters=3,
        #                                progress_bar=False)
        #     epsf, fitted_stars = epsf_builder(stars)
        #     print(epsf)
