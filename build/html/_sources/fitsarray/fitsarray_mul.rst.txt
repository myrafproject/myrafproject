.. _fitsarray_mul:

mul
===

Performs multiplication on the ``FitsArray`` object.

------------

.. method:: FitsArray.mul(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]], output: Optional[str] = None) -> Self

    Performs multiplication on the ``FitsArray`` object.

    **Notes**

    This method can multiply numeric values, other ``Fits`` objects, or lists of numeric values or ``FitsArray`` objects.

    - If ``other`` is numeric, each element of the matrix will be multiplied by that number.
    - If ``other`` is another ``Fits`` object, element-wise multiplication will be performed.
    - If ``other`` is a list of numeric values, the first value will be applied to each matrix. The number of elements in the list must equal the number of elements in the ``FitsArray``.
    - If ``other`` is another ``FitsArray``, element-wise multiplication will be applied. The number of elements in both ``FitsArray`` objects must be equal.

    **Parameters**

        ``other`` : ``Union[Self, Fits, float, int, List[Union[Fits, float, int]]]``
            Either a ``FitsArray`` object, list of floats, list of integers,
            ``Fits`` object, float, or integer.

        ``output`` : ``Optional[str]``
            New path to save the files.

    **Returns**

        ``FitsArray``
            A new ``FitsArray`` object containing the saved FITS files.

    **Raises**

        ``NumberOfElementError``
            Raised when the length of ``other`` is incorrect.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits

    fa = FitsArray.sample()
    fa_2 = FitsArray.sample()

    fits = Fits.sample()

    multiplied_fa_1 = fa.mul(10)
    multiplied_fa_2 = fa.mul(fits)
    multiplied_fa_3 = fa.mul([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    multiplied_fa_4 = fa.mul([Fits.sample() for _ in range(10)])
    multiplied_fa_5 = fa.mul(fa_2)

    multiplied_fa_6 = fa * 10
    multiplied_fa_7 = fa * fits
    multiplied_fa_8 = fa * [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    multiplied_fa_9 = fa * [Fits.sample() for _ in range(10)]
    multiplied_fa_10 = fa * fa_2