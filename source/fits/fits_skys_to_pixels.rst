.. _fits_skys_to_pixels:

skys_to_pixels
==============

Calculates the pixel coordinates corresponding to the given sky coordinates.

------------

.. method:: Fits.skys_to_pixels(skys: Union[List[SkyCoord], SkyCoord]) -> pd.DataFrame

    Calculates the pixel coordinates corresponding to the given sky coordinates.

    **Parameters**

        - **skys** (``Union[List[SkyCoord], SkyCoord]``):
            The sky coordinate(s) for which pixel coordinates are to be calculated.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing the pixel coordinates corresponding to the sky coordinates.

    **Raises**

        - **Unsolvable**
            When the header does not contain a valid WCS solution.




------------

Example:
________

.. code-block:: python

    from myraflib import Fits
    from astropy.coordinates import SkyCoord

    fits = Fits.sample()
    sky = SkyCoord(85.39691915, -2.58041503, unit='deg')
    pixels = fits.skys_to_pixels(sky)
