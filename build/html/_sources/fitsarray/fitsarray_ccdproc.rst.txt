.. _fitsarray_ccdproc:

ccdproc
=======

Performs CCD correction on the FITS data using provided calibration files.

------------

.. method:: FitsArray.ccdproc(self, master_zero: Optional[Fits] = None, master_dark: Optional[Fits] = None, master_flat: Optional[Fits] = None, exposure: Optional[str] = None, output: Optional[str] = None, force: bool = False) -> Self

    Performs CCD correction on the FITS data using provided calibration files.

    **Parameters**

        ``master_zero`` : ``Optional[Fits]``
            The zero file to be used for bias correction.

        ``master_dark`` : ``Optional[Fits]``
            The dark file to be used for dark correction.

        ``master_flat`` : ``Optional[Fits]``
            The flat file to be used for flat-field correction.

        ``exposure`` : ``Optional[str]``
            The header card containing exposure time (``exptime``).

        ``output`` : ``Optional[str]``
            New path to save the corrected files.

        ``force`` : ``bool``, default=False
            If True, forces the correction even if it results in overcorrection.

    **Returns**

        ``FitsArray``
            A CCD-corrected ``FitsArray`` object.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits

    fa = FitsArray.sample()

    master_zero = Fits.sample()
    master_dark = Fits.sample()
    master_flat = Fits.sample()

    calibrated_fa = fa.ccdproc(master_zero=master_zero, master_dark=master_dark, master_flat=master_flat)