.. _fitsarray_flat_correction:

flat_correction
===============

Performs flat correction on the FITS data.

------------

.. method:: FitsArray.flat_correction(self, master_flat: Fits, output: Optional[str] = None, force: bool = False) -> Self

    Performs flat correction on the FITS data.

    **Parameters**

        ``master_flat`` : ``Fits``
            The flat file to be used for correction.

        ``output`` : ``Optional[str]``
            New path to save the files after correction.

        ``force`` : ``bool``, default=False
            If True, forces the correction even if it results in overcorrection.

    **Returns**

        ``FitsArray``
            A flat-corrected ``FitsArray`` object.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits
    import math

    fa = FitsArray.sample()
    master_flat = Fits.sample()

    flat_corrected_fa = fa.flat_correction(master_flat)
