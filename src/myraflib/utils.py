import tempfile
from pathlib import Path, PurePath
from typing import Optional, Union, List, Tuple, Any

import numpy as np

from .error import NumberOfElementError
from .models import NUMERICS


class Fixer:
    @staticmethod
    def smallest_data_type(data: Any) -> Any:
        """
        Returns the smallest data type for the give array without data loss.

        stolen from: https://stackoverflow.com/questions

        Parameters
        ----------
        data : Any
            the data

        Returns
        -------
        Any
            the smallest data type for the give array
        """
        arr_min = data.min()
        arr_max = data.max()
        for data_type in ["u1", "i1", "u2", "i2", "u4", "i4", "u8", "i8"]:
            iinfo = np.iinfo(np.dtype(data_type))
            if arr_min >= int(iinfo.min) and arr_max <= int(iinfo.max):
                return np.dtype(data_type)

        return np.dtype(np.uint)

    @staticmethod
    def key_value_pair(keys: Union[str, List[str]],
                       values: Union[str, int, float, bool, List[Union[str, int, float, bool]]],
                       comments: Optional[Union[str, List[str]]] = None,
                       ) -> Tuple[List[str], List[Union[str, float, int, bool]], List[str]]:
        """
        Corrects keys, values pair for hedit.

        Parameters
        ----------
        keys : Union[str, List[str]]
            keys to be edited
        values : Union[str, int, float, bool, List[Union[str, int, float, bool]]]
            values to added ot/updated on keys
        comments: Optional[Union[str, List[str]]]
            cpmments to added ot/updated on keys

        Returns
        -------
        Tuple[List[str], List[Union[str, float, int, bool]]]
            tuple of keys and values

        Raises
        ------
        ValueError
            when keys is and values is not a list and vice versa
        """

        if isinstance(keys, str) and not isinstance(values, (str, int, float, bool)):
            raise ValueError("Keys is str so values must be either str, int float, or bool")

        if isinstance(keys, list) and not isinstance(values, list):
            raise ValueError("Keys is list so values must be list")

        keys_to_use = keys if isinstance(keys, list) else [keys]
        values_to_use = values if isinstance(values, list) else [values]

        if comments is None:
            comments_ = [""] * len(values_to_use)
        else:
            if isinstance(comments, list):
                comments_ = comments + [""] * (len(values_to_use) - len(comments))
            else:
                comments_ = [comments] + ([""] * (len(values_to_use) - 1))

        return keys_to_use, values_to_use, comments_

    @staticmethod
    def fitsify(path: str) -> str:
        """
        adds fits if the given path does not end with either `fit` ot `fits`

        Parameters
        ----------
        path : str
            the path to check

        Returns
        -------
        string
            the same path if it ends with either `fit` of `fits` otherwise
            adds `fits` to the end of the path
        """
        if not (path.endswith("fit") or path.endswith("fits")):
            return f"{path}.fits"

        return path

    @staticmethod
    def outputs(output: Optional[str], fits_array) -> Union[List[None], List[str]]:
        """
        Replaces parent directory of the given `fits_array` with the given
        directory `output`. If output is None it will create a temporary one
        in the temp directory

        Parameters
        ----------
        output : str, optional
            directory to replace the parent directory of each file in
            `fits_array`
        fits_array : FitsArray
            `FitsArray` object to change parent directory of each file with
            the given output

        Returns
        -------
        list
            `list` of file paths
        """
        if output is None or not Path(output).is_dir():
            return [None] * len(fits_array)

        to_write = []
        for fits in fits_array:
            f = fits.file
            to_write.append(str(PurePath(output, f.name)))

        return to_write

    @staticmethod
    def output(output: Optional[str] = None, override: bool = False,
               prefix: str = "myraf_", suffix: str = ".fits",
               fitsify: bool = True) -> str:
        """
        Checks for the `output`. If it's `None` creates a temporary file.

        Parameters
        ----------
        output : str, optional
            output file path
        override : bool
            deletes the existing file if `override` is `True`, otherwise it
            raises an error
        prefix : str
            `prefix` value for created temporary file
        suffix : str
            `suffix` value for created temporary file
        fitsify : bool
            makes sure the file ends with either `fit` or `fits`

        Returns
        -------
        Path
            `path` new file

        Raises
        ------
        FileExistsError
            when file already exists and `override` is `False`
        """
        if output is None:
            with tempfile.NamedTemporaryFile(delete=True, prefix=prefix,
                                             suffix=suffix) as f:
                output = f.name

        if fitsify:
            output = Fixer.fitsify(output)

        if Path(output).exists():
            if override:
                Path(output).unlink()
            else:
                raise FileExistsError("File already exist")

        return output

    @classmethod
    def aperture(cls, rs: NUMERICS) -> List[Union[float, int]]:
        """
        Makes sure the given aperture(s) are a list of numbers

        Parameters
        ----------
        rs : NUMERICS
            aperture(s)

        Returns
        -------
        list
            Apertures as `list` of numbers. Even if it is just one aperture
        """
        if isinstance(rs, (float, int)):
            rs = [rs]
        return rs

    @staticmethod
    def header(headers: Optional[Union[str, List[str]]] = None) -> Any:
        """
        Makes sure the given header(s) are a list of headers

        Parameters
        ----------
        headers : Union[str, List[str]], optional
            header(s)

        Returns
        -------
        list
            Headers as `list` of strings. Even if it is just one header
        """

        if headers is None:
            return []

        if isinstance(headers, str):
            headers = [headers]

        return headers

    @staticmethod
    def coordinate(xs: NUMERICS, ys: NUMERICS) -> Tuple[List[Union[float, int]], List[Union[float, int]]]:
        """
        Makes sure the given `x` and `y` coordinate(s) are list of numbers and
        have the same length

        Parameters
        ----------
        xs : NUMERICS
            x coordinate(s)
        ys : NUMERICS
            y coordinate(s)

        Returns
        -------
        Tuple[List[Union[float, int]], List[Union[float, int]]]
            tuple of `xs` and `ys` coordinates

        Raises
        ------
        NumberOfElementError
            when `x` and `y` coordinates does not have the same length
        """
        if isinstance(xs, (float, int)):
            xs = [xs]

        if isinstance(ys, (float, int)):
            ys = [ys]

        if len(xs) != len(ys):
            raise NumberOfElementError("The length of Xs and Ys must be equal")

        return [x for x in xs], [y for y in ys]


class Check:
    @staticmethod
    def operand(operand: str) -> None:
        """
        Checks if the operand is both string and one of `["+", "-", "*", "/", "**", "^"]`

        Parameters
        ----------
        operand : str
            the operand
        Returns
        -------
         None


        Raises
        ------
        ValueError
            when operand is not one of `["+", "-", "*", "/", "**", "^"]`
        """
        if operand not in ["+", "-", "*", "/", "**", "^"]:
            raise ValueError("Operand can only be one of these: +, -, *, /, **, ^")

    @staticmethod
    def method(method: str) -> None:
        """
        Checks if the method is both string and one of `["average", "mean", "median", "sum"]`

        Parameters
        ----------
        method : str
            the method
        Returns
        -------
         None


        Raises
        ------
        ValueError
            when method is not one of `["average", "mean", "median", "sum"]`
        """
        if method not in ["average", "mean", "median", "sum"]:
            raise ValueError("Method can only be one of these: average, mean, median, sum")

    @staticmethod
    def clipping(method: Optional[str] = None) -> None:
        """
        Checks if the clipping is both string and one of `["sigma", "minmax"]`

        Parameters
        ----------
        method : str
            the method
        Returns
        -------
         None


        Raises
        ------
        ValueError
            when method is not one of `["sigma", "minmax"]`
        """
        if method is not None:
            if method not in ["sigma", "minmax"]:
                raise ValueError("Method can only be one of these: sigma, minmax")
