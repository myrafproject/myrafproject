.. _fits_value:

value
=====

Returns a value of asked coordinate

------------

.. method:: Fits.value(x, y) -> float

    Returns the value at the specified coordinates.

    **Parameters**

        ``x`` : ``int``
            X coordinate of the requested pixel.

        ``y`` : ``int``
            Y coordinate of the requested pixel.

    **Returns**

        ``float``
            The value at the specified (x, y) coordinates.

    **Raises**

        ``IndexError``
            Raised if the (x, y) coordinates are out of boundaries.


------------

Example:
________
.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    value = fits.value(10, 10)
