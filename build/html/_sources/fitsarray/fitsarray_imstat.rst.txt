.. _fitsarray_imstat:

imstat
======

Returns statistics of the data.

------------

.. method:: FitsArray.imstat(self) -> pd.DataFrame

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
            The statistics as a DataFrame.




------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    statistics = fa.imstat()