from __future__ import annotations

import math
import shutil
from logging import getLogger, Logger
from pathlib import Path
from typing import Optional, Union, List, Any, Tuple, Callable, Dict

import astroalign
import cv2
import numpy as np
import pandas as pd
from astropy import units
from astropy.coordinates import SkyCoord
from astropy.io import fits as fts
from astropy.io.fits.header import Header
from astropy.nddata import CCDData, block_reduce
from astropy.stats import sigma_clipped_stats
from astropy.visualization import ZScaleInterval
from astropy.wcs import WCS
from astropy.wcs.utils import fit_wcs_from_points
from astroquery.astrometry_net import AstrometryNet
from astroquery.simbad import Simbad
from ccdproc import cosmicray_lacosmic, subtract_bias, subtract_dark, flat_correct
from matplotlib import pyplot as plt
from mpl_point_clicker import clicker
from photutils.aperture import CircularAperture, aperture_photometry
from photutils.detection import DAOStarFinder
from photutils.utils import calc_total_error
from scipy import ndimage
from sep import extract as sep_extract, Background, sum_circle
from typing_extensions import Self

from .error import NothingToDo, AlignError, NumberOfElementError, OverCorrection, CardNotFound, Unsolvable
from .models import Data, NUMERICS
from .utils import Fixer, Check

__all__ = ["Fits"]


class Fits(Data):
    def __init__(self, file: Path, logger: Optional[Logger] = None) -> None:

        self.logger = getLogger(f"{self.__class__.__name__}") if logger is None else logger

        self.is_temp = False
        self.file = file

        if not file.exists():
            self.logger.error(f"The File ({self.file}) does not exist.")
            raise FileNotFoundError("File does not exist")

        self.ZMag = 25

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(@: '{id(self)}', path:'{self.file}')"

    def __repr__(self) -> str:
        return self.__str__()
        # return f"{self.__class__.__name__}.from_path('{self.file}')"

    def __del__(self) -> None:
        if self.is_temp:
            self.logger.info("Deleting the temporary file")
            self.file.unlink()

    def __abs__(self) -> str:
        return str(self.file.absolute())

    def __add__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.add(other)

    def __radd__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.add(other)

    def __sub__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.sub(other)

    def __rsub__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.mul(-1).add(other)

    def __mul__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.mul(other)

    def __rmul__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.mul(other)

    def __truediv__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.div(other)

    def __rtruediv__(self, other: Union[Self, float, int]) -> Self:
        if not isinstance(other, (self.__class__, float, int)):
            self.logger.error(f"Other must be either {self.__class__.__name__}, float or int")
            raise NotImplementedError

        return self.div(other).pow(-1)

    def flux_to_mag(self, flux: Union[int, float],
                    flux_error: Union[int, float],
                    exptime: Union[int, float]
                    ) -> Tuple[Union[int, float], Union[int, float]]:
        r"""
        Converts flux and flux error to magnitude and magnitude error

        Notes
        -----
        We use an approximation to calculate mag and merr
        see: https://github.com/spacetelescope/wfc3_photometry/blob/71a40892d665118d161da27465474778b4cf9f1f/photometry_tools/photometry_with_errors.py#L127

        .. math::
            mag = -2.5 * log(f) + 2.5 * log(t_e)

            m_{err} = 1.0857 \times \frac{f}{f_e}

        Where :math:`f` is flux, :math:`t_e` is exposure time, and :math:`f_e` is flux error.

        Parameters
        ----------
        flux : Union[int, float]
            measured flux
        flux_error : Union[int, float]
            measured flux error
        exptime : Union[int, float]
            exposure time

        Returns
        -------
        Tuple[Union[int, float], Union[int, float]]
            calculated magnitude and magnitude error.

        Raises
        ------
        ZeroDivisionError
            when the `flux` is `0`
        """
        self.logger.info("Calculating Flux to Magnitude")

        mag = -2.5 * np.log10(flux)
        if exptime != 0:
            mag += 2.5 * np.log10(exptime)

        if flux_error <= 0:
            mag_err = 0.0
        else:
            mag_err = 1.0857 * flux_error / flux

        if np.isinf(mag_err):
            mag_err = 0

        return mag + self.ZMag, mag_err

    @classmethod
    def from_image(cls, path: str) -> Self:
        """
        Creates a `Fits` object from the given image file

        Parameters
        ----------
        path : str
            path of the file as string

        Returns
        -------
        Fits
            a `Fits` object.

        Raises
        ------
        FileNotFoundError
            when the file does not exist
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"File {path} does not exist")

        image = cv2.imread(path)
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cls.from_data_header(gray_frame)

    @classmethod
    def from_path(cls, path: str) -> Self:
        """
        Creates a `Fits` object from the given file `path` as string

        Parameters
        ----------
        path : str
            path of the file as string

        Returns
        -------
        Fits
            a `Fits` object.

        Raises
        ------
        FileNotFoundError
            when the file does not exist
        """
        return cls(Path(path))

    @classmethod
    def from_data_header(cls, data: Any,
                         header: Optional[Header] = None,
                         output: Optional[str] = None,
                         override: bool = False) -> Self:
        """
        Creates a `Fits` object th give `data` and `header`

        Parameters
        ----------
        data : Any
            the data as `np.ndarray`
        header : Header
            the header as `Header`
        output : str, optional
            the wanted file path.
            a temporary file will be created if it's `None`
        override : bool, default=False
            delete already existing file if `true`

        Returns
        -------
        Fits
            a `Fits` object.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        new_output = Fixer.output(output=output, override=override)

        if not cls.high_precision:
            data_type = Fixer.smallest_data_type(data)
            data = data.astype(data_type)

        fts.writeto(new_output, data, header=header, output_verify="silentfix")
        fits = cls.from_path(new_output)

        fits.is_temp = output is None
        return fits

    @classmethod
    def sample(cls) -> Self:
        """
        Creates a sample `Fits` object
        see: https://www.astropy.org/astropy-data/tutorials/FITS-images/HorseHead.fits


        Returns
        -------
        Fits
            a `Fits` object.
        """
        file = str(Path(__file__).parent / "sample.fits")
        data = fts.getdata(file)
        header = fts.getheader(file)
        return cls.from_data_header(data, header=header)

    def reset_zmag(self) -> None:
        """
        Resets Zmag value to 25

        Notes
        -----
        ZMag is the value added to calculated magnitude from flux.

        .. math::
            mag = ZMag + mag_c

        Where :math:`ZMag` is Zero Magnitude, :math:`mag_c` is calculated magnitude
        """
        self.logger.info("Resetting ZMag to 25")
        self.ZMag = 25

    def header(self) -> pd.DataFrame:
        """
        Returns headers of the fits file

        Returns
        -------
        pd.DataFrame
            the headers as dataframe
        """
        self.logger.info("Getting header")

        header = fts.getheader(abs(self))

        return pd.DataFrame(
            {i: header[i] for i in header if isinstance(header[i], (bool, int, float, str))}, index=[0]).assign(
            image=[abs(self)]
        ).set_index("image")

    def data(self) -> Any:
        """
        returns the data of fits file

        Returns
        -------
        Any
            the data as `np.ndarray`

        Raises
        ------
        ValueError
            if the fits file is not an image
        """
        self.logger.info("Getting data")

        data = fts.getdata(abs(self))
        if not isinstance(data, np.ndarray):
            self.logger.error("Unknown Fits type")
            raise ValueError("Unknown Fits type.  Maybe its a fits table and not an image.")

        return data.astype(float)

    def value(self, x: int, y: int) -> float:
        """
        Returns a value of asked coordinate

        Parameters
        ----------
        x : int
            x coordinate of asked pixel
        y: int
            y coordinate of asked pixel
        Returns
        -------
        float
            value of the x and y

        Raises
        ------
        IndexError
            when the x, y coordinate is out of boundaries
        """
        return float(self.data()[x][y])

    def pure_header(self) -> Header:
        """
        Returns the `Header` of the file

        Returns
        -------
        Header
            the Header object of the file
        """
        self.logger.info("Getting header (as an astropy header object)")

        return fts.getheader(abs(self))

    def ccd(self) -> CCDData:
        """
        Returns the CCDData of the given file

        Returns
        -------
        CDDData
            the CCDData of the file
        """
        self.logger.info("Getting CCDData")

        return CCDData.read(self.file, unit="adu")

    def imstat(self) -> pd.DataFrame:
        """
        Returns statistics of the data

        Notes
        -----
        Stats are calculated using numpy and are:

        - number of pixels
        - mean
        - standard deviation
        - min
        - max

        Returns
        -------
        pd.DataFrame
            the statistics as dataframe
        """
        self.logger.info("Calculating image statistics")

        data = self.data()
        return pd.DataFrame(
            [
                [
                    abs(self), data.size, np.mean(data), np.std(data),
                    np.min(data), np.max(data)
                ]
            ],
            columns=["image", "npix", "mean", "stddev", "min", "max"]
        ).set_index("image")

    def cosmic_clean(self, output: Optional[str] = None,
                     override: bool = False, sigclip: float = 4.5,
                     sigfrac: float = 0.3, objlim: int = 5, gain: float = 1.0,
                     readnoise: float = 6.5, satlevel: float = 65535.0,
                     niter: int = 4, sepmed: bool = True,
                     cleantype: str = 'meanmask', fsmode: str = 'median',
                     psfmodel: str = 'gauss', psffwhm: float = 2.5,
                     psfsize: int = 7, psfk: Optional[Any] = None,
                     psfbeta: float = 4.765, gain_apply: bool = True) -> Self:
        """
        Clears cosmic rays from the fits file

        [1]: https://ccdproc.readthedocs.io/en/latest/api/ccdproc.cosmicray_lacosmic.html

        Parameters
        ----------
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.
        sigclip: float, default=4.5
            Laplacian-to-noise limit for cosmic ray detection.
            Lower values will flag more pixels as cosmic rays.
            Default: 4.5. see [1]
        sigfrac: float, default=0.3
            Fractional detection limit for neighboring pixels.
            For cosmic ray neighbor pixels, a Laplacian-to-noise
            detection limit of sigfrac * sigclip will be used.
            Default: 0.3. see [1]
        objlim: int, default=5
            Minimum contrast between Laplacian image
            and the fine structure image.
            Increase this value if cores of bright stars are
            flagged as cosmic rays.
            Default: 5.0. see [1]
        gain: float, default=1.5
            Gain of the image (electrons / ADU).
            We always need to work in electrons for cosmic ray detection.
            Default: 1.0 see [1]
        readnoise: float, default=6.5
            Read noise of the image (electrons).
            Used to generate the noise model of the image.
            Default: 6.5. see [1]
        satlevel: float, default=65535.0
            Saturation level of the image (electrons).
            This value is used to detect saturated stars and pixels at or
            above this level are added to the mask.
            Default: 65535.0. see [1]
        niter: int, default=4
            Number of iterations of the LA Cosmic algorithm to perform.
            Default: 4. see [1]
        sepmed: bool, default=True
            Use the separable median filter instead of the full median filter.
            The separable median is not identical to the full median filter,
            but they are approximately the same,
            the separable median filter is significantly faster,
            and still detects cosmic rays well.
            Note, this is a performance feature,
            and not part of the original L.A. Cosmic.
            Default: True. see [1]
        cleantype: str, default='meanmask'
            Set which clean algorithm is used:
            1) "median": An unmasked 5x5 median filter.
            2) "medmask": A masked 5x5 median filter.
            3) "meanmask": A masked 5x5 mean filter.
            4) "idw": A masked 5x5 inverse distance weighted interpolation.
            Default: "meanmask". see [1]
        fsmode: float, default='median'
            Method to build the fine structure image:
            1) "median": Use the median filter in the standard LA
            Cosmic algorithm.
            2) "convolve": Convolve the image with the psf kernel to
            calculate the fine structure image.
            Default: "median". see [1]
        psfmodel: str, default='gauss'
            Model to use to generate the psf kernel if fsmode == ‘convolve’
            and psfk is None.
            The current choices are Gaussian and Moffat profiles:
            - "gauss" and "moffat" produce circular PSF kernels.
            - The "gaussx" and "gaussy" produce Gaussian kernels in the x
            and y directions respectively.
            Default: "gauss". see [1]
        psffwhm: float, default=2.5
            Full Width Half Maximum of the PSF to use to generate the kernel.
            Default: 2.5. see [1]
        psfsize: int, default=7
            Size of the kernel to calculate.
            Returned kernel will have size psfsize x psfsize.
            psfsize should be odd.
            Default: 7. see [1]
        psfk: Any, optional
            PSF kernel array to use for the fine structure image
            if fsmode == 'convolve'. If None and fsmode == 'convolve',
            we calculate the psf kernel using psfmodel.
            Default: None. see [1]
        psfbeta: float, default=4.765
            Moffat beta parameter. Only used if fsmode=='convolve' and
            psfmodel=='moffat'.
            Default: 4.765.
        gain_apply: bool, default=True
            If True, return gain-corrected data, with correct units,
            otherwise do not gain-correct the data.
            Default is True to preserve backwards compatibility. see [1]

        Returns
        -------
        Fits
            Cleaned fits
        """
        self.logger.info("Cleaning the data")

        cleaned_data, _ = cosmicray_lacosmic(
            self.data(), sigclip=sigclip,
            sigfrac=sigfrac, objlim=objlim,
            gain=gain, readnoise=readnoise, satlevel=satlevel,
            niter=niter, sepmed=sepmed, cleantype=cleantype.lower(), fsmode=fsmode.lower(),
            psfmodel=psfmodel.lower(), psffwhm=psffwhm, psfsize=psfsize, psfk=psfk,
            psfbeta=psfbeta, gain_apply=gain_apply
        )

        return self.from_data_header(cleaned_data.value, header=self.pure_header(), output=output, override=override)

    def hedit(self, keys: Union[str, List[str]],
              values: Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]] = None,
              comments: Optional[Union[str, List[str]]] = None, delete: bool = False, value_is_key: bool = False
              ) -> Self:
        """
        Edits header of the given file.

        Parameters
        ----------
        keys: str or List[str]
            Keys to be altered.
        values: Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]], optional
            Values to be added.
            Would be ignored if delete is True.
        comments: Optional[ste, List[str]], optional
            Comments to be added.
            Would be ignored if delete is True.
        delete: bool, optional
            Deletes the key from header if True.
        value_is_key: bool, optional
            Adds value of the key given in values if True. Would be ignored if
            delete is True.

        Returns
        -------
        Fits
            The same `Fits` object
        """
        self.logger.info("Editing header")
        if delete:
            if isinstance(keys, str):
                keys = [keys]

            with fts.open(abs(self), "update") as hdu:
                for key in keys:
                    if key in hdu[0].header:
                        del hdu[0].header[key]
                    else:
                        self.logger.info("Key does not exist")

                hdu.flush()

        else:
            if values is None:
                self.logger.error("Delete is False and Value is not given")
                raise NothingToDo("Delete is False and Value is not given")

            keys_to_use, values_to_use, comments_to_use = Fixer.key_value_pair(keys, values, comments)

            if len(keys_to_use) != len(values_to_use):
                self.logger.error("List of keys and values must be equal in length")
                raise ValueError("List of keys and values must be equal in length")

            with fts.open(abs(self), "update") as hdu:
                for key, value, comment in zip(keys_to_use, values_to_use, comments_to_use):
                    if value_is_key:
                        hdu[0].header[key] = hdu[0].header[value]
                    else:
                        hdu[0].header[key] = value
                    hdu[0].header.comments[key] = comment

                hdu.flush()

        return self

    def save_as(self, output: str, override: bool = False) -> Self:
        """
        Saves the `Fits` file as output.

        Parameters
        ----------
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        self.logger.info("Saving the fits to as")

        new_output = Fixer.output(output=output, override=override)
        shutil.copy(self.file, new_output)
        return self.__class__.from_path(new_output)

    def add(self, other: Union[Self, float, int], output: Optional[str] = None, override: bool = False) -> Self:
        r"""
        Does Addition operation on the `Fits` object

        Notes
        -----
        It is able to add numeric values as other `Fits`

        - If other is numeric each element of the matrix will be added to the number.
        - If other is another `Fits` elementwise summation will be done.

        Parameters
        ----------
        other: Union[Self, float, int]
            Either a `Fits` object, float, or integer
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        self.logger.info("Making addition operation")

        if not isinstance(other, (float, int, self.__class__)):
            self.logger.error(f"Please provide either a {self.__class__} Object or a numeric value")
            raise ValueError(f"Please provide either a {self.__class__} Object or a numeric value")

        if isinstance(other, (float, int)):
            new_data = self.data() + other
        else:
            new_data = self.data() + other.data()

        return self.__class__.from_data_header(
            new_data, header=self.pure_header(),
            output=output, override=override
        )

    def sub(self, other: Union[Self, float, int], output: Optional[str] = None, override: bool = False) -> Self:
        """
        Does Subtraction operation on the `Fits` object

        Notes
        -----
        It is able to subtract numeric values as other `Fits`

        - If other is numeric each element of the matrix will be subtracted by the number.
        - If other is another `Fits` elementwise subtraction will be done.


        Parameters
        ----------
        other: Union[Self, float, int]
            Either a `Fits` object, float, or integer
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        self.logger.info("Making subtraction operation")

        if not isinstance(other, (float, int, self.__class__)):
            self.logger.error(f"Please provide either a {self.__class__} Object or a numeric value")
            raise ValueError(f"Please provide either a {self.__class__} Object or a numeric value")

        if isinstance(other, (float, int)):
            new_data = self.data() - other
        else:
            new_data = self.data() - other.data()

        return self.__class__.from_data_header(
            new_data, header=self.pure_header(),
            output=output, override=override
        )

    def mul(self, other: Union[Self, float, int], output: Optional[str] = None, override: bool = False) -> Self:
        """
        Does Multiplication operation on the `Fits` object

        Notes
        -----
        It is able to multiply numeric values as other `Fits`

        - If other is numeric each element of the matrix will be multiplied by the number.
        - If other is another `Fits` elementwise multiplication will be done.


        Parameters
        ----------
        other: Union[Self, float, int]
            Either a `Fits` object, float, or integer
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        self.logger.info("Making multiplication operation")

        if not isinstance(other, (float, int, self.__class__)):
            self.logger.error(f"Please provide either a {self.__class__} Object or a numeric value")
            raise ValueError(f"Please provide either a {self.__class__} Object or a numeric value")

        if isinstance(other, (float, int)):
            new_data = self.data() * other
        else:
            new_data = self.data() * other.data()

        return self.__class__.from_data_header(
            new_data, header=self.pure_header(),
            output=output, override=override
        )

    def div(self, other: Union[Self, float, int], output: Optional[str] = None, override: bool = False) -> Self:
        """
        Does Division operation on the `Fits` object

        Notes
        -----
        It is able to divide numeric values as other `Fits`

        - If other is numeric each element of the matrix will be divided by the number.
        - If other is another `Fits` elementwise division will be done.


        Parameters
        ----------
        other: Union[Self, float, int]
            Either a `Fits` object, float, or integer
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        self.logger.info("Making division operation")

        if not isinstance(other, (float, int, self.__class__)):
            self.logger.error(f"Please provide either a {self.__class__} Object or a numeric value")
            raise ValueError(f"Please provide either a {self.__class__} Object or a numeric value")

        if isinstance(other, (float, int)):
            new_data = self.data() / other
        else:
            new_data = self.data() / other.data()

        return self.__class__.from_data_header(
            new_data, header=self.pure_header(),
            output=output, override=override
        )

    def pow(self, other: Union[Self, float, int], output: Optional[str] = None, override: bool = False) -> Self:
        """
        Does Power operation on the `Fits` object

        Notes
        -----
        It is able to power to numeric values as other `Fits`

        - If other is numeric each element of the matrix will be raised by the number.
        - If other is another `Fits` elementwise power will be done.


        Parameters
        ----------
        other: Union[Self, float, int]
            Either a `Fits` object, float, or integer
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        FileExistsError
            when the file does exist and `override` is `False`
        """
        self.logger.info("Making power operation")

        if not isinstance(other, (float, int, self.__class__)):
            self.logger.error(f"Please provide either a {self.__class__} Object or a numeric value")
            raise ValueError(f"Please provide either a {self.__class__} Object or a numeric value")

        if isinstance(other, (float, int)):
            new_data = self.data() ** other
        else:
            new_data = self.data() ** other.data()

        return self.__class__.from_data_header(
            new_data, header=self.pure_header(),
            output=output, override=override
        )

    def imarith(self, other: Union[Self, float, int], operand: str,
                output: Optional[str] = None, override: bool = False) -> Self:
        """
        Does Arithmetic operation on the `Fits` object

        Notes
        -----
        It is able to do operation with numeric values as other `Fits`

        - If other is numeric each element of the matrix will be processed by the number.
        - If other is another `Fits` elementwise operation will be done.


        Parameters
        ----------
        other: Union[Self, float, int]
            Either a `Fits`, `float`, or `int`
        operand: str
            operation as string. One of `["+", "-", "*", "/"]`
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            New `Fits` object of saved fits file.

        Raises
        ------
        ValueError
            when the given value is not `Fits`, `float`, or `int`
        ValueError
            when operand is not one of `["+", "-", "*", "/", "**", "^"]`
        """
        self.logger.info("Making an arithmetic operation")

        if not isinstance(other, (float, int, self.__class__)):
            self.logger.error(f"Please provide either a {self.__class__} Object or a numeric value")
            raise ValueError(f"Please provide either a {self.__class__} Object or a numeric value")

        Check.operand(operand)

        if operand == "+":
            return self.add(other, output=output, override=override)
        elif operand == "-":
            return self.sub(other, output=output, override=override)
        elif operand == "*":
            return self.mul(other, output=output, override=override)
        elif operand in ("**", "^"):
            return self.pow(other, output=output, override=override)
        else:
            return self.div(other, output=output, override=override)

    def align(self, reference: Self, output: Optional[str] = None,
              max_control_points: int = 50, min_area: int = 5,
              override: bool = False) -> Self:
        """
        Aligns the fits file with the given reference

        [1]: https://astroalign.quatrope.org/en/latest/api.html#astroalign.register

        Parameters
        ----------
        reference: Self
            The reference Image to be aligned as a Fits object.
        output: str, optional
            Path of the new fits file.
        max_control_points: int, default=50
            The maximum number of control point-sources to
            find the transformation. [1]
        min_area: int, default=5
            Minimum number of connected pixels to be considered a source. [1]
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            `Fits` object of aligned image.
        """
        self.logger.info("Aligning the image")

        if not isinstance(reference, self.__class__):
            self.logger.error(f"Other must be a {self.__class__}")
            raise ValueError(f"Other must be a {self.__class__}")

        try:
            data = self.data()
            reference_data = reference.data()
            w = WCS(self.pure_header())

            t, (source_list, target_list) = astroalign.find_transform(
                source=data,
                target=reference_data,
                max_control_points=max_control_points,
                min_area=min_area,
            )

            registered_image, _ = astroalign.apply_transform(
                t, data, reference_data, 0, False
            )

            try:

                xs = source_list[:, 0]
                ys = source_list[:, 1]

                new_xs = target_list[:, 0]
                new_ys = target_list[:, 1]

                skys = w.pixel_to_world(xs.tolist(), ys.tolist())
                w = fit_wcs_from_points([new_xs, new_ys], skys)
            except Unsolvable:
                self.logger.info("No WCS found in header")
            except AttributeError as e:
                self.logger.info(e)

            temp_header = Header()
            # temp_header.extend(self.pure_header(), unique=True, update=True)
            temp_header.extend(w.to_header(), unique=True, update=True)
            return self.__class__.from_data_header(
                registered_image, header=temp_header,
                output=output, override=override
            )
        except Exception as e:
            self.logger.error(e)
            raise AlignError(e)

    def show(self, scale: bool = True, sources: Optional[pd.DataFrame] = None) -> None:
        """
        Shows the Image using matplotlib.

        Parameters
        ----------
        scale: bool, optional
            Scales the Image if True.
        sources: pd.DataFrame, optional
            Draws points on image if a list is given.
        """
        self.logger.info("Showing the image")

        zscale = ZScaleInterval() if scale else lambda x: x

        plt.imshow(zscale(self.data()), cmap="Greys_r")

        if sources is not None:
            plt.scatter(sources["xcentroid"], sources["ycentroid"])

        plt.xticks([])
        plt.yticks([])
        plt.show()

    def coordinate_picker(self, scale: bool = True) -> pd.DataFrame:
        """
        Shows the Image using matplotlib and returns a list of
        coordinates picked by user.

        Parameters
        ----------
        scale: bool, optional
            Scales the Image if True.

        Returns
        -------
        pd.DataFrame
            List of coordinates selected.
        """
        self.logger.info("Showing the image to pick some coordinates")

        zscale = ZScaleInterval() if scale else lambda x: x

        fig, ax = plt.subplots(constrained_layout=True)
        ax.imshow(zscale(self.data()), cmap="Greys_r")
        klkr = clicker(ax, ["source"], markers=["o"])
        plt.show()
        if len(klkr.get_positions()["source"]) == 0:
            return pd.DataFrame([], columns=["xcentroid", "ycentroid"])

        return pd.DataFrame(
            klkr.get_positions()["source"], columns=[
                "xcentroid", "ycentroid"])

    def solve_field(self, api_key: str, solve_timeout: int = 120,
                    force_image_upload: bool = False,
                    output: Optional[str] = None, override: bool = False
                    ) -> Self:
        """
        Solves filed for the given file.

        [1]: https://astroquery.readthedocs.io/en/latest/api/astroquery.astrometry_net.AstrometryNetClass.html
            #astroquery.astrometry_net.AstrometryNetClass.solve_from_image

        Parameters
        ----------
        api_key: str
            api_key of astrometry.net (https://nova.astrometry.net/api_help)
        solve_timeout: int, default=120
            solve timeout as seconds
        force_image_upload: bool, default=False
            If True, upload the image to astrometry.net even if it is possible to detect sources in the image locally.
            This option will almost always take longer than finding sources locally.
            It will even take longer than installing photutils and then rerunning this.
            Even if this is False the image will be uploaded unless photutils is installed.
            see: [1]
        output: str
            New path to save the file.
        override: bool, default=False
            If True will overwrite the new_path if a file is already exists.

        Returns
        -------
        Fits
            `Fits` object of field solved image.

        Raises
        ------
        Unsolvable
            when the data is unsolvable or timeout
        """
        try:
            self.logger.info("Solving field")
            ast = AstrometryNet()
            ast.api_key = api_key
            wcs_header = ast.solve_from_image(abs(self), force_image_upload=force_image_upload)
            return self.__class__.from_data_header(self.data(), header=wcs_header, output=output, override=override)
        except Exception as error:
            self.logger.error(error)
            raise Unsolvable("Cannot solve")

    def zero_correction(self, master_zero: Self, output: Optional[str] = None,
                        override: bool = False, force: bool = False) -> Self:
        """
        Does zero correction of the data

        Parameters
        ----------
        master_zero : Self
            Zero file to be used for correction
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.
        force: bool, default=False
            Overcorrection flag

        Returns
        -------
        Fits
            Zero corrected `Fits` object

        Raises
        ------
        OverCorrection
            when the `Fits` object is already
            zero corrected and `force` is `False`
        """
        self.logger.info("Making zero correction on the image")

        if "MY-ZERO" not in self.header() or force:
            zero_corrected = subtract_bias(self.ccd(), master_zero.ccd())
            header = self.pure_header()
            header["MY-ZERO"] = master_zero.file.name

            return self.__class__.from_data_header(
                zero_corrected.data, header=header,
                output=output, override=override
            )

        self.logger.error("This Data is already zero corrected")
        raise OverCorrection("This Data is already zero corrected")

    def dark_correction(self, master_dark: Self, exposure: Optional[str] = None, output: Optional[str] = None,
                        override: bool = False, force: bool = False) -> Self:
        """
        Does dark correction of the data

        Parameters
        ----------
        master_dark : Self
            Dark file to be used for correction
        exposure : str, optional
            header card containing exptime
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.
        force: bool, default=False
            Overcorrection flag

        Returns
        -------
        Fits
            Dark corrected `Fits` object

        Raises
        ------
        OverCorrection
            when the `Fits` object is already
            dark corrected and `force` is `False`
        """
        self.logger.info("Making dark correction on the image")

        if "MY-DARK" not in self.header() or force:
            if exposure is None:
                options = {"dark_exposure": 1 * units.s,
                           "data_exposure": 1 * units.s}
            else:
                if exposure not in self.header() or \
                        exposure not in master_dark.header():
                    self.logger.error(f"Key {exposure} not found in file, master_dark or both")
                    raise CardNotFound(f"Key {exposure} not found in file, master_dark or both")

                options = {
                    "dark_exposure": float(
                        master_dark.header()[exposure].values[0]) * units.s,
                    "data_exposure": float(
                        self.header()[exposure].values[0]) * units.s
                }

            dark_corrected = subtract_dark(
                self.ccd(), master_dark.ccd(),
                **options, scale=True
            )
            header = self.pure_header()
            header["MY-DARK"] = master_dark.file.name

            return self.__class__.from_data_header(
                dark_corrected.data, header=header,
                output=output, override=override
            )

        self.logger.error("This Data is already dark corrected")
        raise OverCorrection("This Data is already dark corrected")

    def flat_correction(self, master_flat: Self, output: Optional[str] = None,
                        override: bool = False, force: bool = False) -> Self:
        """
        Does flat correction of the data

        Parameters
        ----------
        master_flat : Self
            Flat file to be used for correction
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.
        force: bool, default=False
            Overcorrection flag

        Returns
        -------
        Fits
            Flat corrected `Fits` object

        Raises
        ------
        OverCorrection
            when the `Fits` object is already
            flat corrected and `force` is `False`
        """
        self.logger.info("Making flat correction on the image")

        if "MY-FLAT" not in self.header() or force:
            flat_corrected = flat_correct(self.ccd(), master_flat.ccd())
            header = self.pure_header()
            header["MY-FLAT"] = master_flat.file.name

            return self.__class__.from_data_header(
                flat_corrected.data, header=header,
                output=output, override=override
            )

        self.logger.error("This Data is already flat corrected")
        raise OverCorrection("This Data is already flat corrected")

    def ccdproc(self, master_zero: Optional[Self] = None, master_dark: Optional[Self] = None,
                master_flat: Optional[Self] = None, exposure: Optional[str] = None, output: Optional[str] = None,
                override: bool = False, force: bool = False) -> Self:
        """
        Does ccdproc correction of the data. can be zero, dark, or flat in any combination

        Parameters
        ----------
        master_zero : Optional[Self]
            Zero file to be used for correction
        master_dark : Optional[Self]
            Dark file to be used for correction
        master_flat : Optional[Self]
            Flat file to be used for correction
        exposure : str, optional
            header card containing exptime
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.
        force: bool, default=False
            Overcorrection flag

        Returns
        -------
        Fits
            ccd corrected `Fits` object
        """
        self.logger.info("Making ccd correction on the image")

        if all(each is None for each in [master_zero, master_dark, master_flat]):
            raise NothingToDo("None of master Zero, Dark, or Flat is not provided")

        corrected = self.ccd()
        header = self.pure_header()
        if master_zero:
            if "MY-ZERO" not in self.header() or force:
                corrected = subtract_bias(corrected, master_zero.ccd())
                header["MY-ZERO"] = master_zero.file.name

        if master_dark:
            if "MY-DARK" not in self.header() or force:
                if exposure is None:
                    options = {"dark_exposure": 1 * units.s,
                               "data_exposure": 1 * units.s}
                else:
                    if exposure not in self.header() or \
                            exposure not in master_dark.header():
                        self.logger.error(f"Key {exposure} not found in file, master_dark or both")
                        raise CardNotFound(f"Key {exposure} not found in file, master_dark or both")

                    options = {
                        "dark_exposure": float(
                            master_dark.header()[exposure].values[0]) * units.s,
                        "data_exposure": float(
                            self.header()[exposure].values[0]) * units.s
                    }
                corrected = subtract_dark(
                    corrected, master_dark.ccd(),
                    **options, scale=True
                )
                header["MY-DARK"] = master_dark.file.name

        if master_flat:
            if "MY-FLAT" not in self.header() or force:
                corrected = flat_correct(corrected, master_flat.ccd())
                header["MY-FLAT"] = master_flat.file.name

        return self.__class__.from_data_header(
            corrected.data, header=header,
            output=output, override=override
        )

    def background(self) -> Background:
        """
        Returns a `Background` object of the fits file.

        Returns
        -------
        Background
            background object of `Fits`
        """
        self.logger.info("Getting background")

        return Background(self.data())

    def daofind(self, sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> pd.DataFrame:
        """
        Runs daofind to detect sources on the image.

        [1]: https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipped_stats.html

        [2]: https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html

        Parameters
        ----------
        sigma: float, default=3
            The number of standard deviations to use for both the lower and
            upper clipping limit. These limits are overridden by sigma_lower
            and sigma_upper, if input.
            The default is 3. [1]
        fwhm: float, default=3
            The full-width half-maximum (FWHM) of the major axis of the
            Gaussian kernel in units of pixels. [2]
        threshold: float, default=5
            The absolute image value above which to select sources. [2]

        Returns
        -------
        pd.DataFrame
            List of sources found on the image.
        """
        self.logger.info("Extracting sources (daofind) from images")

        mean, median, std = sigma_clipped_stats(self.data(), sigma=sigma)
        daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold * std)
        sources = daofind(self.data() - median)

        if sources is not None:
            return sources.to_pandas()

        return pd.DataFrame(
            [],
            columns=[
                "id", "xcentroid", "ycentroid", "sharpness", "roundness1",
                "roundness2", "npix", "sky", "peak", "flux", "mag"
            ]
        )

    def extract(self, detection_sigma: float = 5.0, min_area: float = 5.0) -> pd.DataFrame:
        """
        Runs astroalign._find_sources to detect sources on the image.

        Parameters
        ----------
        detection_sigma: float, default=5
            `thresh = detection_sigma * bkg.globalrms`
        min_area: float, default=5
            Minimum area

        Returns
        -------
        pd.DataFrame
            List of sources found on the image.
        """
        self.logger.info("Extracting sources (sep_extract) from images")

        bkg = self.background()
        thresh = detection_sigma * bkg.globalrms
        sources = sep_extract(self.data() - bkg.back(), thresh,
                              minarea=min_area)
        sources.sort(order="flux")
        if len(sources) < 0:
            self.logger.error("No source was found")
            raise NumberOfElementError("No source was found")

        return pd.DataFrame(
            sources,
        ).rename(columns={"x": "xcentroid", "y": "ycentroid"})

    def photometry_sep(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                       headers: Optional[Union[str, list[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> pd.DataFrame:
        """
        Does a photometry using sep

        Parameters
        ----------
        xs: Union[float, int, List[Union[float, int]]]
            x coordinate(s)
        ys: Union[float, int, List[Union[float, int]]]
            y coordinate(s)
        rs: Union[float, int, List[Union[float, int]]]
            aperture(s)
        headers: Union[str, list[str]], optional
            Header keys to be extracted after photometry
        exposure: Union[str, float, int], optional
            Header key that contains or a numeric value of exposure time

        Returns
        -------
        pd.DataFrame
            photometric data as dataframe

        Raises
        ------
        NumberOfElementError
            when `x` and `y` coordinates does not have the same length
        """
        self.logger.info("Doing photometry (sep) on the image")

        table = []

        the_header = self.header()

        if exposure is None:
            exposure_to_use = 0.0
        else:
            if isinstance(exposure, (int, float)):
                exposure_to_use = exposure
            else:
                exposure_to_use = float(the_header[exposure].iloc[0])

        new_xs, new_ys = Fixer.coordinate(xs, ys)
        new_rs = Fixer.aperture(rs)
        new_headers = Fixer.header(headers)

        headers_ = []
        keys_ = []
        for new_header in new_headers:
            keys_.append(new_header)
            try:
                headers_.append(the_header[new_header].iloc[0])
            except KeyError:
                headers_.append(None)

        data = self.data()
        background = self.background()

        clean_d = data - background.rms()
        error = calc_total_error(
            self.data(), background, exposure_to_use
        )
        for new_r in new_rs:
            fluxes, flux_errs, flags = sum_circle(
                data,
                new_xs, new_ys, new_r,
                err=error
            )
            for x, y, flux, flux_err, flag in zip(new_xs, new_ys, fluxes,
                                                  flux_errs, flags):
                try:
                    sky = self.pixels_to_skys(x, y).iloc[0].sky
                    ra = sky.ra.degree
                    dec = sky.dec.degree
                except Exception as e:
                    self.logger.info(f"Could not get ra, dec. {e}")
                    ra = None
                    dec = None

                value = clean_d[int(x)][int(y)]
                snr = np.nan if value < 0 else math.sqrt(value)
                mag, mag_err = self.flux_to_mag(flux, flux_err,
                                                exposure_to_use)
                table.append(
                    [
                        abs(self), "sep", x, y, ra, dec, new_r, flux, flux_err,
                        flag, snr, mag, mag_err, *headers_
                    ]
                )
        return pd.DataFrame(
            table,
            columns=[
                "image", "package", "xcentroid", "ycentroid", "ra", "dec", "aperture",
                "flux", "flux_error", "flag", "snr", "mag", "merr", *keys_
            ]
        ).set_index("image")

    def photometry_phu(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                       headers: Optional[Union[str, list[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> pd.DataFrame:
        """
        Does a photometry using photutils

        Parameters
        ----------
        xs: Union[float, int, List[Union[float, int]]]
            x coordinate(s)
        ys: Union[float, int, List[Union[float, int]]]
            y coordinate(s)
        rs: Union[float, int, List[Union[float, int]]]
            aperture(s)
        headers: Union[str, list[str]], optional
            Header keys to be extracted after photometry
        exposure: Union[str, float, int], optional
            Header key that contains or a numeric value of exposure time

        Returns
        -------
        pd.DataFrame
            photometric data as dataframe

        Raises
        ------
        NumberOfElementError
            when `x` and `y` coordinates does not have the same length
        """
        self.logger.info("Doing photometry (photutils) on the image")

        table = []

        the_header = self.header()

        if exposure is None:
            exposure_to_use = 0.0
        else:
            if isinstance(exposure, (int, float)):
                exposure_to_use = exposure
            else:
                exposure_to_use = float(the_header[exposure].iloc[0])

        new_xs, new_ys = Fixer.coordinate(xs, ys)
        new_rs = Fixer.aperture(rs)
        new_headers = Fixer.header(headers)

        headers_ = []
        keys_ = []
        for new_header in new_headers:
            keys_.append(new_header)
            try:
                headers_.append(the_header[new_header].iloc[0])
            except KeyError:
                headers_.append(None)

        data = self.data()
        background = self.background()

        clean_d = data - background.rms()

        for new_r in new_rs:
            apertures = CircularAperture([
                [new_x, new_y] for new_x, new_y in zip(new_xs, new_ys)
            ], r=new_r)
            error = calc_total_error(
                self.data(), self.background(), exposure_to_use
            )
            phot_table = aperture_photometry(data, apertures, error=error)

            for phot_line in phot_table:
                value = clean_d[
                    int(phot_line["xcenter"].value)
                ][
                    int(phot_line["ycenter"].value)
                ]
                snr = np.nan if value < 0 else math.sqrt(value)
                mag, mag_err = self.flux_to_mag(
                    phot_line["aperture_sum"],
                    phot_line["aperture_sum_err"],
                    exposure_to_use
                )

                try:
                    sky = self.pixels_to_skys(phot_line["xcenter"].value, phot_line["ycenter"].value).iloc[0].sky
                    ra = sky.ra.degree
                    dec = sky.dec.degree
                except Exception as e:
                    self.logger.info(f"Could not get ra, dec. {e}")
                    ra = None
                    dec = None

                table.append(
                    [
                        abs(self), "phu",
                        phot_line["xcenter"].value,
                        phot_line["ycenter"].value,
                        ra, dec,
                        new_r,
                        phot_line["aperture_sum"],
                        phot_line["aperture_sum_err"],
                        None, snr, mag, mag_err, *headers_
                    ]
                )

        return pd.DataFrame(
            table,
            columns=[
                "image", "package", "xcentroid", "ycentroid", "ra", "dec", "aperture",
                "flux", "flux_error", "flag", "snr", "mag", "merr", *keys_
            ]
        ).set_index("image")

    def photometry(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                   headers: Optional[Union[str, list[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> pd.DataFrame:
        """
        Does a photometry using both sep and photutils

        Parameters
        ----------
        xs: Union[float, int, List[Union[float, int]]]
            x coordinate(s)
        ys: Union[float, int, List[Union[float, int]]]
            y coordinate(s)
        rs: Union[float, int, List[Union[float, int]]]
            aperture(s)
        headers: Union[str, list[str]], optional
            Header keys to be extracted after photometry
        exposure: Union[str, float, int], optional
            Header key that contains or a numeric value of exposure time

        Returns
        -------
        pd.DataFrame
            photometric data as dataframe

        Raises
        ------
        NumberOfElementError
            when `x` and `y` coordinates does not have the same length
        """
        return pd.concat(
            (self.photometry_sep(
                xs, ys, rs, headers=headers, exposure=exposure
            ),
             self.photometry_phu(
                 xs, ys, rs, headers=headers, exposure=exposure
             ))
        )

    def shift(self, x: int, y: int, output: Optional[str] = None, override: bool = False) -> Self:
        """
        Shifts the data of `Fits` object

        Parameters
        ----------
        x: int
            x coordinate
        y: int
            y coordinate
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.

        Returns
        -------
        Fits
            shifted `Fits` object
        """
        self.logger.info("Shifting the image")
        set_value = np.median(self.data())
        shifted_data = np.roll(self.data(), x, axis=1)
        if x < 0:
            shifted_data[:, x:] = set_value
        elif x > 0:
            shifted_data[:, 0:x] = set_value

        shifted_data = np.roll(shifted_data, y, axis=0)
        if y < 0:
            shifted_data[y:, :] = set_value
        elif y > 0:
            shifted_data[0:y, :] = set_value

        w = WCS(self.pure_header())

        try:
            highest = min(self.data().shape)
            xs = np.random.randint(0, highest, 20)
            ys = np.random.randint(0, highest, 20)

            skys = w.pixel_to_world(xs.tolist(), ys.tolist())
            w = fit_wcs_from_points([xs + x, ys + y], skys)
        except Unsolvable:
            self.logger.info("No WCS found in header")
        except AttributeError as e:
            self.logger.info(e)

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)
        return self.from_data_header(shifted_data, header=temp_header,
                                     output=output, override=override)

    def rotate(self, angle: Union[float, int],
               output: Optional[str] = None, override: bool = False) -> Self:
        """
        Rotates the data of `Fits` object

        Parameters
        ----------
        angle: float, int
            rotation angle (radians)
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.

        Returns
        -------
        Fits
            rotated `Fits` object
        """
        self.logger.info("Rotating the image")
        set_value = np.median(self.data())

        angle_degree = math.degrees(angle)
        data = ndimage.rotate(self.data(), angle_degree, reshape=False, cval=set_value)

        w = WCS(self.pure_header())
        try:
            # cd_matrix = w.wcs.cd
            shape = self.data().shape
            highest = min(self.data().shape)
            xs = np.random.randint(0, highest, 20)
            ys = np.random.randint(0, highest, 20)

            skys = w.pixel_to_world(xs.tolist(), ys.tolist())

            center = np.array(shape) / 2.0
            rotation_matrix = np.array([[np.cos(-angle), -np.sin(-angle)],
                                        [np.sin(-angle), np.cos(-angle)]])
            translated_coords = np.array([xs, ys]) - center[:, np.newaxis]
            new_coords = np.dot(rotation_matrix, translated_coords) + center[:, np.newaxis]
            new_coords = np.round(new_coords).astype(int)
            new_coords[0] = np.clip(new_coords[0], 0, data.shape[0] - 1)
            new_coords[1] = np.clip(new_coords[1], 0, data.shape[1] - 1)

            w = fit_wcs_from_points([new_coords[0], new_coords[1]], skys)

        except Unsolvable:
            self.logger.info("No WCS found in header")
        except AttributeError as e:
            self.logger.info(e)

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)
        return self.__class__.from_data_header(data, header=temp_header, output=output, override=override)

    def crop(self, x: int, y: int, width: int, height: int,
             output: Optional[str] = None, override: bool = False) -> Self:
        """
        Crop the data of `Fits` object

        Parameters
        ----------
        x: int
            x coordinate of top left
        y: int
            y coordinate of top left
        width: int
            Width of the cropped image
        height: int
            Height of the cropped image
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.

        Returns
        -------
        Fits
            cropped `Fits` object

        Raises
        ------
        IndexError
            when the data is empty after cropping
        """
        self.logger.info("Cropping the image")

        data = self.data()[y:y + height, x:x + width]

        w = WCS(self.pure_header())

        if data.size == 0:
            raise IndexError("Out of boundaries")

        try:
            w = w[y:y + height, x:x + width]
        except Unsolvable:
            self.logger.info("No WCS found in header")
        except AttributeError as e:
            self.logger.info(e)

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)
        return self.__class__.from_data_header(data, header=temp_header, output=output, override=override)

    def bin(self, binning_factor: Union[int, List[int]], func: Callable[[Any], float] = np.mean,
            output: Optional[str] = None, override: bool = False) -> Self:
        """
        Bin the data of `Fits` object

        Parameters
        ----------
        binning_factor: Union[int, List[int]]
            binning factor
        func: Callable[[Any], float], default `np.mean`
            the function to be used on merge
        output: str, optional
            Path of the new fits file.
        override: bool, default=False
            If True will overwrite the output if a file is already exists.

        Returns
        -------
        Fits
            binned `Fits` object

        Raises
        ------
        ValueError
            when the `binning_factor` is wrong
        ValueError
            when the `binning_factor` is big
        """
        self.logger.info("Binning the image")
        if isinstance(binning_factor, int):
            binning_factor_to_use = [binning_factor] * 2
        else:
            if len(binning_factor) != 2:
                raise ValueError("Binning Factor must be a list of 2 integers")
            binning_factor_to_use = binning_factor
        try:
            binned_data = block_reduce(self.data(), tuple(binning_factor_to_use), func=func)
            w = WCS(self.pure_header())
        except ValueError:
            raise ValueError("Big value")

        try:
            highest = min(self.data().shape)
            xs = np.random.randint(0, highest, 20)
            ys = np.random.randint(0, highest, 20)

            skys = w.pixel_to_world(xs.tolist(), ys.tolist())

            new_coords = [
                xs // binning_factor_to_use[0],
                ys // binning_factor_to_use[1]
            ]

            w = fit_wcs_from_points([new_coords[0], new_coords[1]], skys)
        except Unsolvable:
            self.logger.info("No WCS found in header")
        except AttributeError as e:
            self.logger.info(e)

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)
        return self.__class__.from_data_header(binned_data, header=temp_header, output=output, override=override)

    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> pd.DataFrame:
        """
        Calculate Sky Coordinate of given Pixel

        Parameters
        ----------
        xs: Union[List[Union[int, float]], int, float]
            x coordinate(s) of pixel
        ys: Union[List[Union[int, float]], int, float]
            y coordinate(s) of pixel

        Returns
        -------
        pd.DataFrame
            Dataa frame of pixel and sky coordinates

        Raises
        ------
        ValueError
            when the length of xs and ys is not equal
        Unsolvable
            when header does not contain WCS solution

        """
        self.logger.info("Calculating pixels to skys")

        xs_to_use = xs if isinstance(xs, list) else [xs]
        ys_to_use = ys if isinstance(ys, list) else [ys]

        if len(xs_to_use) != len(ys_to_use):
            raise ValueError("xs and ys must be equal in length")

        data = []

        w = WCS(self.pure_header())

        for x, y in zip(xs_to_use, ys_to_use):
            sky = w.pixel_to_world(x, y)
            if not isinstance(sky, SkyCoord):
                raise Unsolvable("Plate is not solved")

            data.append([abs(self), x, y, sky])

        return pd.DataFrame(
            data,
            columns=["image", "xcentroid", "ycentroid", "sky"]
        ).set_index("image")

    def skys_to_pixels(self, skys: Union[List[SkyCoord], SkyCoord]) -> pd.DataFrame:
        """
        Calculate Pixel Coordinate of given Sky

        Parameters
        ----------
        skys: Union[List[SkyCoord], SkyCoord]
            x coordinate(s) of pixel

        Returns
        -------
        pd.DataFrame
            Dataa frame of pixel and sky coordinates

        Raises
        ------
        Unsolvable
            when header does not contain WCS solution

        """
        self.logger.info("Calculating skys to pixels")

        skys_to_use = skys if isinstance(skys, list) else [skys]

        data = []

        w = WCS(self.pure_header())

        for sky in skys_to_use:
            try:
                pixels = w.world_to_pixel(sky)
            except ValueError:
                raise Unsolvable("Plate is not solved")
            if np.isnan(pixels).any():
                raise Unsolvable("Plate is not solved")

            data.append([abs(self), sky, float(pixels[0]), float(pixels[1])])

        return pd.DataFrame(
            data,
            columns=["image", "sky", "xcentroid", "ycentroid"]
        ).set_index("image")

    def map_to_sky(self):
        """
        Returns sources on the image from Simbad

        Returns
        -------
        pd.DataFrame
            Dataa frame of names, pixel, and sky coordinates

        Raises
        ------
        Unsolvable
            when header does not contain WCS solution

        """
        header = self.pure_header()
        nx = header["NAXIS1"]
        ny = header["NAXIS2"]
        polygon = self.pixels_to_skys([0, 0, nx, nx], [0, ny, ny, 0])
        polygon_sstr = ", ".join(
            [f"{round(each.ra.deg, 1)}, {round(each.dec.deg, 1)}" for each in polygon.sky.to_list()])

        query = f"SELECT main_id, ra, dec FROM basic WHERE 1 = CONTAINS(POINT('ICRS', ra, dec), POLYGON('ICRS', {polygon_sstr}))"
        results = Simbad.query_tap(query)
        data: Dict[str, List[Any]] = {
            "name": [],
            "sky": [],
            "xcentroid": [],
            "ycentroid": [],
        }
        for each in results.to_pandas().to_numpy():
            sky = SkyCoord(each[1], each[2], unit="deg")
            x, y = self.skys_to_pixels(sky)[["xcentroid", "ycentroid"]].iloc[0].to_list()
            if x < 0 or y < 0 or x > nx or y > ny:
                continue
            data["name"].append(each[0])
            data["sky"].append(sky)
            data["xcentroid"].append(x)
            data["ycentroid"].append(y)

        return pd.DataFrame(data)
