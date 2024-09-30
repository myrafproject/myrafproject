.. _fitsarray_div:

div
===

Performs division on the ``FitsArray`` object.

------------

.. method:: FitsArray.div(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]], output: Optional[str] = None) -> Self

    Performs division on the ``FitsArray`` object.

    **Notes**

    This method can divide numeric values, other ``Fits`` objects, or lists of numeric values or ``FitsArray`` objects.

    - If ``other`` is numeric, each element of the matrix will be divided by that number.
    - If ``other`` is another ``Fits`` object, element-wise division will be performed.
    - If ``other`` is a list of numeric values, the first value will be applied to each matrix. The number of elements in the list must equal the number of elements in the ``FitsArray``.
    - If ``other`` is another ``FitsArray``, element-wise division will be applied. The number of elements in both ``FitsArray`` objects must be equal.

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

    divided_fa_1 = fa.div(10)
    divided_fa_2 = fa.div(fits)
    divided_fa_3 = fa.div([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    divided_fa_4 = fa.div([Fits.sample() for _ in range(10)])
    divided_fa_5 = fa.div(fa_2)

    divided_fa_6 = fa / 10
    divided_fa_7 = fa / fits
    divided_fa_8 = fa / [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    divided_fa_9 = fa / [Fits.sample() for _ in range(10)]
    divided_fa_10 = fa / fa_2