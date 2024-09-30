.. _fits_show:

show
====

Displays the image using matplotlib.

------------

.. method:: Fits.show(scale=True, sources=None) -> None

    Displays the image using matplotlib.

    **Parameters**

        ``scale`` : ``bool``, optional, default=True
            If ``True``, scales the image for better visualization.

        ``sources`` : ``Optional[pd.DataFrame]``, optional
            If provided, draws points on the image based on the coordinates in the DataFrame.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    fits.show()
