.. _fits_pixels_to_skys:

pixels_to_skys
==============

Calculates the sky coordinates corresponding to the given pixel coordinates.

------------

.. method:: Fits.pixels_to_skys(xs: Union[List[Union[int, float]], int, float], ys: Union[List[Union[int, float]], int, float]) -> pd.DataFrame

    Calculates the sky coordinates corresponding to the given pixel coordinates.

    **Parameters**

        - **xs** (``Union[List[Union[int, float]], int, float]``):
            The x coordinate(s) of the pixel(s).

        - **ys** (``Union[List[Union[int, float]], int, float]``):
            The y coordinate(s) of the pixel(s).

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing the pixel and corresponding sky coordinates.

    **Raises**

        - **ValueError**
            When the length of ``xs`` and ``ys`` is not equal.

        - **Unsolvable**
            When the header does not contain a valid WCS solution.



------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    skys = fits.pixels_to_skys(10, 10)
