.. _fits_shift:

fits_shift
==========

Shifts the data of the ``Fits`` object.

------------

.. method:: Fits.shift(x: int, y: int, output: Optional[str] = None, override: bool = False) -> Self

    Shifts the data of the ``Fits`` object.

    **Parameters**

        - **x** (``int``):
            The number of pixels to shift in the x-direction.

        - **y** (``int``):
            The number of pixels to shift in the y-direction.

        - **output** (``str, optional``):
            Path of the new fits file where the shifted data will be saved.

        - **override** (``bool, default=False``):
            If ``True``, will overwrite the output if a file with the same name already exists.

    **Returns**

        ``Fits``
            A shifted ``Fits`` object.



------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    shifted_fits = Fits.shift(10, 10)
