.. _fits_rotate:

fits_rotate
===========

Rotates the data of the ``Fits`` object.

------------

.. method:: Fits.rotate(angle: Union[float, int], output: Optional[str] = None, override: bool = False) -> Self

    Rotates the data of the ``Fits`` object.

    **Parameters**

        - **angle** (``Union[float, int]``):
            The rotation angle in radians.

        - **output** (``str, optional``):
            Path of the new fits file where the rotated data will be saved.

        - **override** (``bool, default=False``):
            If ``True``, will overwrite the output if a file with the same name already exists.

    **Returns**

        ``Fits``
            A rotated ``Fits`` object.



------------

Example:
________

.. code-block:: python

    from myraflib import Fits
    import math

    fits = Fits.sample()
    rotated_fits = fits.rotate(math.radians(45))
