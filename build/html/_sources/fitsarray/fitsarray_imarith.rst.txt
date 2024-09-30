.. _fitsarray_imarith:

imarith
=======

Performs an arithmetic operation on the ``FitsArray`` object.

------------

.. method:: FitsArray.imarith(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]], operand: str, output: Optional[str] = None) -> Self

    Performs an arithmetic operation on the ``FitsArray`` object.

    **Notes**

    This method can perform arithmetic operations using numeric values, other ``Fits`` objects, lists of numeric values, or ``FitsArray`` objects.

    - If ``other`` is numeric, each element of the matrix will be processed with that number.
    - If ``other`` is another ``Fits`` object, element-wise operations will be applied.
    - If ``other`` is a list of numeric values, the first value will be applied to each matrix. The number of elements in the list must equal the number of elements in the ``FitsArray``.
    - If ``other`` is another ``FitsArray``, element-wise operations will be applied. The number of elements in both ``FitsArray`` objects must be equal.

    **Parameters**

        ``other`` : ``Union[Self, Fits, float, int, List[Union[Fits, float, int]]]``
            Either a ``FitsArray`` object, list of floats, list of integers,
            ``Fits`` object, float, or integer.

        ``operand`` : ``str``
            The operation to be performed as a string. One of ``["+", "-", "*", "/", "**", "^"]``.

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

    # same thing can be done for all of "+", "-", "*", "/", "**", "^" operations
    added_fa_1 = fa.imarith(10, "+")
    added_fa_2 = fa.imarith(fits, "+")
    added_fa_3 = fa.imarith([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "+")
    added_fa_4 = fa.imarith([Fits.sample() for _ in range(10)], "+")
    added_fa_5 = fa.imarith(fa_2, "+")