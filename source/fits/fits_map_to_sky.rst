.. _fits_map_to_sky:

map_to_sky
==========

Retrieves source information from Simbad and returns their coordinates on the image.

------------

.. method:: Fits.map_to_sky() -> pd.DataFrame

    Retrieves source information from Simbad and returns their coordinates on the image.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing names, pixel coordinates, and corresponding sky coordinates of the sources.

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
    sources = fits.map_to_sky()
