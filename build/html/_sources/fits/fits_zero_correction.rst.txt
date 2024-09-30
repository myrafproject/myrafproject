.. _fits_zero_correction:

zero_correction
===============

Applies zero correction to the FITS data using a master zero file.

------------

.. method:: Fits.zero_correction(master_zero: Self, output=None, override=False, force=False) -> Self

    Applies zero correction to the FITS data using a master zero file.

    **Parameters**

        ``master_zero`` : ``Self``
            The master zero file to be used for the correction.

        ``output`` : ``str``, optional
            The path where the zero-corrected FITS file will be saved.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the output path if a file already exists.

        ``force`` : ``bool``, optional, default=False
            Flag to indicate overcorrection.

    **Returns**

        ``Fits``
            A zero-corrected ``Fits`` object.

    **Raises**

        ``OverCorrection``
            If the ``Fits`` object is already zero corrected and ``force`` is ``False``.



------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    master_zero = Fits.sample()

    zero_corrected = fits.zero_correction(master_zero)
