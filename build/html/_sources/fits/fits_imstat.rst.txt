.. _fits_imstat:

imstat
======

Returns statistics of the data

------------

.. method:: Fits.imstat() -> pd.DataFrame

    Returns statistics of the data.

    **Notes**

        Stats are calculated using NumPy and include:

        - Number of pixels
        - Mean
        - Standard deviation
        - Minimum
        - Maximum

    **Returns**

        ``pd.DataFrame``
            The statistics as a pandas DataFrame.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    statistics = fits.imstat()
