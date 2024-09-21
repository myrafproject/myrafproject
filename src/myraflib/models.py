from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, List, Union, Any, TYPE_CHECKING, Dict, Callable

import numpy as np
from astropy.time import Time
from typing_extensions import Self

if TYPE_CHECKING:
    from .fits import Fits

from astropy.io.fits import Header
from sep import Background

import pandas as pd
from astropy.nddata import CCDData
from astropy.coordinates import SkyCoord

NUMERICS = Union[float, int, List[Union[float, int]]]


class Data(ABC):
    high_precision = False

    @classmethod
    @abstractmethod
    def from_image(cls, path: str) -> Self:
        ...

    @classmethod
    @abstractmethod
    def from_path(cls, path: str) -> Self:
        ...

    @classmethod
    @abstractmethod
    def from_data_header(cls, data: Any, header: Optional[Header] = None,
                         output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @classmethod
    @abstractmethod
    def sample(cls) -> Self:
        ...

    @abstractmethod
    def reset_zmag(self) -> None:
        ...

    @abstractmethod
    def header(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def data(self) -> Any:
        ...

    @abstractmethod
    def value(self, x: int, y: int) -> float:
        ...

    @abstractmethod
    def pure_header(self) -> Header:
        ...

    @abstractmethod
    def ccd(self) -> CCDData:
        ...

    @abstractmethod
    def imstat(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def cosmic_clean(self, output: Optional[str] = None,
                     override: bool = False, sigclip: float = 4.5,
                     sigfrac: float = 0.3, objlim: int = 5, gain: float = 1.0,
                     readnoise: float = 6.5, satlevel: float = 65535.0,
                     niter: int = 4, sepmed: bool = True,
                     cleantype: str = 'meanmask', fsmode: str = 'median',
                     psfmodel: str = 'gauss', psffwhm: float = 2.5,
                     psfsize: int = 7, psfk: Optional[Any] = None,
                     psfbeta: float = 4.765, gain_apply: bool = True) -> Self:
        ...

    @abstractmethod
    def hedit(self, keys: Union[str, List[str]],
              values: Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]] = None,
              comments: Optional[Union[str, List[str]]] = None, delete: bool = False, value_is_key: bool = False
              ) -> Self:
        ...

    @abstractmethod
    def save_as(self, output: str, override: bool = False) -> Self:
        ...

    @abstractmethod
    def add(self, other: Union[Self, float, int],
            output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def sub(self, other: Union[Self, int, float],
            output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def mul(self, other: Union[Self, int, float],
            output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def div(self, other: Union[Self, int, float],
            output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def pow(self, other: Union[Fits, float, int],
            output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def imarith(self, other: Union[Self, int, float], operand: str,
                output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def align(self, reference: Self, output: Optional[str] = None,
              max_control_points: int = 50, min_area: int = 5,
              override: bool = False) -> Self:
        ...

    @abstractmethod
    def show(self, scale: bool = True, sources: Optional[pd.DataFrame] = None) -> None:
        ...

    @abstractmethod
    def coordinate_picker(self, scale: bool = True) -> pd.DataFrame:
        ...

    @abstractmethod
    def solve_field(self, api_key: str, solve_timeout: int = 120,
                    force_image_upload: bool = False,
                    output: Optional[str] = None, override: bool = False
                    ) -> Self:
        ...

    @abstractmethod
    def zero_correction(self, master_zero: Self,
                        output: Optional[str] = None, override: bool = True, force: bool = False) -> Self:
        ...

    @abstractmethod
    def dark_correction(self, master_dark: Self, exposure: Optional[str] = None,
                        output: Optional[str] = None, override: bool = False,
                        force: bool = False) -> Self:
        ...

    @abstractmethod
    def flat_correction(self, master_flat: Self, output: Optional[str] = None,
                        override: bool = False, force: bool = False) -> Self:
        ...

    @abstractmethod
    def ccdproc(self, master_zero: Optional[Self] = None, master_dark: Optional[Self] = None,
                master_flat: Optional[Self] = None, exposure: Optional[str] = None, output: Optional[str] = None,
                override: bool = False, force: bool = False) -> Self:
        ...

    @abstractmethod
    def background(self) -> Background:
        ...

    @abstractmethod
    def daofind(self, sigma: float = 3.0, fwhm: float = 3.0,
                threshold: float = 5.0) -> pd.DataFrame:
        ...

    @abstractmethod
    def extract(self, detection_sigma: float = 5.0,
                min_area: float = 5.0) -> pd.DataFrame:
        ...

    @abstractmethod
    def photometry_sep(self,
                       xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                       headers: Optional[Union[str, list[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> pd.DataFrame:
        ...

    @abstractmethod
    def photometry_phu(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                       headers: Optional[Union[str, list[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> pd.DataFrame:
        ...

    @abstractmethod
    def photometry(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                   headers: Optional[Union[str, list[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> pd.DataFrame:
        ...

    @abstractmethod
    def shift(self, x: int, y: int, output: Optional[str] = None,
              override: bool = False) -> Self:
        ...

    @abstractmethod
    def rotate(self, angle: Union[float, int], output: Optional[str] = None,
               override: bool = False) -> Self:
        ...

    @abstractmethod
    def crop(self, x: int, y: int, width: int, height: int,
             output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def bin(self, binning_factor: Union[int, List[int]], func: Callable[[Any], float] = np.mean,
            output: Optional[str] = None, override: bool = False) -> Self:
        ...

    @abstractmethod
    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> pd.DataFrame:
        ...

    @abstractmethod
    def skys_to_pixels(self, skys: Union[List[SkyCoord], SkyCoord]) -> pd.DataFrame:
        ...

    @abstractmethod
    def map_to_sky(self):
        ...


class DataArray(ABC):
    high_precision = False

    @classmethod
    @abstractmethod
    def from_video(cls, path: str, start_time: Optional[Union[Time, float]] = None) -> Self:
        ...

    @classmethod
    @abstractmethod
    def from_paths(cls, paths: List[str]) -> Self:
        ...

    @classmethod
    @abstractmethod
    def from_pattern(cls, pattern: str) -> Self:
        ...

    @classmethod
    @abstractmethod
    def sample(cls, numer_of_samples: int = 10) -> Self:
        ...

    @abstractmethod
    def merge(self, other: Self) -> None:
        ...

    @abstractmethod
    def append(self, other: Fits) -> None:
        ...

    @abstractmethod
    def header(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def data(self) -> List[Any]:
        ...

    @abstractmethod
    def value(self, x: int, y: int) -> pd.DataFrame:
        ...

    @abstractmethod
    def pure_header(self) -> List[Header]:
        ...

    @abstractmethod
    def ccd(self) -> List[CCDData]:
        ...

    @abstractmethod
    def imstat(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def cosmic_clean(self, output: Optional[str] = None,
                     override: bool = False, sigclip: float = 4.5,
                     sigfrac: float = 0.3, objlim: int = 5, gain: float = 1.0,
                     readnoise: float = 6.5, satlevel: float = 65535.0,
                     niter: int = 4, sepmed: bool = True,
                     cleantype: str = 'meanmask', fsmode: str = 'median',
                     psfmodel: str = 'gauss', psffwhm: float = 2.5,
                     psfsize: int = 7, psfk: Optional[Any] = None,
                     psfbeta: float = 4.765, gain_apply: bool = True) -> Self:
        ...

    @abstractmethod
    def hedit(self, keys: Union[str, List[str]],
              values: Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]] = None,
              comments: Optional[Union[str, List[str]]] = None, delete: bool = False, value_is_key: bool = False
              ) -> Self:
        ...

    @abstractmethod
    def hselect(self, fields: Union[str, List[str]]) -> pd.DataFrame:
        ...

    @abstractmethod
    def save_as(self, output: str) -> Self:
        ...

    @abstractmethod
    def add(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]],
            output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def sub(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]],
            output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def mul(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]],
            output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def div(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]],
            output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def pow(self,
            other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]],
            output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def imarith(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]], operand: str,
                output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def shift(self, xs: Union[List[int], int], ys: Union[List[int], int],
              output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def rotate(self, angle: Union[List[Union[float, int]], float, int],
               output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def crop(self, xs: Union[List[int], int], ys: Union[List[int], int],
             widths: Union[List[int], int], heights: Union[List[int], int],
             output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def bin(self, binning_factor: Union[int, List[int]], func: Callable[[Any], float] = np.mean,
            output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def align(self, other: Union[Fits, int] = 0, output: Optional[str] = None,
              max_control_points: int = 50, min_area: int = 5) -> Self:
        ...

    @abstractmethod
    def show(self, scale: bool = True, interval: float = 1.0) -> None:
        ...

    @abstractmethod
    def solve_field(self, api_key: str, reference: Union[Fits, int] = 0,
                    solve_timeout: int = 120, force_image_upload: bool = False,
                    max_control_points: int = 50, min_area: int = 5,
                    output: Optional[str] = None) -> Self:
        ...

    @abstractmethod
    def zero_correction(self, master_zero: Fits,
                        output: Optional[str] = None, force: bool = False) -> Self:
        ...

    @abstractmethod
    def dark_correction(self, master_dark: Fits, exposure: Optional[str] = None,
                        output: Optional[str] = None, force: bool = False) -> Self:
        ...

    @abstractmethod
    def flat_correction(self, master_flat: Fits,
                        output: Optional[str] = None, force: bool = False) -> Self:
        ...

    @abstractmethod
    def ccdproc(self, master_zero: Optional[Fits] = None, master_dark: Optional[Fits] = None,
                master_flat: Optional[Fits] = None, exposure: Optional[str] = None, output: Optional[str] = None,
                force: bool = False) -> Self:
        ...

    @abstractmethod
    def background(self) -> List[Background]:
        ...

    @abstractmethod
    def daofind(self, index: int = 0, sigma: float = 3.0, fwhm: float = 3.0,
                threshold: float = 5.0) -> pd.DataFrame:
        ...

    @abstractmethod
    def extract(self, index: int = 0, detection_sigma: float = 5.0,
                min_area: float = 5.0) -> pd.DataFrame:
        ...

    @abstractmethod
    def photometry_sep(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                       headers: Optional[Union[str, list[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> pd.DataFrame:
        ...

    @abstractmethod
    def photometry_phu(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                       headers: Optional[Union[str, list[str]]] = None,
                       exposure: Optional[Union[str, float, int]] = None
                       ) -> pd.DataFrame:
        ...

    @abstractmethod
    def photometry(self, xs: NUMERICS, ys: NUMERICS, rs: NUMERICS,
                   headers: Optional[Union[str, list[str]]] = None,
                   exposure: Optional[Union[str, float, int]] = None
                   ) -> pd.DataFrame:
        ...

    @abstractmethod
    def group_by(self, groups: Union[str, List[str]]) -> Dict[Any, Self]:
        ...

    @abstractmethod
    def combine(self, method: str = "average", clipping: Optional[str] = None,
                weights: Optional[List[Union[float, int]]] = None,
                output: Optional[str] = None, override: bool = False) -> Fits:
        ...

    @abstractmethod
    def zero_combine(self, method: str = "median", clipping: Optional[str] = None,
                     output: Optional[str] = None, override: bool = False) -> Fits:
        ...

    @abstractmethod
    def dark_combine(self, method: str = "median", clipping: Optional[str] = None,
                     weights: Optional[Union[List[str], List[Union[float, int]]]] = None,
                     output: Optional[str] = None, override: bool = False) -> Fits:
        ...

    @abstractmethod
    def flat_combine(self, method: str = "median", clipping: Optional[str] = None,
                     weights: Optional[Union[List[str], List[Union[float, int]]]] = None,
                     output: Optional[str] = None, override: bool = False) -> Fits:
        ...

    @abstractmethod
    def pixels_to_skys(self, xs: Union[List[Union[int, float]], int, float],
                       ys: Union[List[Union[int, float]], int, float]) -> pd.DataFrame:
        ...

    @abstractmethod
    def skys_to_pixels(self, skys: Union[List[SkyCoord], SkyCoord]) -> pd.DataFrame:
        ...

    @abstractmethod
    def map_to_sky(self) -> pd.DataFrame:
        ...
