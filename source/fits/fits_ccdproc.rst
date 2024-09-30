.. _fits_ccdproc:

ccdproc
=======

Performs CCD processing corrections on the FITS data, allowing for zero, dark, and flat corrections in any combination.

------------

.. method:: Fits.ccdproc(master_zero=None, master_dark=None, master_flat=None, exposure=None, output=None, override=False, force=False) -> Self

    Performs CCD processing corrections on the FITS data, allowing for zero, dark, and flat corrections in any combination.

    **Parameters**

        ``master_zero`` : ``Optional[Self]``
            The master zero file to be used for correction.

        ``master_dark`` : ``Optional[Self]``
            The master dark file to be used for correction.

        ``master_flat`` : ``Optional[Self]``
            The master flat file to be used for correction.

        ``exposure`` : ``str``, optional
            The header card containing exposure time information.

        ``output`` : ``str``, optional
            The path where the corrected FITS file will be saved.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the output path if a file already exists.

        ``force`` : ``bool``, optional, default=False
            Flag to indicate overcorrection.

    **Returns**

        ``Fits``
            A CCD-corrected ``Fits`` object.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    master_zero = Fits.sample()
    master_dark = Fits.sample()
    master_flat = Fits.sample()

    calibrated_fits = fits.ccdproc(
        master_zero=master_zero,
        master_dark=master_dark,
        master_flat=master_flat
    )
