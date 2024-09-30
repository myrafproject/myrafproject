.. _fitsarray_pow:

pow
===

Performs a power operation on the ``FitsArray`` object.

------------

.. method:: FitsArray.pow(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]], output: Optional[str] = None) -> Self

    Performs a power operation on the ``FitsArray`` object.

    **Notes**

    This method can raise numeric values, other ``Fits`` objects, or lists of numeric values or ``FitsArray`` objects.

    - If ``other`` is numeric, each element of the matrix will be raised to that power.
    - If ``other`` is another ``Fits`` object, element-wise power will be applied.
    - If ``other`` is a list of numeric values, the first value will be applied to each matrix. The number of elements in the list must equal the number of elements in the ``FitsArray``.
    - If ``other`` is another ``FitsArray``, element-wise power will be applied. The number of elements in both ``FitsArray`` objects must be equal.

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

    raised_fa_1 = fa.pow(2)
    raised_fa_2 = fa.pow(fits)
    raised_fa_3 = fa.pow([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    raised_fa_4 = fa.pow([Fits.sample() for _ in range(10)])
    raised_fa_5 = fa.pow(fa_2)
