.. _fitsarray_shift:

shift
=====

Shifts the data of the ``FitsArray`` object.

------------

.. method:: FitsArray.shift(self, xs: Union[List[int], int], ys: Union[List[int], int], output: Optional[str] = None) -> Self

    Shifts the data of the ``FitsArray`` object.

    **Parameters**

        ``xs`` : ``Union[List[int], int]``
            x coordinate(s) for shifting.

        ``ys`` : ``Union[List[int], int]``
            y coordinate(s) for shifting.

        ``output`` : ``Optional[str]``
            New path to save the files.

    **Returns**

        ``FitsArray``
            A shifted ``FitsArray`` object.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()

    shifted_fa_1 = fa.shift(10, 10)
    shifted_fa_2 = fa.shift([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9 , 8, 7, 6, 5, 4, 3, 2, 1])
