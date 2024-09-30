.. _fitsarray_from_pattern:

from_pattern
============

Create a ``FitsArray`` from patterns.

------------

.. method:: FitsArray.from_pattern(cls, pattern: str, logger: Optional[Logger] = None, verbose: bool = False) -> Self

    Create a ``FitsArray`` from patterns.

    **Notes**

    This method uses a specified pattern to locate and combine FITS files into a single ``FitsArray`` object.

    **Parameters**

        ``pattern`` : ``str``
            The pattern that can be interpreted by `glob` to find FITS files.

        ``logger`` : ``Optional[Logger]``
            An optional logger for logging messages during the operation.

        ``verbose`` : ``bool``, optional, default=False
            If set to ``True``, additional information will be displayed during processing.

    **Returns**

        ``FitsArray``
            The ``FitsArray`` created from the files matching the pattern.

    **Raises**

        ``NumberOfElementError``
            Raised when the number of FITS files found is 0.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.from_pattern("PATH/TO/FILES*.fits")
