.. _fitsarray_map_to_sky:

map_to_sky
==========

Returns sources on the image from Simbad.

------------

.. method:: FitsArray.map_to_sky() -> pd.DataFrame

    Returns sources on the image from Simbad.

    **Returns**

        ``pd.DataFrame``
            Data frame of names, pixel, and sky coordinates.

    **Raises**

        ``Unsolvable``
            When the header does not contain WCS solution.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    sources = fa.map_to_sky()