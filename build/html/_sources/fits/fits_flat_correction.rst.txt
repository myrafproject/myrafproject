.. _fits_flat_correction:

flat_correction
===============

Applies flat correction to the FITS data using a master flat file.

------------

.. method:: Fits.flat_correction(master_flat: Self, output=None, override=False, force=False) -> Self

    Applies flat correction to the FITS data using a master flat file.

    **Parameters**

        ``master_flat`` : ``Self``
            The master flat file to be used for the correction.

        ``output`` : ``str``, optional
            The path where the flat-corrected FITS file will be saved.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the output path if a file already exists.

        ``force`` : ``bool``, optional, default=False
            Flag to indicate overcorrection.

    **Returns**

        ``Fits``
            A flat-corrected ``Fits`` object.

    **Raises**

        ``OverCorrection``
            If the ``Fits`` object is already flat corrected and ``force`` is ``False``.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    master_flat = Fits.sample()

    flat_corrected = fits.flat_correction(master_flat)
