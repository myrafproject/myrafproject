.. _fitsarray_sub:

sub
===

Performs subtraction on the ``FitsArray`` object.

------------

.. method:: FitsArray.sub(self, other: Union[Self, Fits, float, int, List[Union[Fits, float, int]]], output: Optional[str] = None) -> Self

    Performs subtraction on the ``FitsArray`` object.

    **Notes**

    This method can subtract numeric values, other ``Fits`` objects, or lists of numeric values or ``FitsArray`` objects.

    - If ``other`` is numeric, each element of the matrix will be subtracted from that number.
    - If ``other`` is another ``Fits`` object, element-wise subtraction will be performed.
    - If ``other`` is a list of numeric values, the first value will be applied to each matrix. The number of elements in the list must equal the number of elements in the ``FitsArray``.
    - If ``other`` is another ``FitsArray``, element-wise subtraction will be applied. The number of elements in both ``FitsArray`` objects must be equal.

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

    subtracted_fa_1 = fa.sub(10)
    subtracted_fa_2 = fa.sub(fits)
    subtracted_fa_3 = fa.sub([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    subtracted_fa_4 = fa.sub([Fits.sample() for _ in range(10)])
    subtracted_fa_5 = fa.sub(fa_2)

    subtracted_fa_6 = fa - 10
    subtracted_fa_7 = fa - fits
    subtracted_fa_8 = fa - [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    subtracted_fa_9 = fa - [Fits.sample() for _ in range(10)]
    subtracted_fa_10 = fa - fa_2