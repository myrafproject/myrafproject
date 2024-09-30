.. _fits_background:

background
==========

Returns the background object of the FITS file.

------------

.. method:: Fits.background() -> sep.Background

    Returns the background object of the FITS file.

    **Returns**

        ``Background``
            A ``Background`` object representing the background of the ``Fits`` data.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    background = fits.background()
