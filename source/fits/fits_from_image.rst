.. _fits_from_image:

from_image
==========

Creates a ``Fits`` object from the given image file

------------

.. method:: Fits.from_image(path) -> Self

    Creates a ``Fits`` object from the given image file.

    **Parameters**

        ``path`` : ``str``
            Path of the file as a string.

    **Returns**

        ``Fits``
            A ``Fits`` object.

    **Raises**

        ``FileNotFoundError``
            Raised when the file does not exist.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.from_image("PATH/TO/FILE")