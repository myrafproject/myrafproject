from abc import ABC, abstractmethod
from typing import Dict, Any, Union, List, Tuple, Optional, Callable, Iterable, Iterator, Literal
from typing_extensions import Self
from pathlib import Path
from sep import Background
import numpy as np
from astropy.table import QTable
from astropy.nddata import CCDData
from astropy.coordinates import SkyCoord

from myraflib.data_model import Data
from myraflib.utils import NUMERIC, NUMERICS, HEADER_ANY


class DataArray(ABC):
    data: Iterable[Data]

    @abstractmethod
    def __str__(self) -> str:
        """String representation of Data"""

    @abstractmethod
    def __repr__(self) -> str:
        """Representation of Data"""

    # @abstractmethod
    # def __del__(self) -> None:
    #     """Destructor of data"""
    #
    @abstractmethod
    def __abs__(self) -> Self:
        """Absolute value of data"""

    @abstractmethod
    def __add__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (+)"""

    @abstractmethod
    def __radd__(self, other: Union[Self, NUMERIC]) -> Self:
        """Right operator overloading (+)"""

    @abstractmethod
    def __sub__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (-)"""

    @abstractmethod
    def __rsub__(self, other: Union[Self, NUMERIC]) -> Self:
        """Right operator overloading (-)"""

    @abstractmethod
    def __mul__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (*)"""

    @abstractmethod
    def __rmul__(self, other: Union[Self, NUMERIC]) -> Self:
        """Right operator overloading (*)"""

    @abstractmethod
    def __truediv__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (/)"""

    @abstractmethod
    def __pow__(self, power: Union[Self, NUMERIC], modulo=None) -> Self:
        """Operator overloading (**)"""

    #
    @abstractmethod
    def __mod__(self, power: Union[Self, NUMERIC], modulo=None) -> Self:
        """Operator overloading (%)"""

    @abstractmethod
    def __rmod__(self, power: Union[Self, NUMERIC], modulo=None) -> Self:
        """Right operator overloading (%)"""

    @abstractmethod
    def __neg__(self) -> Self:
        """Negative operator overloading"""

    @abstractmethod
    def __pos__(self) -> Self:
        """Positive operator overloading"""

    @abstractmethod
    def __contains__(self, item: Data) -> bool:
        """Checks if item is in DataArray"""

    @abstractmethod
    def __setitem__(self, key: Union[int, slice], value: Data) -> None:
        """Sets value to the given index"""

    @abstractmethod
    def __delitem__(self, key: Union[int, slice]) -> None:
        """Deletes value to the given index"""

    @classmethod
    @abstractmethod
    def from_paths(cls, paths: List[str]) -> Self:
        """Returns a DataArray from a list of paths"""

    @classmethod
    @abstractmethod
    def from_pattern(cls, pattern: str) -> Self:
        """Returns a DataArray from a pattern (glob)"""

    @classmethod
    @abstractmethod
    def sample(cls, n=10) -> Self:
        """Creates a sample DataArray"""

    @abstractmethod
    def merge(self, other: Self) -> Self:
        """Returns merged DataArrays"""

    @abstractmethod
    def append(self, other: Data) -> Self:
        """Returns an appended DataArray"""

    @property
    @abstractmethod
    def header(self) -> QTable:
        """Returns headers of DataArray"""

    @property
    @abstractmethod
    def data(self) -> Iterator[np.ndarray]:
        """Returns data of DataArray"""

    @property
    @abstractmethod
    def ccd(self) -> Iterator[CCDData]:
        """Returns CCD data of DataArray"""

    @abstractmethod
    def value(self, x: int, y: int) -> np.ndarray:
        """Returns value of a given coordinates"""

    @property
    @abstractmethod
    def files(self) -> List[str]:
        """Returns the fits files' paths"""

    @property
    @abstractmethod
    def stats(self) -> QTable:
        """Returns a DataFrame of statistics of DataArray"""

    @abstractmethod
    def background(self) -> Iterator[Background]:
        """Returns the background of the given fits file"""

    @abstractmethod
    def cosmic_cleaner(self, sigclip: float = 4.5, sigfrac: float = 0.3, objlim: float = 5.0, gain: float = 1.0,
                       readnoise: float = 6.5, satlevel: float = 65535.0, pssl: float = 0.0, niter: int = 4,
                       sepmed: bool = True, cleantype: Literal["median", "medmask", "meanmask", "idw"] = 'meanmask',
                       fsmode: Literal["median", "convolve"] = 'median',
                       psfmodel: Literal["gauss", "moffat", "gaussx", "gaussy"] = 'gauss',
                       psffwhm: float = 2.5, psfsize: int = 7, psfk: np.ndarray = None, psfbeta: float = 4.765,
                       gain_apply: bool = True) -> Self:
        """Cleans the fits file from cosmic rays"""

    @abstractmethod
    def hedit(self, keys: Union[str, List[str]], values: Optional[Union[HEADER_ANY, List[HEADER_ANY]]] = None,
              delete: bool = False, value_is_key: bool = False) -> Self:
        """Edits header of given files"""

    @abstractmethod
    def hselect(self, fields: Union[str, List[str]]) -> QTable:
        """Returns a Table of selected headers of DataArray"""

    @abstractmethod
    def save(self, path: Union[str, Path], overwrite: bool = False) -> Self:
        """Saves DataArray to given path"""

    @abstractmethod
    def abs(self) -> Self:
        """Return absolute value of DataArray"""

    @abstractmethod
    def add(self, other: Union[Self, Data, NUMERIC, List[Union[Data, NUMERIC]]]) -> Self:
        """Adds either another numeric, Data, DataArray or list of numerics to the given DataArray"""

    @abstractmethod
    def sub(self, other: Union[Self, Data, NUMERIC, List[Union[Data, NUMERIC]]]) -> Self:
        """Subtracts either another numeric, Data, DataArray or list of numerics from the given DataArray"""

    @abstractmethod
    def mul(self, other: Union[Self, Data, NUMERIC, List[Union[Data, NUMERIC]]]) -> Self:
        """Multiplies either another numeric, Data, DataArray or list of numerics to the given DataArray"""

    @abstractmethod
    def div(self, other: Union[Self, Data, NUMERIC, List[Union[Data, NUMERIC]]]) -> Self:
        """Divides either another numeric, Data, DataArray or list of numerics to the given DataArray"""

    @abstractmethod
    def pow(self, other: Union[Self, Data, NUMERIC, List[Union[Data, NUMERIC]]]) -> Self:
        """Raises the data to given value"""

    def mod(self, other: Union[Self, Data, NUMERIC, List[Union[Data, NUMERIC]]]):
        """Modular arithmetic operation"""

    @abstractmethod
    def imarith(self, other: Union[Self, NUMERIC], operator: Literal["+", "-", "*", "/", "**", "^", "%"]) -> Self:
        """Makes arithmetic operation to fits"""

    @abstractmethod
    def extract(self, index: int = 0, detection_sigma: float = 5.0, min_area: float = 5.0) -> QTable:
        """Extracts sources from fits"""

    @abstractmethod
    def daofind(self, index: int = 0, sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> QTable:
        """Extracts sources from fits using daofind"""

    @abstractmethod
    def align(self, reference: Union[Data, int] = 0, max_control_points: int = 50, min_area: int = 5) -> Self:
        """Aligns the DataArray by another Data"""

    @abstractmethod
    def shift(self, xs: Union[List[int], int], ys: Union[List[int], int]) -> Self:
        """Shifts the DataArray by the given numerics"""

    @abstractmethod
    def rotate(self, angle: Union[List[NUMERIC], NUMERIC]) -> Self:
        """Rotates the DataArray by given angle"""

    @abstractmethod
    def crop(self, x: Union[int, List[int]], y: Union[int, List[int]],
             width: Union[int, List[int]], height: Union[int, List[int]]) -> Self:
        """Crops the DataArray by given coordinates"""

    @abstractmethod
    def bin(self, binning_factor: Union[Union[int, Tuple[int, int]], List[Union[int, Tuple[int, int]]]],
            func: Callable[..., float] = np.mean) -> Self:
        """Bin the DataArray"""

    @abstractmethod
    def show(self, points: QTable = None, scale: bool = True, interval: float = 1.0) -> None:
        """Shows DataArray"""

    @abstractmethod
    def solve_field(self, api_key: str, reference: Union[Data, int] = 0, solve_timeout: int = 120,
                    force_image_upload: bool = False, max_control_points: int = 50, min_area: int = 5,
                    soft_solve: bool = True) -> Self:
        """WCS solves"""

    @abstractmethod
    def group_by(self, groups: Union[str, List[str]]) -> Dict[Any, Self]:
        """Groups the DataArray"""

    @abstractmethod
    def combine(self, method: Literal["average", "mean", "median", "sum"] = "average",
                clipping: Literal[None, "sigma", "minmax"] = None,
                weights: Optional[List[Union[float, int]]] = None) -> Data:
        """Combines the DataArray to Data"""

    @abstractmethod
    def zero_combine(self, method: Literal["average", "mean", "median"] = "median",
                     clipping: Literal[None, "sigma", "minmax"] = None) -> Data:
        """Combines the DataArray to Data (zerocombine)"""

    @abstractmethod
    def dark_combine(self, method: Literal["average", "mean", "median"] = "median",
                     clipping: Literal[None, "sigma", "minmax"] = None,
                     weights: Optional[Union[List[str], List[Union[float, int]]]] = None) -> Data:
        """Combines the DataArray to Data (darkcombine)"""

    @abstractmethod
    def flat_combine(self, method: Literal["average", "mean", "median"] = "median",
                     clipping: Literal[None, "sigma", "minmax"] = None,
                     weights: Optional[Union[List[str], List[Union[float, int]]]] = None) -> Data:
        """Combines the DataArray to Data (flatcombine)"""

    @abstractmethod
    def zero_correction(self, master_zero: Self, force: bool = False) -> Self:
        """Does zero correction of the data"""

    @abstractmethod
    def dark_correction(self, master_dark: Self, exposure: Optional[str] = None, force: bool = False) -> Self:
        """Dark corrects the fits"""

    @abstractmethod
    def flat_correction(self, master_flat: Self, exposure: Optional[str] = None, force: bool = False) -> Self:
        """Flat corrects the fits"""

    @abstractmethod
    def photometry_sep(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                       headers: Optional[Union[str, List[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> QTable:
        """Does a photometry using sep"""

    @abstractmethod
    def photometry_phu(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                       headers: Optional[Union[str, List[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> QTable:
        """Does a photometry using photutils"""

    @abstractmethod
    def photometry(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                   headers: Optional[Union[str, List[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> QTable:
        """Does a photometry using both sep and photutils"""

    @abstractmethod
    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> QTable:
        """Calculate Sky Coordinate of given Pixel"""

    @abstractmethod
    def skys_to_pixels(self, skys: SkyCoord) -> QTable:
        """Calculate Pixel Coordinate of given Sky"""
