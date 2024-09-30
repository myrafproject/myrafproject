.. _fitsarray_crop:

crop
====

Crops the data of the ``FitsArray`` object.

------------

.. method:: FitsArray.crop(self, xs: Union[List[int], int], ys: Union[List[int], int], widths: Union[List[int], int], heights: Union[List[int], int], output: Optional[str] = None) -> Self

    Crops the data of the ``FitsArray`` object.

    **Parameters**

        ``xs`` : ``Union[List[int], int]``
            x coordinate(s).

        ``ys`` : ``Union[List[int], int]``
            y coordinate(s).

        ``widths`` : ``Union[List[int], int]``
            width(s).

        ``heights`` : ``Union[List[int], int]``
            height(s).

        ``output`` : ``Optional[str]``
            New path to save the files.

    **Returns**

        ``FitsArray``
            A cropped ``FitsArray`` object.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray
    import math

    fa = FitsArray.sample()

    cropped_fa_1 = fa.crop(10, 10, 100, 100)
    cropped_fa_2 = fa.crop(
        [x for x in range(10)],
        [y for y in range(10)],
        100, 100
    )
