.. _fitsarray_data:

data
==========

Returns the data of the FITS files.

------------

.. method:: FitsArray.data(self) -> List[Any]

    Returns the data of the FITS files.

    **Returns**

        ``List[Any]``
            A list of data as ``np.ndarray`` objects.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    data = fa.data()