.. _fits_sample:

sample
======

Creates a sample ``Fits`` object
see: https://www.astropy.org/astropy-data/tutorials/FITS-images/HorseHead.fits

------------

.. method:: Fits.sample() -> Self

    Creates a sample `Fits` object.

    .. seealso::
        `HorseHead FITS image <https://www.astropy.org/astropy-data/tutorials/FITS-images/HorseHead.fits>`_

    **Returns**

        ``Fits``
            A `Fits` object.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()