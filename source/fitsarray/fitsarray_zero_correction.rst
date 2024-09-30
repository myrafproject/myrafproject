.. _fitsarray_zero_correction:

zero_correction
===============

Performs zero correction on the FITS data.

------------

.. method:: FitsArray.zero_correction(self, master_zero: Fits, output: Optional[str] = None, force: bool = False) -> Self

    Performs zero correction on the FITS data.

    **Parameters**

        ``master_zero`` : ``Fits``
            The zero file to be used for correction.

        ``output`` : ``Optional[str]``
            New path to save the files after correction.

        ``force`` : ``bool``, default=False
            If True, forces the correction even if it results in overcorrection.

    **Returns**

        ``FitsArray``
            A zero-corrected ``FitsArray`` object.




------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits
    import math

    fa = FitsArray.sample()
    master_zero = Fits.sample()

    zero_corrected_fa = fa.zero_correction(master_zero)
