from abc import ABC, abstractmethod
from typing import Dict, Any, Union, List, Literal, Tuple, Optional, Callable
from typing_extensions import Self
from pathlib import Path
from matplotlib import pyplot as plt
from sep import Background
import numpy as np
from astropy.table import QTable
from astropy.nddata import CCDData
from astropy.coordinates import SkyCoord

from myraflib.utils import NUMERIC, NUMERICS, HEADER_ANY


class Data(ABC):

    @abstractmethod
    def __str__(self) -> str:
        """String representation of Data"""

    @abstractmethod
    def __repr__(self) -> str:
        """Representation of Data"""

    @abstractmethod
    def __del__(self) -> None:
        """Destructor of data"""

    @abstractmethod
    def __abs__(self) -> Self:
        """Absolute value of data"""

    @abstractmethod
    def __add__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (+)"""

    @abstractmethod
    def __iadd__(self, other: Union[Self, NUMERIC]) -> Self:
        """Inplace operator overloading (+=)"""

    @abstractmethod
    def __sub__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (-)"""

    @abstractmethod
    def __isub__(self, other: Union[Self, NUMERIC]) -> Self:
        """Inplace operator overloading (-=)"""

    @abstractmethod
    def __mul__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (*)"""

    @abstractmethod
    def __imul__(self, other: Union[Self, NUMERIC]) -> Self:
        """Inplace operator overloading (*=)"""

    @abstractmethod
    def __truediv__(self, other: Union[Self, NUMERIC]) -> Self:
        """Operator overloading (/)"""

    @abstractmethod
    def __idiv__(self, other: Union[Self, NUMERIC]) -> Self:
        """Inplace operator overloading (/=)"""

    @abstractmethod
    def __pow__(self, power: Union[Self, NUMERIC], modulo=None) -> Self:
        """Operator overloading (**)"""

    @abstractmethod
    def __ipow__(self, other: Union[Self, NUMERIC]) -> Self:
        """Inplace operator overloading (**=)"""

    @abstractmethod
    def __mod__(self, other: Union[Self, NUMERIC], modulo=None) -> Self:
        """Operator overloading (%)"""

    @abstractmethod
    def __imod__(self, other: Union[Self, NUMERIC]) -> Self:
        """Inplace operator overloading (%=)"""

    @abstractmethod
    def __eq__(self, other: Self) -> bool:
        """Operator overloading (==)"""

    @abstractmethod
    def __ne__(self, other: Self) -> Self:
        """Operator overloading (!=)"""

    @abstractmethod
    def __neg__(self) -> Self:
        """Negative operator overloading"""

    @abstractmethod
    def __pos__(self) -> Self:
        """Positive operator overloading"""

    @property
    @abstractmethod
    def file(self) -> str:
        """Returns the fits file's path"""

    @classmethod
    @abstractmethod
    def from_path(cls, path: str) -> Self:
        """Creates a Data Object from a given path"""

    @classmethod
    @abstractmethod
    def sample(cls) -> Self:
        """Creates a sample Data"""

    @abstractmethod
    def is_same(self, other: Self) -> bool:
        """Checks if data is identical to other"""

    @property
    @abstractmethod
    def ccd(self) -> CCDData:
        """Returns the CCDData of fits"""

    @property
    @abstractmethod
    def data(self) -> np.ndarray:
        """Returns the data of the given fits file"""

    @abstractmethod
    def value(self, x: int, y: int) -> NUMERIC:
        """Returns value of a given coordinates"""

    @property
    @abstractmethod
    def header(self) -> Dict[str, Any]:
        """Returns the header of the given fits file"""

    @property
    @abstractmethod
    def stats(self) -> Dict[str, Any]:
        """Returns the stats of the given fits file"""

    @abstractmethod
    def background(self) -> Background:
        """Returns the background of the given fits file"""

    @abstractmethod
    def cosmic_cleaner(self, sigclip: float = 4.5, sigfrac: float = 0.3, objlim: float = 5.0, gain: float = 1.0,
                       readnoise: float = 6.5, satlevel: float = 65535.0, pssl: float = 0.0, niter: int = 4,
                       sepmed: bool = True, cleantype: Literal["median", "medmask", "meanmask", "idw"] = 'meanmask',
                       fsmode: Literal["median", "convolve"] = 'median',
                       psfmodel: Literal["gauss", "moffat", "gaussx", "gaussy"] = 'gauss',
                       psffwhm: float = 2.5, psfsize: int = 7, psfk: np.ndarray = None, psfbeta: float = 4.765,
                       gain_apply: bool = True, output: Optional[str] = None, override: bool = False) -> Self:
        """Cleans the fits file from cosmic rays"""

    @abstractmethod
    def hedit(self, keys: Union[str, List[str]], values: Optional[Union[HEADER_ANY, List[HEADER_ANY]]] = None,
              comment: Optional[Union[HEADER_ANY, List[HEADER_ANY]]] = None, delete: bool = False,
              value_is_key: bool = False, output: Optional[str] = None, override: bool = False) -> Self:
        """Edits header of the given file"""

    @abstractmethod
    def save(self, path: Union[str, Path], overwrite: bool = False) -> Self:
        """Saves the fits file to the given path"""

    @abstractmethod
    def abs(self, output: Optional[str] = None, override: bool = False) -> Self:
        """Return absolute value of DataArray"""

    @abstractmethod
    def add(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        """Adds either another numeric or another fits to this fits file"""

    @abstractmethod
    def sub(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        """Subtracts either another numeric or another fits from this fits file"""

    @abstractmethod
    def mul(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        """Multiplies either another numeric or another fits from this fits file"""

    @abstractmethod
    def div(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        """Divides either another numeric or another fits to this fits file"""

    def pow(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False) -> Self:
        """Raises the data to given value"""

    def mod(self, other: Union[Self, NUMERIC], output: Optional[str] = None, override: bool = False):
        """Modular arithmetic operation"""

    @abstractmethod
    def imarith(self, other: Union[Self, NUMERIC], operator: Literal["+", "-", "*", "/", "**", "^", "%"],
                output: Optional[str] = None, override: bool = False) -> Self:
        """Makes arithmetic operation to fits"""

    @abstractmethod
    def extract(self, detection_sigma: float = 5.0, min_area: float = 5.0) -> QTable:
        """Extracts sources from fits"""

    @abstractmethod
    def daofind(self, sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> QTable:
        """Extracts sources from fits using daofind"""

    @abstractmethod
    def align(self, reference: Self, max_control_points: int = 50, detection_sigma: float = 5.0, min_area: int = 5,
              output: Optional[str] = None, override: bool = False) -> Self:
        """Aligns this with given fits"""

    @abstractmethod
    def show(self, ax: plt.Axes = None, sources: QTable = None, scale: bool = True) -> None:
        """Shows fits data"""

    @abstractmethod
    def solve_field(self, api_key: str) -> Self:
        """WCS solves"""

    @abstractmethod
    def coordinate_picker(self, scale: bool = True) -> QTable:
        """Shows the Image using matplotlib and returns a list of coordinates picked by user"""

    @abstractmethod
    def shift(self, x: NUMERIC, y: NUMERIC, output: Optional[str] = None, override: bool = False) -> Self:
        """Shifts the image"""

    @abstractmethod
    def rotate(self, angle: NUMERIC, output: Optional[str] = None, override: bool = False) -> Self:
        """Rotates the image"""

    @abstractmethod
    def crop(self, x: int, y: int, width: int, height: int, output: Optional[str] = None,
             override: bool = False) -> Self:
        """Crop the data of `Fits` object"""

    @abstractmethod
    def bin(self, binning_factor: Union[int, Tuple[int, int]], func: Callable[..., float] = np.mean,
            output: Optional[str] = None, override: bool = False) -> Self:
        """Bin the data of `Fits` object"""

    @abstractmethod
    def zero_correction(self, master_zero: Self, force: bool = False,
                        output: Optional[str] = None, override: bool = False) -> Self:
        """Zero corrects the fits"""

    @abstractmethod
    def dark_correction(self, master_dark: Self, exposure: Optional[str] = None, force: bool = False,
                        output: Optional[str] = None, override: bool = False) -> Self:
        """Dark corrects the fits"""

    @abstractmethod
    def flat_correction(self, master_flat: Self, force: bool = False, output: Optional[str] = None,
                        override: bool = False) -> Self:
        """Flat corrects the fits"""

    @abstractmethod
    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> QTable:
        """Calculate Sky Coordinate of given Pixel"""

    @abstractmethod
    def skys_to_pixels(self, skys: SkyCoord) -> QTable:
        """Calculate Pixel Coordinate of given Sky"""

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
    def photometry(self, xs: Union[NUMERIC, NUMERICS], ys: Union[NUMERIC, NUMERICS], rs: Union[NUMERIC, NUMERICS],
                   headers: Optional[Union[str, List[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> QTable:
        """Does a photometry using both sep and photutils"""
