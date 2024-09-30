.. _fits_coordinate_picker:

coordinate_picker
=================

Displays the image using matplotlib and allows the user to pick coordinates.

------------

.. method:: Fits.coordinate_picker(scale=True) -> pd.DataFrame

    Displays the image using matplotlib and allows the user to pick coordinates.

    **Parameters**

        ``scale`` : ``bool``, optional, default=True
            If ``True``, scales the image for better visualization.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing the list of coordinates selected by the user.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    coordinates = fits.coordinate_picker()
