import itertools
import math
from copy import copy
from logging import Logger, getLogger
from pathlib import Path

from typing import Optional, Dict, Any, Union, List, Literal, Tuple, Callable
from typing_extensions import Self

import numpy as np
from scipy import ndimage

from matplotlib import pyplot as plt
from mpl_point_clicker import clicker

import astroalign

from astropy.coordinates import SkyCoord
from astropy import units
from astropy.units import Quantity
from astropy.visualization import ZScaleInterval
from astropy.stats import sigma_clipped_stats
from astropy.table import QTable, vstack
from astropy.wcs import WCS
from astropy.wcs.utils import fit_wcs_from_points
from astropy.io import fits as fts
from astropy.io.fits import Header
from astropy.nddata import CCDData, block_reduce

from sep import extract as sep_extract, Background, sum_circle

from ccdproc import cosmicray_lacosmic, subtract_bias, subtract_dark, flat_correct

from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture, aperture_photometry
from photutils.utils import calc_total_error

from myraflib.data_model import Data
from myraflib.error import NothingToDo, OperatorError, NumberOfElementError, Unsolvable, AlignError, OverCorrection, \
    CardNotFound
from myraflib.utils import Fixer, NUMERIC, HEADER_ANY, NUMERICS


class Fits(Data):
    ZMag = 25

    def __init__(self, path: Path, logger: Optional[Logger] = None) -> None:

        if logger is None:
            self.logger = getLogger(__file__)
        else:
            self.logger = logger

        if not path.exists():
            self.logger.error("File does not exist")
            raise FileNotFoundError("File does not exist")

        self.is_temp = False
        self.path = path
        self.hdu = fts.open(self.path.absolute(), mode="update")

        if self.data.ndim != 2:
            self.logger.error("Data must be 2D")
            raise ValueError("Data must be 2D")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.path})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.from_path({self.path.absolute()})"

    def __del__(self):
        try:
            if self.is_temp:
                if self.path.exists():
                    self.path.unlink()
        except Exception as e:
            self.logger.warning(e)

    def __abs__(self) -> Self:
        return self.abs()

    def __add__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.add(other)

    def __iadd__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.add(other)

    def __sub__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.sub(other)

    def __isub__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.sub(other)

    def __mul__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.mul(other)

    def __imul__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.mul(other)

    def __truediv__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.div(other)

    def __idiv__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.div(other)

    def __pow__(self, power: Union[Self, NUMERIC], modulo=None) -> Self:
        return self.pow(power)

    def __ipow__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.pow(other)

    def __mod__(self, other: Union[Self, NUMERIC], modulo=None) -> Self:
        return self.mod(other)

    def __imod__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.mod(other)

    def __eq__(self, other: Self) -> bool:
        return self.is_same(other)

    def __ne__(self, other: Self) -> bool:
        return not self.is_same(other)

    def __neg__(self) -> Self:
        return self.mul(-1)

    def __pos__(self) -> Self:
        return self

    def flux_to_mag(self, flux: Union[int, float],
                    flux_error: Union[int, float],
                    exptime: Union[int, float]
                    ) -> Tuple[Union[int, float], Union[int, float]]:
        self.logger.info("Converting flux to mag")
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

    @property
    def file(self) -> str:
        self.logger.info("Getting file path")
        return self.path.absolute().__str__()

    @classmethod
    def from_data_header(cls, data: np.ndarray, header: Optional[Header] = None,
                         output: Optional[str] = None, override: bool = False) -> Self:
        new_output = Fixer.output(output=output, override=override)
        fts.writeto(new_output, data, header=header, output_verify="silentfix")
        fits = cls.from_path(new_output)

        fits.is_temp = output is None
        return fits

    @classmethod
    def from_path(cls, path: str) -> Self:
        return cls(Path(path))

    @classmethod
    def sample(cls) -> Self:
        file = str(Path(__file__).parent / "sample.fits")
        data = fts.getdata(file)
        header = fts.getheader(file)
        return cls.from_data_header(data, header=header)

    def is_same(self, other: Self) -> bool:
        self.logger.info("Checking if two Fits are the same")
        return np.array_equal(
            self.data, other.data
        )

    @property
    def ccd(self) -> CCDData:
        self.logger.info("Creating CCDData of the fits file")
        return CCDData(self.data, unit="adu")

    @property
    def data(self) -> np.ndarray:
        self.logger.info("Getting data")
        return self.hdu[0].data

    def value(self, x: int, y: int) -> NUMERIC:
        self.logger.info("Getting value from fits file")
        value = float(self.data[x][y])

        if value.is_integer():
            return int(value)

        return value

    @property
    def header(self) -> Dict[str, Any]:
        self.logger.info("Getting header")
        header = self.hdu[0].header
        return {
            card: header[card]
            for card in header
            if card not in ['COMMENT', 'HISTORY']
        }

    @property
    def stats(self) -> Dict[str, Any]:
        self.logger.info("Getting stats")
        data = self.data
        w, h = data.shape
        return {
            "size": data.size,
            "width": w,
            "height": h,
            "min": data.min(),
            "mean": data.mean(),
            "std": data.std(),
            "max": data.max(),
        }

    def background(self) -> Background:
        self.logger.info("Getting background")
        return Background(self.data.astype(float))

    def cosmic_cleaner(self, sigclip: float = 4.5, sigfrac: float = 0.3, objlim: float = 5.0, gain: float = 1.0,
                       readnoise: float = 6.5, satlevel: float = 65535.0, pssl: float = 0.0, niter: int = 4,
                       sepmed: bool = True, cleantype: Literal["median", "medmask", "meanmask", "idw"] = 'meanmask',
                       fsmode: Literal["median", "convolve"] = 'median',
                       psfmodel: Literal["gauss", "moffat", "gaussx", "gaussy"] = 'gauss',
                       psffwhm: float = 2.5, psfsize: int = 7, psfk: np.ndarray = None, psfbeta: float = 4.765,
                       gain_apply: bool = True, output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Cleaning data")

        cleaned_data, _ = cosmicray_lacosmic(
            self.data, sigclip=sigclip, sigfrac=sigfrac, objlim=objlim, gain=gain, readnoise=readnoise,
            satlevel=satlevel, niter=niter, sepmed=sepmed, cleantype=cleantype, fsmode=fsmode, psfmodel=psfmodel,
            psffwhm=psffwhm, psfsize=psfsize, psfk=psfk, psfbeta=psfbeta, gain_apply=gain_apply
        )

        if output is None:
            self.hdu[0].data = cleaned_data.astype(int).value
            self.hdu.flush()
            return self

        return self.from_data_header(cleaned_data.value, header=self.hdu[0].header, output=output, override=override)

    def hedit(self, keys: Union[str, List[str]], values: Optional[Union[HEADER_ANY, List[HEADER_ANY]]] = None,
              comments: Optional[Union[HEADER_ANY, List[HEADER_ANY]]] = None, delete: bool = False,
              value_is_key: bool = False, output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Editing the header")

        header = copy(self.hdu[0].header)

        if delete:
            if isinstance(keys, str):
                keys = [keys]

            for key in keys:
                if key in header:
                    del header[key]
                else:
                    self.logger.warning("Key does not exist")

        else:
            if values is None:
                self.logger.error("Delete is False and Value is not given")
                raise NothingToDo("Delete is False and Value is not given")

            keys_to_use, values_to_use, comment_to_use = Fixer.key_value_pair(keys, values, comments)

            if len(keys_to_use) != len(values_to_use):
                self.logger.error("List of keys and values must be equal in length")
                raise ValueError("List of keys and values must be equal in length")

            for key, value, comment in zip(keys_to_use, values_to_use, comment_to_use):
                if value_is_key:
                    header[key] = header[value]
                else:
                    header[key] = value

                header.comments[key] = comment

        if output is None:
            self.hdu[0].header = header
            self.hdu.flush()
            return self

        return self.from_data_header(self.data, header=header, output=output, override=override)

    def save(self, path: Union[str, Path], overwrite: bool = False) -> Self:
        self.logger.info("Saving the fits file")
        if isinstance(path, str):
            new_path = path
        else:
            new_path = path.absolute().__str__()

        return self.from_data_header(self.data, header=self.hdu[0].header, output=new_path, override=overwrite)

    def abs(self, output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Getting the absolute value of the fits file")
        new_data = abs(self.data)

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def add(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Adding the value to the fits file")
        if isinstance(other, self.__class__):
            new_data = self.data + other.data
        else:
            new_data = self.data + other

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def sub(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Subtracting the value from the fits file")
        if isinstance(other, self.__class__):
            new_data = self.data - other.data
        else:
            new_data = self.data - other

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def mul(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Multiplying the value with the fits file")
        if isinstance(other, self.__class__):
            new_data = self.data * other.data
        else:
            new_data = self.data * other

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def div(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Dividing the value with the fits file")

        if isinstance(other, self.__class__):
            new_data = self.data / other.data
        else:
            new_data = self.data / other

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def pow(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Getting the power of the fits with given value")
        if isinstance(other, self.__class__):
            new_data = self.data ** other.data
        else:
            new_data = self.data ** other

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def mod(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False):
        self.logger.info("Getting the mod of the fits with given value")
        if isinstance(other, self.__class__):
            new_data = self.data % other.data
        else:
            new_data = self.data % other

        if output is None:
            self.hdu[0].data = new_data.astype(int)
            self.hdu.flush()
            return self

        return self.from_data_header(new_data.astype(int), header=self.hdu[0].header, output=output, override=override)

    def imarith(self, other: Union[Self, NUMERIC], operator: Literal["+", "-", "*", "/", "**", "^", "%"],
                output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Arithmetic operation")
        if operator == "+":
            return self.add(other, output=output, override=override)
        elif operator == "-":
            return self.sub(other, output=output, override=override)
        elif operator == "*":
            return self.mul(other, output=output, override=override)
        elif operator == "/":
            return self.div(other, output=output, override=override)
        elif operator == "^" or operator == "**":
            return self.pow(other, output=output, override=override)
        elif operator == "%":
            return self.mod(other, output=output, override=override)
        else:
            self.logger.error(f"Unknown operator ({operator})")
            raise OperatorError(f"Unknown operator ({operator})")

    def extract(self, detection_sigma: float = 5.0, min_area: float = 5.0) -> QTable:
        self.logger.info("Extracting sources from fits (sep)")
        bkg = self.background()
        thresh = detection_sigma * bkg.globalrms
        sources = sep_extract(self.data - bkg.back(), thresh, minarea=min_area)
        sources.sort(order="flux")

        if len(sources) < 0:
            self.logger.error("No source was found")
            raise NumberOfElementError("No source was found")

        table = QTable(sources)[["x", "y"]]
        table['x'].unit = units.pix
        table['y'].unit = units.pix
        return table

    def daofind(self, sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> QTable:
        self.logger.info("Extracting sources from fits (daofind)")
        mean, median, std = sigma_clipped_stats(self.data, sigma=sigma)
        daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold * std)
        sources = daofind(self.data - median)

        if len(sources) < 0:
            self.logger.error("No source was found")
            raise NumberOfElementError("No source was found")

        table = QTable(sources)[["xcentroid", "ycentroid"]]

        table.rename_column('xcentroid', 'x')
        table.rename_column('ycentroid', 'y')

        table['x'].unit = units.pix
        table['y'].unit = units.pix

        return table

    def align(self, reference: Self, max_control_points: int = 50, detection_sigma: float = 5.0, min_area: int = 5,
              output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Aligning the fits with given fits")

        try:
            data = self.data.astype(float)
            reference_data = reference.data.astype(float)
            w = WCS(self.hdu[0].header)

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

            if output is None:
                self.hdu[0].data = registered_image.astype(int)
                self.hdu.header = temp_header
                self.hdu.flush()
                return self

            return self.from_data_header(registered_image.astype(int), header=temp_header,
                                         output=output, override=override)


        except Exception as e:
            print(e)
            self.logger.error("Cannot align two images")
            raise AlignError("Cannot align two images")

    def show(self, ax: plt.Axes = None, sources: QTable = None, scale: bool = True) -> None:
        self.logger.info("Showing fits")

        zscale = ZScaleInterval() if scale else lambda x: x

        if ax is not None:
            ax.imshow(zscale(self.data), cmap="Greys_r")
            return

        plt.imshow(zscale(self.data), cmap="Greys_r")

        if sources is not None:
            plt.scatter(sources["x"].value, sources["y"].value)

        plt.xticks([])
        plt.yticks([])
        plt.show()

    def solve_field(self, api_key: str, output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Solving plate")
        if output is None:
            return self

        return self.save(output, overwrite=override)

    def coordinate_picker(self, scale: bool = True) -> QTable:
        self.logger.info("Coordinate picker")
        zscale = ZScaleInterval() if scale else lambda x: x

        fig, ax = plt.subplots(constrained_layout=True)

        ax.imshow(zscale(self.data), cmap="Greys_r")
        klkr = clicker(ax, ["source"], markers=["o"])
        plt.show()

        if len(klkr.get_positions()["source"]) == 0:
            empty_table = QTable()
            empty_table['x'] = Quantity([], unit='pix')  # An empty column with unit meters
            empty_table['y'] = Quantity([], unit='pix')  # An empty column with unit seconds
            return empty_table

        return QTable(
            Quantity(klkr.get_positions()["source"], unit='pix'),
            names=["x", "y"]
        )

    def shift(self, x: NUMERIC, y: NUMERIC, output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Shifting fits")
        fill_val = np.median(self.data)
        shifted_data = np.roll(self.data, x, axis=1)
        if x < 0:
            shifted_data[:, x:] = fill_val
        elif x > 0:
            shifted_data[:, 0:x] = fill_val

        shifted_data = np.roll(shifted_data, y, axis=0)
        if y < 0:
            shifted_data[y:, :] = fill_val
        elif y > 0:
            shifted_data[0:y, :] = fill_val

        w = WCS(self.hdu[0].header)

        try:
            highest = min(self.data.shape)
            xs = np.random.randint(0, highest, 20)
            ys = np.random.randint(0, highest, 20)

            skys = w.pixel_to_world(xs.tolist(), ys.tolist())
            w = fit_wcs_from_points([xs + x, ys + y], skys)
        except:
            self.logger.error("No WCS found in header")
            raise Unsolvable("No WCS found in header")

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)

        if output is None:
            self.hdu[0].data = shifted_data.astype(int)
            self.hdu[0].header = temp_header
            self.hdu.flush()
            return self

        return self.from_data_header(shifted_data.astype(int), header=temp_header, output=output, override=override)

    def rotate(self, angle: NUMERIC, output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Rotating fits")
        fill_val = np.median(self.data)
        angle_degree = angle * 180 / math.pi
        rotated_data = ndimage.rotate(self.data, angle_degree, reshape=False, cval=fill_val)

        w = WCS(self.hdu[0].header)
        try:
            # cd_matrix = w.wcs.cd
            shape = self.data.shape
            highest = min(self.data.shape)
            xs = np.random.randint(0, highest, 20)
            ys = np.random.randint(0, highest, 20)

            skys = w.pixel_to_world(xs.tolist(), ys.tolist())

            center = np.array(shape) / 2.0
            rotation_matrix = np.array([[np.cos(-angle), -np.sin(-angle)],
                                        [np.sin(-angle), np.cos(-angle)]])
            translated_coords = np.array([xs, ys]) - center[:, np.newaxis]
            new_coords = np.dot(rotation_matrix, translated_coords) + center[:, np.newaxis]
            new_coords = np.round(new_coords).astype(int)
            new_coords[0] = np.clip(new_coords[0], 0, rotated_data.shape[0] - 1)
            new_coords[1] = np.clip(new_coords[1], 0, rotated_data.shape[1] - 1)

            w = fit_wcs_from_points([new_coords[0], new_coords[1]], skys)

        except:
            self.logger.error("No WCS found in header")
            raise Unsolvable("No WCS found in header")

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)

        if output is None:
            self.hdu[0].data = rotated_data.astype(int)
            self.hdu[0].header = temp_header
            self.hdu.flush()
            return self

        return self.from_data_header(rotated_data.astype(int), header=temp_header, output=output, override=override)

    def crop(self, x: int, y: int, width: int, height: int, output: Optional[str] = None,
             override: bool = False) -> Self:
        self.logger.info("Cropping fits")
        print(y, y + height, x, x + width)
        cropped_data = self.data[y:y + height, x:x + width]

        w = WCS(self.hdu[0].header)

        if cropped_data.size == 0:
            self.logger.error("Out of boundaries")
            raise IndexError("Out of boundaries")

        try:
            w = w[y:y + height, x:x + width]
        except:
            self.logger.error("No WCS found in header")
            raise Unsolvable("No WCS found in header")

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)

        if output is None:
            self.hdu[0].data = cropped_data.astype(int)
            self.hdu[0].header = temp_header
            self.hdu.flush()
            return self

        return self.from_data_header(cropped_data.astype(int), header=temp_header, output=output, override=override)

    def bin(self, binning_factor: Union[int, Tuple[int, int]], func: Callable[..., float] = np.mean,
            output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Binning fits")

        if isinstance(binning_factor, int):
            binning_factor_to_use = [binning_factor] * 2
        else:
            if len(binning_factor) != 2:
                self.logger.error("Binning Factor must be a list of 2 integers")
                raise ValueError("Binning Factor must be a list of 2 integers")
            binning_factor_to_use = binning_factor
        try:
            binned_data = block_reduce(self.data, tuple(binning_factor_to_use), func=func)
            w = WCS(self.hdu[0].header)
        except ValueError:
            self.logger.error("Bad value")
            raise ValueError("Bad value")

        try:
            highest = min(self.data.shape)
            xs = np.random.randint(0, highest, 20)
            ys = np.random.randint(0, highest, 20)

            skys = w.pixel_to_world(xs.tolist(), ys.tolist())

            new_coords = [
                xs // binning_factor_to_use[0],
                ys // binning_factor_to_use[1]
            ]

            w = fit_wcs_from_points([new_coords[0], new_coords[1]], skys)
        except:
            self.logger.error("No WCS found in header")
            raise Unsolvable("No WCS found in header")

        temp_header = Header()
        # temp_header.extend(self.pure_header(), unique=True, update=True)
        temp_header.extend(w.to_header(), unique=True, update=True)

        if output is None:
            self.hdu[0].data = binned_data.astype(int)
            self.hdu[0].header = temp_header
            self.hdu.flush()
            return self

        return self.from_data_header(binned_data.astype(int), header=temp_header, output=output, override=override)

    def zero_correction(self, master_zero: Self, force: bool = False,
                        output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Zero correction")

        if "MY-ZERO" not in self.hdu[0].header or force:
            zero_corrected = subtract_bias(self.ccd, master_zero.ccd).data.astype(int)
            header = self.hdu[0].header
            header["MY-ZERO"] = master_zero.path.absolute().__str__()

            if output is None:
                self.hdu[0].data = zero_corrected
                self.hdu[0].header = header
                self.hdu.flush()
                return self

            return self.from_data_header(zero_corrected, header=header, output=output, override=override)

        self.logger.error("This Data is already zero corrected")
        raise OverCorrection("This Data is already zero corrected")

    def dark_correction(self, master_dark: Self, exposure: Optional[str] = None, force: bool = False,
                        output: Optional[str] = None, override: bool = False) -> Self:
        self.logger.info("Dark correction")

        if "MY-DARK" not in self.hdu[0].header or force:
            if exposure is None:
                options = {"dark_exposure": 1 * units.s,
                           "data_exposure": 1 * units.s}
            else:
                if exposure not in self.hdu[0].header or exposure not in master_dark.header():
                    raise CardNotFound(f"Key {exposure} not found in file, master_dark or both")

                options = {
                    "dark_exposure": float(
                        float(master_dark.header()[exposure].values[0])) * units.s,
                    "data_exposure": float(
                        float(self.hdu[0].header[exposure].values[0])) * units.s
                }

            dark_corrected = subtract_dark(
                self.ccd, master_dark.ccd,
                **options, scale=True
            )
            header = self.hdu[0].header
            header["MY-DARK"] = master_dark.path.absolute().__str__()

            if output is None:
                self.hdu[0].data = dark_corrected.data.astype(int)
                self.hdu[0].header = header
                self.hdu.flush()
                return self

            return self.__class__.from_data_header(dark_corrected.data.astype(int), header=header,
                                                   output=output, override=override)

        self.logger.error("This Data is already dark corrected")
        raise OverCorrection("This Data is already dark corrected")

    def flat_correction(self, master_flat: Self, force: bool = False, output: Optional[str] = None,
                        override: bool = False) -> Self:
        self.logger.info("Flat correction")

        if "MY-FLAT" not in self.hdu[0].header or force:
            flat_corrected = flat_correct(self.ccd, master_flat.ccd)
            header = self.hdu[0].header
            header["MY-FLAT"] = master_flat.path.absolute().__str__()

            if output is None:
                self.hdu[0].data = flat_corrected.data.astype(int)
                self.hdu[0].header = header
                self.hdu.flush()
                return self

            return self.__class__.from_data_header(flat_corrected.data.data.astype(int), header=header,
                                                   output=output, override=override)

        self.logger.error("This Data is already flat corrected")
        raise OverCorrection("This Data is already flat corrected")

    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> QTable:
        self.logger.info("Pixels to Skys")

        xs_to_use = xs if isinstance(xs, list) else [xs]
        ys_to_use = ys if isinstance(ys, list) else [ys]

        if len(xs_to_use) != len(ys_to_use):
            self.logger.error("xs and ys must be equal in length")
            raise ValueError("xs and ys must be equal in length")

        data = []

        w = WCS(self.hdu[0].header)

        for x, y in zip(xs_to_use, ys_to_use):
            sky = w.pixel_to_world(x, y)
            if not isinstance(sky, SkyCoord):
                self.logger.error("Plate is not solved")
                raise Unsolvable("Plate is not solved")

            data.append([x * units.pix, y * units.pix, sky.ra, sky.dec])

        return QTable(
            list(map(list, itertools.zip_longest(*data, fillvalue=None))),
            names=["x", "y", "ra", "dec"]
        )

    def skys_to_pixels(self, skys: SkyCoord) -> QTable:
        self.logger.info("Skys to Pixels")

        data = []

        w = WCS(self.hdu[0].header)

        for sky in skys:
            try:
                pixels = w.world_to_pixel(sky)
                data.append([sky.ra, sky.dec, float(pixels[0]) * units.pix, float(pixels[1]) * units.pix])
            except ValueError:
                self.logger.error("Plate is not solved")
                raise Unsolvable("Plate is not solved")
            if np.isnan(pixels).any():
                self.logger.error("Plate is not solved")
                raise Unsolvable("Plate is not solved")

        return QTable(
            list(map(list, itertools.zip_longest(*data, fillvalue=None))),
            names=["ra", "dec", "x", "y"]
        )

    def photometry_sep(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                       headers: Optional[Union[str, List[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None) -> QTable:
        self.logger.info("Photometry sep")

        table = []

        the_header = self.header

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
                headers_.append(the_header[new_header])
            except KeyError:
                self.logger.warning("Couldn't find header key")
                headers_.append(None)

        data = self.data.astype(float)
        background = self.background()

        clean_d = data - background.rms()
        error = calc_total_error(
            data, background, exposure_to_use
        )
        for new_r in new_rs:
            fluxes, flux_errs, flags = sum_circle(data, new_xs, new_ys, new_r, err=error)

            for x, y, flux, flux_err, flag in zip(new_xs, new_ys, fluxes,
                                                  flux_errs, flags):
                try:
                    sky = self.pixels_to_skys(x, y).iloc[0].sky
                    ra, dec = sky.ra, sky.dec
                except Exception as e:
                    self.logger.warning(f"Could not get ra, dec. {e}")
                    ra, dec = None, None

                value = clean_d[int(x)][int(y)]
                snr = np.nan if value < 0 else math.sqrt(value)
                mag, mag_err = self.flux_to_mag(flux, flux_err,
                                                exposure_to_use)
                table.append(
                    [
                        self.file, "sep", x * units.pix, y * units.pix, ra, dec,
                                          new_r * units.pix, flux * units.adu,
                                          flux_err * units.adu, flag, snr, mag * units.mag,
                                          mag_err * units.mag, *headers_
                    ]
                )
        return QTable(
            list(map(list, itertools.zip_longest(*table, fillvalue=None))),
            names=["image", "package", "x", "y", "ra", "dec", "aperture", "flux",
                   "flux_error", "flag", "snr", "mag", "merr", *keys_]
        )

    def photometry_phu(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                       headers: Optional[Union[str, List[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None) -> QTable:
        self.logger.info("Photometry photutils")

        table = []

        the_header = self.header
        data = self.data.astype(float)

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
                headers_.append(the_header[new_header])
            except KeyError:
                self.logger.warning("Couldn't find header key")
                headers_.append(None)

        background = self.background()

        clean_d = data - background.rms()

        for new_r in new_rs:
            apertures = CircularAperture([
                [new_x, new_y] for new_x, new_y in zip(new_xs, new_ys)
            ], r=new_r)
            error = calc_total_error(
                data, self.background(), exposure_to_use
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
                    ra, dec = sky.ra, sky.dec
                except Exception as e:
                    self.logger.warning(f"Could not get ra, dec. {e}")
                    ra, dec = None, None

                table.append(
                    [
                        self.file, "phu",
                        phot_line["xcenter"].value * units.pix, phot_line["ycenter"].value * units.pix,
                        ra, dec, new_r * units.pix,
                        phot_line["aperture_sum"] * units.adu, phot_line["aperture_sum_err"] * units.adu,
                        np.nan, snr, mag * units.mag, mag_err * units.mag, *headers_]
                )

        return QTable(
            list(map(list, itertools.zip_longest(*table, fillvalue=None))),
            names=["image", "package", "x", "y", "ra", "dec", "aperture",
                   "flux", "flux_error", "flag", "snr", "mag", "merr", *keys_]
        )

    def photometry(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                   headers: Optional[Union[str, List[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> QTable:
        self.logger.info("Photometry")
        table_sep = self.photometry_sep(xs, ys, rs, headers=headers, exposure=exposure)
        table_phu = self.photometry_phu(xs, ys, rs, headers=headers, exposure=exposure)
        return vstack([table_sep, table_phu])
