.. _fitsarray_dark_correction:

dark_correction
===============

Performs dark correction on the FITS data.

------------

.. method:: FitsArray.dark_correction(self, master_dark: Fits, exposure: Optional[str] = None, output: Optional[str] = None, force: bool = False) -> Self

    Performs dark correction on the FITS data.

    **Parameters**

        ``master_dark`` : ``Fits``
            The dark file to be used for correction.

        ``exposure`` : ``Optional[str]``
            The header card that contains the exposure time (`exptime`).

        ``output`` : ``Optional[str]``
            New path to save the files after correction.

        ``force`` : ``bool``, default=False
            If True, forces the correction even if it results in overcorrection.

    **Returns**

        ``FitsArray``
            A dark-corrected ``FitsArray`` object.





------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits
    import math

    fa = FitsArray.sample()
    master_dark = Fits.sample()

    dark_corrected_fa = fa.dark_correction(master_dark)
