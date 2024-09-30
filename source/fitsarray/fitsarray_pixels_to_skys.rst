.. _fitsarray_pixels_to_skys:

pixels_to_skys
==============



Calculate Sky Coordinate of given Pixel.


------------


.. method:: FitsArray.pixels_to_skys(xs: Union[List[Union[int, float]], int, float], ys: Union[List[Union[int, float]], int, float]) -> pd.DataFrame

    Calculate Sky Coordinate of given Pixel.

    **Parameters**

        ``xs`` : ``Union[List[Union[int, float]], int, float]``
            x coordinate(s) of pixel.

        ``ys`` : ``Union[List[Union[int, float]], int, float]``
            y coordinate(s) of pixel.

    **Returns**

        ``pd.DataFrame``
            Data frame of pixel and sky coordinates.

    **Raises**

    **ValueError**
        When the length of ``xs`` and ``ys`` is not equal.

    **Unsolvable**
        When the header does not contain WCS solution.




------------


Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    ccd = fa.pixels_to_skys(10, 10)