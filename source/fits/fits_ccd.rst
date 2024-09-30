.. _fits_ccd:

ccd
===

Returns the CCDData of the given file

------------

.. method:: Fits.ccd() -> CCDData

    Returns the `CCDData` of the given FITS file.

    **Returns**

        ``CCDData``
            The `CCDData` of the file.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    ccd = fits.ccd()
