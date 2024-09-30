.. _fits_crop:

fits_crop
=========

Crops the data of the ``Fits`` object.

------------

.. method:: Fits.crop(x: int, y: int, width: int, height: int, output: Optional[str] = None, override: bool = False) -> Self

    Crops the data of the ``Fits`` object.

    **Parameters**

        - **x** (``int``):
            The x-coordinate of the top-left corner of the crop area.

        - **y** (``int``):
            The y-coordinate of the top-left corner of the crop area.

        - **width** (``int``):
            The width of the cropped image.

        - **height** (``int``):
            The height of the cropped image.

        - **output** (``str, optional``):
            Path of the new fits file where the cropped data will be saved.

        - **override** (``bool, default=False``):
            If ``True``, will overwrite the output if a file with the same name already exists.

    **Returns**

        ``Fits``
            A cropped ``Fits`` object.

    **Raises**

        - **IndexError**
            When the data is empty after cropping.




------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    cropped_fits = Fits.crop(100, 100, 200, 200)
