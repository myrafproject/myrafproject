.. _fitsarray_from_paths:

from_paths
==========

Create a ``FitsArray`` from paths as a list of strings.

------------

.. method:: FitsArray.from_paths(cls, paths: List[str], logger: Optional[Logger] = None, verbose: bool = False) -> Self

    Create a ``FitsArray`` from paths as a list of strings.

    **Notes**

    This method combines multiple FITS files into a single ``FitsArray`` object.

    **Parameters**

        ``paths`` : ``List[str]``
            A list of paths to the FITS files as strings.

        ``logger`` : ``Optional[Logger]``
            An optional logger for logging messages during the operation.

        ``verbose`` : ``bool``, optional, default=False
            If set to ``True``, additional information will be displayed during processing.

    **Returns**

        ``FitsArray``
            The ``FitsArray`` created from the list of FITS files.

    **Raises**

        ``NumberOfElementError``
            Raised when the number of FITS files is 0.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.from_paths(["PATH/TO/FILE_1", "PATH/TO/FILE_2"])
