.. _fitsarray_value:

value
=====

Returns a table of values for the specified coordinate.

------------

.. method:: FitsArray.value(self, x: int, y: int) -> pd.DataFrame

    Returns a table of values for the specified coordinate.

    **Parameters**

        ``x`` : ``int``
            The x coordinate of the requested pixel.

        ``y`` : ``int``
            The y coordinate of the requested pixel.

    **Returns**

        ``pd.DataFrame``
            A table of values for the specified coordinate.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    values = fa.value(10, 10)