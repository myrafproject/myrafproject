.. _fits_pure_header:

pure_header
===========

Returns the ``Header`` of the file

------------

.. method:: Fits.pure_header() -> astropy.io.header.Header

    Returns the `Header` of the FITS file.

    **Returns**

        ``Header``
            The `Header` object of the file.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    header = fits.pure_header()