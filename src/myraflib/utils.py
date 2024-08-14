import tempfile
from pathlib import Path
from typing import Union, Iterable, Optional, List, Tuple, Any

import numpy as np

from myraflib.error import NumberOfElementError

NUMERIC = Union[int, float]
NUMERICS = Union[Iterable[NUMERIC], np.ndarray]
HEADER_ANY = Union[int, float, bool, str]


class Fixer:

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

    @staticmethod
    def key_value_pair(keys: Union[str, List[str]],
                       values: Union[str, int, float, bool, List[Union[str, int, float, bool]]],
                       comments: Union[str, int, float, bool, List[Union[str, int, float, bool]]],
                       ) -> Tuple[List[str], List[Union[str, float, int, bool]], List[str]]:
        """
        Corrects keys, values pair for hedit.

        Parameters
        ----------
        keys : Union[str, List[str]]
            keys to be edited
        values : Union[str, int, float, bool, List[Union[str, int, float, bool]]]
            values to added ot/updated on keys
        comments : Union[str, int, float, bool, List[Union[str, int, float, bool]]]
            comments to added ot/updated on keys

        Returns
        -------
        Tuple[List[str], List[Union[str, float, int, bool]], List[str]]
            tuple of keys, values, comments

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
        comments_to_use = comments if isinstance(comments, list) else [comments]

        if len(comments_to_use) < len(values_to_use):
            comments_to_use += [None] * (len(values_to_use) - len(comments_to_use))

        return keys_to_use, values_to_use, comments_to_use

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
