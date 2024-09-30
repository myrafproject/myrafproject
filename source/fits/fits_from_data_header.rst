.. _fits_from_data_header:

from_data_header
================

Creates a ``Fits`` object th give ``data`` and ``header``

------------

.. method:: Fits.from_data_header(data, header=None, output=None, override=False) -> Self

    Creates a `Fits` object from the given `data` and `header`.

    **Parameters**

        ``data`` : ``Any``
            The data as an `np.ndarray`.

        ``header`` : ``Header``, optional
            The header as a `Header` object. If not provided, a default header will be used.

        ``output`` : ``str``, optional
            The desired file path. If set to ``None``, a temporary file will be created.

        ``override`` : ``bool``, default=False
            If ``True``, the existing file at the given path will be overwritten.

    **Returns**

        ``Fits``
            A `Fits` object.

    **Raises**

        ``FileExistsError``
            Raised when the file already exists and `override` is set to ``False``.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits
    import numpy as np

    data = np.random.random((128, 128))

    fits = Fits.from_data_header(data)