.. _fitsarray_sample:

sample
======

Creates a sample ``FitsArray`` object.

------------

.. method:: FitsArray.sample(cls, numer_of_samples: int = 10, logger: Optional[Logger] = None, verbose: bool = False) -> Self

    Creates a sample ``FitsArray`` object.

    **Notes**

    This method generates a sample ``FitsArray`` using predefined FITS data.
    For reference, see: `HorseHead.fits <https://www.astropy.org/astropy-data/tutorials/FITS-images/HorseHead.fits>`_.

    **Parameters**

        ``numer_of_samples`` : ``int``, optional, default=10
            The number of ``Fits`` objects to include in the ``FitsArray``.

        ``logger`` : ``Optional[Logger]``
            An optional logger for logging messages during the operation.

        ``verbose`` : ``bool``, optional, default=False
            If set to ``True``, additional information will be displayed during processing.

    **Returns**

        ``FitsArray``
            A ``FitsArray`` object containing the generated samples.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
