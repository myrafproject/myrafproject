.. _fits_save_as:

save_as
=======

Saves the ``Fits`` file to the specified output path.

------------

.. method:: Fits.save_as(output, override=False) -> Self

    Saves the ``Fits`` file to the specified output path.

    **Parameters**

        ``output`` : ``str``
            New path to save the file.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the ``output`` path if a file already exists.

    **Returns**

        ``Fits``
            A new ``Fits`` object representing the saved FITS file.

    **Raises**

        ``FileExistsError``
            If the file already exists and ``override`` is ``False``.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    data = fits.save_as("NEW/FILE/PATH")
