.. _fitsarray_header:

header
======

Returns the headers of the FITS files.

------------

.. method:: FitsArray.header(self) -> pd.DataFrame

    Returns the headers of the FITS files.

    **Returns**

        ``pd.DataFrame``
            The headers as a DataFrame.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    header = fa.header()
