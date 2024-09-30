.. _fits_header:

header
======

Returns headers of the fits file

------------

.. method:: Fits.header() -> pd.DataFrame

    Returns headers of the FITS file.

    **Returns**

        ``pd.DataFrame``
            The headers as a pandas DataFrame.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    header = fits.header()