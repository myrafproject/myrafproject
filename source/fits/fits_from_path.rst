.. _fits_from_path:

from_path
=========

Creates a ``Fits`` object from the given file `path` as string

------------

.. method:: Fits.from_path(path) -> Self

    Creates a `Fits` object from the given file `path` as a string.

    **Parameters**

        ``path`` : ``str``
            Path of the file as a string.

    **Returns**

        ``Fits``
            A `Fits` object.

    **Raises**

        ``FileNotFoundError``
            Raised when the file does not exist.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.from_path("PATH/TO/FILE")
