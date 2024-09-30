.. _fitsarray_skys_to_pixels:

skys_to_pixels
==============

Calculate Pixel Coordinate of given Sky.


------------


.. method:: FitsArray.skys_to_pixels(skys: Union[List[SkyCoord], SkyCoord]) -> pd.DataFrame

    Calculate Pixel Coordinate of given Sky.

    **Parameters**

    **skys** : ``Union[List[SkyCoord], SkyCoord]``
        Sky coordinate(s).

    **Returns**

    ``pd.DataFrame``
        Data frame of pixel and sky coordinates.

    **Raises**

    **Unsolvable**
        When the header does not contain WCS solution.




------------



Example:
________

.. code-block:: python

    from myraflib import FitsArray
    from astropy.coordinates import SkyCoord

    fa = FitsArray.sample()
    sky = SkyCoord(85.39691915, -2.58041503, unit='deg')
    ccd = fa.skys_to_pixels(sky)