import itertools
import math
from glob import glob
from logging import Logger, getLogger
from pathlib import Path
from random import randint
from typing import List, Union, Optional, Iterator, Literal, Callable, Tuple, Dict, Any

import numpy as np
from astropy import units
from astropy.coordinates import SkyCoord
from astropy.nddata import CCDData
from astropy.table import QTable, vstack
from astropy.units import Quantity
from astropy.visualization import ZScaleInterval
from ccdproc import Combiner
from matplotlib import pyplot as plt, animation
from sep import Background
from typing_extensions import Self

from .error import NumberOfElementError, OverCorrection
from .fits import Fits
from .dataarray_model import DataArray
from .utils import HEADER_ANY, NUMERIC, NUMERICS


def empty_phot():
    empty_table = QTable()
    empty_table['image'] = []
    empty_table['package'] = []
    empty_table['x'] = Quantity([], unit='pix')
    empty_table['y'] = Quantity([], unit='pix')
    empty_table['ra'] = Quantity([], unit='deg')
    empty_table['dec'] = Quantity([], unit='deg')
    empty_table['aperture'] = Quantity([], unit='pix')
    empty_table['flux'] = Quantity([], unit='adu')
    empty_table['flux_error'] = Quantity([], unit='adu')
    empty_table['flag'] = []
    empty_table['snr'] = []
    empty_table['mag'] = Quantity([], unit='mag')
    empty_table['merr'] = Quantity([], unit='mag')

    return empty_table


class FitsArray(DataArray):
    def __init__(self, fitses: List[Fits], logger: Optional[Logger] = None):
        if logger is None:
            self.logger = getLogger(__file__)
        else:
            self.logger = logger

        if len(fitses) == 0:
            self.logger.error("No Fits object was given")
            raise NumberOfElementError("No Fits object was given")

        self.fitses: List[Fits] = fitses

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(nof:{len(self)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.from_paths({self.fitses.__str__()}))"

    def __len__(self) -> int:
        return len(self.fitses)

    def __iter__(self) -> Iterator[Fits]:
        for fits in self.fitses:
            yield fits

    def __getitem__(self, key: Union[int, slice]) -> Union[Fits, Self]:

        if isinstance(key, int):
            return self.fitses[key]
        elif isinstance(key, slice):
            return self.__class__(self.fitses[key])

        self.logger.error("Wrong slice")
        raise ValueError("Wrong slice")

    def __abs__(self) -> Self:
        return self.abs()

    def __add__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.add(other)

    def __radd__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.add(other)

    def __sub__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.sub(other)

    def __rsub__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.sub(other)

    def __mul__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.mul(other)

    def __rmul__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.mul(other)

    def __truediv__(self, other: Union[Self, NUMERIC]) -> Self:
        return self.div(other)

    def __pow__(self, power: Union[Self, NUMERIC], modulo=None) -> Self:
        return self.pow(power)

    def __mod__(self, other: Union[Self, NUMERIC], modulo=None) -> Self:
        return self.mod(other)

    def __rmod__(self, other: Union[Self, NUMERIC], modulo=None) -> Self:
        return self.mod(other)

    def __neg__(self) -> Self:
        return self.mul(-1)

    def __pos__(self) -> Self:
        return self

    def __contains__(self, item: Fits) -> bool:
        for each in self:
            if each.is_same(item):
                return True

        return False

    def __setitem__(self, key: Union[int, slice], value: Fits) -> None:
        self.fitses[key] = value

    def __delitem__(self, key: Union[int, slice]) -> None:
        del self.fitses[key]

    @classmethod
    def from_paths(cls, paths: List[str]) -> Self:
        files = []
        for each in map(Path, paths):
            try:
                files.append(Fits(each))
            except FileNotFoundError:
                pass

        return cls(files)

    def __weight_corrector(self, weights: Optional[Union[List[str], List[Union[float, int]]]] = None):
        self.logger.info("Checking weights...")
        if weights is None:
            weights_to_use = [1] * len(self)
        else:
            weights_to_use = weights

        if isinstance(weights, List):
            the_weights = weights_to_use
        else:
            the_weights = [weights_to_use]

        if len(the_weights) != len(self):
            self.logger.error("The length of the weights is not equal to the number of fits objects")
            raise ValueError("The length of the weights is not equal to the number of fits objects")

        return the_weights

    @classmethod
    def from_pattern(cls, pattern: str) -> Self:
        return cls.from_paths(glob(pattern))

    @classmethod
    def sample(cls, n=10) -> Self:
        fitses = []
        for i in range(n):
            file = Fits.sample()
            file.shift(randint(i, 2 * i), randint(i, 2 * i)).rotate(math.radians(randint(i, 2 * i) / 10))
            fitses.append(file)

        return cls(fitses)

    def merge(self, other: Self) -> Self:
        self.logger.info(f"Merging two FitsArrays")
        self.fitses.extend(other.fitses)
        return self

    def append(self, other: Fits) -> Self:
        self.logger.info("Appending Fits to FitsArray")
        self.fitses.append(other)
        return self

    @property
    def header(self) -> QTable:
        self.logger.info("Getting fits header")
        headers = []
        for each in self:
            try:
                header = {
                    "image": each.path.absolute().__str__()
                }
                header.update(each.header)

                headers.append(header)
            except Exception as e:
                self.logger.warning(e)

        if len(headers) == 0:
            self.logger.error("Couldn't get any fits header")
            raise NumberOfElementError("Couldn't get any fits header")

        return QTable(
            [
                each
                for each in headers
            ]
        )

    @property
    def data(self) -> Iterator[np.ndarray]:
        self.logger.info("Getting fits data")
        for each in self:
            try:
                yield each.data
            except Exception as e:
                self.logger.warning(e)

    @property
    def ccd(self) -> Iterator[CCDData]:
        self.logger.info("Getting fitses CCDData")
        for each in self:
            try:
                yield each.ccd
            except Exception as e:
                self.logger.warning(e)

    def value(self, x: int, y: int) -> QTable:
        self.logger.info("Getting fitses value")
        values = []
        for each in self:
            try:
                values.append([each.path.absolute().__str__(), x, y, each.value(x, y)])
            except Exception as e:
                self.logger.warning(e)

        if len(values) == 0:
            self.logger.error("Couldn't get value for any of fits")
            raise NumberOfElementError("Couldn't get value for any of fits")

        return QTable(
            list(map(list, itertools.zip_longest(*values, fillvalue=None))),
            names=["image", "x", "y", "value"]
        )

    @property
    def files(self) -> List[str]:
        self.logger.info("Getting fits files")
        files = []
        for each in self:
            try:
                files.append(each.file)
            except Exception as e:
                self.logger.warning(e)

        if len(files) == 0:
            self.logger.error("Couldn't get files for any of fits")
            raise NumberOfElementError("Couldn't get path for any of fits")

        return files

    @property
    def stats(self) -> QTable:
        self.logger.info("Getting fits stats")
        stats = []
        for each in self:
            line = []
            try:
                line.append(each.path.absolute().__str__())
                line.extend(list(each.stats.values()))
                stats.append(line)
            except Exception as e:
                self.logger.warning(e)

        if len(stats) == 0:
            self.logger.error("Couldn't get stats for any of fits")
            raise NumberOfElementError("Couldn't get stats for any of fits")

        return QTable(
            list(map(list, itertools.zip_longest(*stats, fillvalue=None))),
            names=["image", "size", "width", "height", "min", "mean", "std", "max"]
        )

    def background(self) -> Iterator[Background]:
        self.logger.info("Getting background of fitses")
        for each in self:
            try:
                yield each.background()
            except Exception as e:
                self.logger.warning(e)

    def cosmic_cleaner(self, sigclip: float = 4.5, sigfrac: float = 0.3, objlim: float = 5.0, gain: float = 1.0,
                       readnoise: float = 6.5, satlevel: float = 65535.0, pssl: float = 0.0, niter: int = 4,
                       sepmed: bool = True, cleantype: Literal["median", "medmask", "meanmask", "idw"] = 'meanmask',
                       fsmode: Literal["median", "convolve"] = 'median',
                       psfmodel: Literal["gauss", "moffat", "gaussx", "gaussy"] = 'gauss',
                       psffwhm: float = 2.5, psfsize: int = 7, psfk: np.ndarray = None, psfbeta: float = 4.765,
                       gain_apply: bool = True) -> Self:
        self.logger.info("Cleaning fitses")
        for each in self:
            try:
                _ = each.cosmic_cleaner(sigclip=sigclip, sigfrac=sigfrac, objlim=objlim, gain=gain, readnoise=readnoise,
                                        satlevel=satlevel, pssl=pssl, niter=niter, sepmed=sepmed, cleantype=cleantype,
                                        fsmode=fsmode, psfmodel=psfmodel, psffwhm=psffwhm, psfsize=psfsize, psfk=psfk,
                                        psfbeta=psfbeta, gain_apply=gain_apply)
            except Exception as e:
                self.logger.warning(e)

            return self

    def hedit(self, keys: Union[str, List[str]], values: Optional[Union[HEADER_ANY, List[HEADER_ANY]]] = None,
              delete: bool = False, value_is_key: bool = False) -> Self:
        self.logger.info("Editing the header")

        for each in self:
            _ = each.hedit(keys=keys, values=values, delete=delete, value_is_key=value_is_key)
        return self

    def hselect(self, fields: Union[str, List[str]]) -> QTable:
        self.logger.info("Selecting the header")
        if isinstance(fields, str):
            fields = [fields]

        headers = self.header
        fields_to_use = [field for field in fields if field in headers.columns]

        if len(fields_to_use) == 0:
            empty_table = QTable()
            return empty_table
        fields_to_use.insert(0, "image")
        return self.header[fields_to_use]

    def save(self, path: Union[str, Path], overwrite: bool = False) -> Self:
        self.logger.info("Saving fitses")
        fitses = []
        for each in self:
            try:
                fits = each.save(path=path, overwrite=overwrite)
                fitses.append(fits)
            except Exception as e:
                self.logger.warning(e)

        if len(fitses) == 0:
            self.logger.error("Couldn't save any fits")
            raise NumberOfElementError("Couldn't save any fits")

        return fitses

    def abs(self) -> Self:
        for each in self:
            try:
                _ = each.abs()
            except Exception as e:
                self.logger.warning(e)

        return self

    def add(self, other: Union[Self, Fits, NUMERIC, List[Union[Fits, NUMERIC]]]) -> Self:
        self.logger.info("Adding value to fitses")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.add(other)
            except Exception as e:
                self.logger.warning(e)

        return self

    def sub(self, other: Union[Self, Fits, NUMERIC, List[Union[Fits, NUMERIC]]]) -> Self:
        self.logger.info("Subtracting value from fitses")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.sub(other)
            except Exception as e:
                self.logger.warning(e)

        return self

    def mul(self, other: Union[Self, Fits, NUMERIC, List[Union[Fits, NUMERIC]]]) -> Self:
        self.logger.info("Multiplying value with fitses")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.mul(other)
            except Exception as e:
                self.logger.error(e)

        return self

    def div(self, other: Union[Self, Fits, NUMERIC, List[Union[Fits, NUMERIC]]]) -> Self:
        self.logger.info("Dividing fitses with the value")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.div(other)
            except Exception as e:
                self.logger.warning(e)

        return self

    def pow(self, other: Union[Self, Fits, NUMERIC, List[Union[Fits, NUMERIC]]]) -> Self:
        self.logger.info("Rasing fitses with the value")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.pow(other)
            except Exception as e:
                self.logger.warning(e)

        return self

    def mod(self, other: Union[Self, Fits, NUMERIC, List[Union[Fits, NUMERIC]]]):
        self.logger.info("Calculating mod of fitses with the value")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.mod(other)
            except Exception as e:
                self.logger.warning(e)

        return self

    def imarith(self, other: Union[Self, NUMERIC], operator: Literal["+", "-", "*", "/", "**", "^", "%"]) -> Self:
        self.logger.info("Image arithmetic")
        if isinstance(other, List):
            if len(other) != len(self):
                self.logger.error("Number of other does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of other does not match the number of elements in FitsArray")
            others = other
        else:
            others = [other] * len(self)

        for each, other in zip(self, others):
            try:
                _ = each.imarith(other, operator)
            except Exception as e:
                self.logger.warning(e)

        return self

    def extract(self, index: int = 0, detection_sigma: float = 5.0, min_area: float = 5.0) -> QTable:
        self.logger.info("Extracting sources from fits (sep)")
        if index >= len(self):
            self.logger.error("Index out of range")
            raise IndexError("Index out of range")

        return self[index].extract(detection_sigma=detection_sigma, min_area=min_area)

    def daofind(self, index: int = 0, sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> QTable:
        self.logger.info("Extracting sources from fits (daofind)")
        if index >= len(self):
            self.logger.error("Index out of range")
            raise IndexError("Index out of range")

        return self[index].daofind(sigma=sigma, fwhm=fwhm, threshold=threshold)

    def align(self, reference: Union[Fits, int] = 0, max_control_points: int = 50, min_area: int = 5) -> Self:
        self.logger.info("Aligning fits")
        if isinstance(reference, Fits):
            the_reference = reference
        else:
            the_reference = self[reference]

        for each in self:
            try:
                _ = each.align(the_reference, max_control_points=max_control_points, min_area=min_area)
            except Exception as e:
                self.logger.warning(e)

        return self

    def shift(self, xs: Union[List[int], int], ys: Union[List[int], int]) -> Self:
        self.logger.info("Shifting fitses")

        if type(xs) is not type(ys):
            self.logger.error("xs and ys must be same type")
            raise ValueError("xs and ys must be same type")

        if isinstance(xs, List):
            if len(xs) != len(ys) != len(self):
                self.logger.error("Number of coordinates does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of coordinates does not match the number of elements in FitsArray")
            new_xs = xs
            new_ys = ys
        else:
            new_xs = [xs] * len(self)
            new_ys = [ys] * len(self)

        for each, x, y in zip(self, new_xs, new_ys):
            try:
                _ = each.shift(x, y)
            except Exception as e:
                self.logger.warning(e)

        return self

    def rotate(self, angles: Union[List[NUMERIC], NUMERIC]) -> Self:
        self.logger.info("Rotating fitses")
        if isinstance(angles, List):
            if len(angles) != len(self):
                self.logger.error("Number of angles does not match the number of elements in FitsArray")
                raise NumberOfElementError("Number of angles does not match the number of elements in FitsArray")
            new_angles = angles
        else:
            new_angles = [angles] * len(self)

        for each, angle in zip(self, new_angles):
            try:
                _ = each.rotate(angle)
            except Exception as e:
                self.logger.warning(e)

        return self

    def crop(self, xs: Union[int, List[int]], ys: Union[int, List[int]],
             widths: Union[int, List[int]], heights: Union[int, List[int]]) -> Self:
        self.logger.info("Cropping fitses")
        if type(xs) is not type(ys) is not type(widths) is not type(heights):
            self.logger.error("xs, ys, widths and heights must be same type")
            raise ValueError("xs, ys, widths and heights must be same type")

        if isinstance(xs, List):
            if len(xs) != len(ys) != len(widths) != len(heights) != len(self):
                self.logger.error("Number of coordinates and dimensions does not match the "
                                  "number of elements in FitsArray")
                raise NumberOfElementError("Number of coordinates and dimensions does not match the "
                                           "number of elements in FitsArray")
            new_xs = xs
            new_ys = ys
            new_widths = widths
            new_heights = heights
        else:
            new_xs = [xs] * len(self)
            new_ys = [ys] * len(self)
            new_widths = [widths] * len(self)
            new_heights = [heights] * len(self)

        for each, x, y, w, h in zip(self, new_xs, new_ys, new_widths, new_heights):
            try:
                _ = each.crop(x, y, w, h)
            except Exception as e:
                self.logger.warning(e)

        return self

    def bin(self, binning_factors: Union[Union[int, Tuple[int, int]], List[Union[int, Tuple[int, int]]]],
            func: Callable[..., float] = np.mean) -> Self:
        self.logger.info("Binning fitses")

        if isinstance(binning_factors, List):
            if len(binning_factors) != len(self):
                self.logger.error("Number of binning_factors number of elements in FitsArray")
                raise NumberOfElementError("Number of binning_factors number of elements in FitsArray")
            new_binning_factors = binning_factors
        else:
            new_binning_factors = [binning_factors] * len(self)

        for each, binning_factor in zip(self, new_binning_factors):
            try:
                _ = each.bin(binning_factor)
            except Exception as e:
                self.logger.warning(e)

        return self

    def show(self, points: QTable = None, scale: bool = True, interval: float = 1.0) -> None:
        self.logger.info("Animation fitses")
        fig = plt.figure()

        if scale:
            zscale = ZScaleInterval()
        else:
            def zscale(x):
                return x

        im = plt.imshow(zscale(self[0].data), cmap="Greys_r", animated=True)
        plt.xticks([])
        plt.yticks([])

        def updatefig(args):
            im.set_array(zscale(self[args % len(self)].data))
            return im,

        _ = animation.FuncAnimation(
            fig, updatefig, interval=interval, blit=True,
            cache_frame_data=False
        )
        plt.show()

    def solve_field(self, api_key: str, reference: Union[Fits, int] = 0, solve_timeout: int = 120,
                    force_image_upload: bool = False, max_control_points: int = 50, min_area: int = 5,
                    soft_solve: bool = True) -> Self:
        self.logger.info("Solving plate")

        return self

    def group_by(self, groups: Union[str, List[str]]) -> Dict[Any, Self]:
        self.logger.info("Grouping fitses")
        if isinstance(groups, List):
            the_groups = groups
        else:
            the_groups = [groups]

        if len(the_groups) < 1:
            return dict()

        headers = self.header.to_pandas()

        for group in the_groups:
            if group not in headers.columns:
                headers[group] = np.nan

        grouped = {}
        for keys, df in headers.groupby(groups, dropna=False):
            grouped[keys] = self.__class__.from_paths(df["image"].tolist())

        return grouped

    def combine(self, method: Literal["average", "mean", "median", "sum"] = "average",
                clipping: Literal[None, "sigma", "minmax"] = None,
                weights: Optional[List[Union[float, int]]] = None) -> Fits:
        self.logger.info("Combining fitses")
        if method not in ["average", "mean", "median", "sum"]:
            self.logger.error("Method must be one of average, mean, median, sum")
            raise ValueError("Method must be one of average, mean, median, sum")

        if clipping not in [None, "sigma", "minmax"]:
            self.logger.error("Clipping must be one of None, sigma, minmax")
            raise ValueError("Clipping must be one of None, sigma, minmax")

        combiner = Combiner(self.ccd)

        if weights is None:
            the_weights = [1] * len(self)
        else:
            the_weights = weights

        if len(the_weights) != len(self):
            self.logger.error("Length of weights must be equal to number of Fits")
            raise ValueError("Length of weights must be equal to number of Fits")

        if clipping is not None:
            if "sigma".startswith(clipping):
                combiner.sigma_clipping()
            else:
                combiner.minmax_clipping()

        combiner.weights = np.array(the_weights)

        if "median".startswith(method.lower()):
            the_data = combiner.median_combine().data
        elif "sum".startswith(method.lower()):
            the_data = combiner.sum_combine().data
        else:
            the_data = combiner.average_combine().data

        return Fits.from_data_header(data=the_data)

    def zero_combine(self, method: Literal["average", "mean", "median"] = "median",
                     clipping: Literal[None, "sigma", "minmax"] = None) -> Fits:
        self.logger.info("Zero combining fitses")
        return self.combine(method=method, clipping=clipping)

    def dark_combine(self, method: Literal["average", "mean", "median"] = "median",
                     clipping: Literal[None, "sigma", "minmax"] = None,
                     weights: Optional[Union[List[str], List[Union[float, int]]]] = None) -> Fits:
        self.logger.error("Dark combining fitses")

        the_weights = self.__weight_corrector(weights)
        return self.combine(method=method, clipping=clipping, weights=the_weights)

    def flat_combine(self, method: Literal["average", "mean", "median"] = "median",
                     clipping: Literal[None, "sigma", "minmax"] = None,
                     weights: Optional[Union[List[str], List[Union[float, int]]]] = None) -> Fits:
        self.logger.error("Flat combining fitses")

        the_weights = self.__weight_corrector(weights)
        return self.combine(method=method, clipping=clipping, weights=the_weights)

    def zero_correction(self, master_zero: Self, force: bool = False) -> Self:
        self.logger.info("Zero correction")
        fits_array = []
        for fits in self:
            try:
                zero_corrected = fits.zero_correction(master_zero, force=force)
                fits_array.append(zero_corrected)
            except OverCorrection:
                fits_array.append(fits)
            except Exception as error:
                self.logger.warning(error)

        return self.__class__(fits_array)

    def dark_correction(self, master_dark: Self, exposure: Optional[str] = None, force: bool = False) -> Self:
        self.logger.info("Dark correction")
        fits_array = []
        for fits in self:
            try:
                dark_corrected = fits.dark_correction(master_dark, exposure=exposure, force=force)
                fits_array.append(dark_corrected)
            except OverCorrection:
                fits_array.append(fits)
            except Exception as error:
                self.logger.warning(error)

        return self.__class__(fits_array)

    def flat_correction(self, master_flat: Self, exposure: Optional[str] = None, force: bool = False) -> Self:
        self.logger.info("Flat correction")
        fits_array = []
        for fits in self:
            try:
                dark_corrected = fits.flat_correction(master_flat, force=force)
                fits_array.append(dark_corrected)
            except OverCorrection:
                fits_array.append(fits)
            except Exception as error:
                self.logger.warning(error)

        return self.__class__(fits_array)

    def photometry_sep(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                       headers: Optional[Union[str, List[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None) -> QTable:
        self.logger.info("Photometry sep")
        photometry = []
        for fits in self:
            try:
                phot = fits.photometry_sep(xs, ys, rs, headers=headers, exposure=exposure)
                photometry.append(phot)
            except NumberOfElementError:
                self.logger.error("The length of Xs and Ys must be equal")
                raise NumberOfElementError("The length of Xs and Ys must be equal")
            except Exception as error:
                self.logger.warning(error)

        if len(photometry) == 0:
            self.logger.warning("Couldn't do photometry")
            raise NumberOfElementError("Couldn't do photometry")

        return vstack(photometry)

    def photometry_phu(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                       headers: Optional[Union[str, List[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None) -> QTable:
        self.logger.info("Photometry photutils")
        photometry = []
        for fits in self:
            try:
                phot = fits.photometry_phu(xs, ys, rs, headers=headers, exposure=exposure)
                photometry.append(phot)
            except NumberOfElementError:
                self.logger.error("The length of Xs and Ys must be equal")
                raise NumberOfElementError("The length of Xs and Ys must be equal")
            except Exception as error:
                self.logger.warning(error)

        if len(photometry) < 1:
            self.logger.warning("Couldn't do photometry")
            raise NumberOfElementError("Couldn't do photometry")

        return vstack(photometry)

    def photometry(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                   headers: Optional[Union[str, List[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> QTable:
        self.logger.info("Photometry")
        photometry = []
        for fits in self:
            try:
                phot = fits.photometry(xs, ys, rs, headers=headers, exposure=exposure)
                photometry.append(phot)
            except NumberOfElementError:
                self.logger.error("The length of Xs and Ys must be equal")
                raise NumberOfElementError("The length of Xs and Ys must be equal")
            except Exception as error:
                self.logger.warning(error)

        if len(photometry) == 0:
            self.logger.warning("Couldn't do photometry")
            raise NumberOfElementError("Couldn't do photometry")

        return vstack(photometry)

    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> QTable:
        self.logger.info("Pixels to Skys")
        data = []
        for each in self:
            try:
                values = each.pixels_to_skys(xs, ys)
                coordinates = values.to_pandas().to_numpy().tolist()
                for i in range(len(coordinates)):
                    coordinates[i].insert(0, each.path.absolute().__str__())
                data.extend(coordinates)
            except Exception as e:
                self.logger.warning(e)

        if len(data) == 0:
            self.logger.error("Couldn't find pixels to skys")
            raise NumberOfElementError("Couldn't find pixels to skys")

        table = QTable(
            list(map(list, itertools.zip_longest(*data, fillvalue=None))),
            names=["image", "x", "y", "ra", "dec"],
        )
        table["x"] *= units.pix
        table["y"] *= units.pix
        table["ra"] *= units.deg
        table["dec"] *= units.deg
        return table

    def skys_to_pixels(self, skys: SkyCoord) -> QTable:
        data = []
        for each in self:
            try:
                values = each.skys_to_pixels(skys)
                coordinates = values.to_pandas().to_numpy().tolist()
                for i in range(len(coordinates)):
                    coordinates[i].insert(0, each.path.absolute().__str__())
                data.extend(coordinates)
            except Exception as e:
                self.logger.warning(e)

        if len(data) == 0:
            self.logger.error("Couldn't find pixels to skys")
            raise NumberOfElementError("Couldn't find pixels to skys")

        table = QTable(
            list(map(list, itertools.zip_longest(*data, fillvalue=None))),
            names=["image", "ra", "dec", "x", "y"],
        )
        table["x"] *= units.pix
        table["y"] *= units.pix
        table["ra"] *= units.deg
        table["dec"] *= units.deg
        return table
