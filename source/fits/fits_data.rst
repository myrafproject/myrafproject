.. _fits_data:

data
====

Returns the data of the FITS file.

------------

.. method:: Fits.data() -> Any

    Returns the data of the FITS file.

    **Returns**

        ``Any``
            The data as an ``np.ndarray``.

    **Raises**

        ``ValueError``
            Raised if the FITS file is not an image.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    data = fits.data()
