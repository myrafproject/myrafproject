.. _fits_sub:

sub
===

Performs a subtraction operation on the ``Fits`` object.

------------

.. method:: Fits.sub(other, output=None, override=False) -> Self

    Performs a subtraction operation on the ``Fits`` object.

    **Notes**

    This method can subtract numeric values or another ``Fits`` object.

    - If ``other`` is numeric, each element of the matrix will be subtracted by that number.
    - If `other` is another ``Fits`` object, element-wise subtraction will be performed.

    **Parameters**

        ``other`` : ``Union[Self, float, int]``
            Either a ``Fits`` object, a float, or an integer.

        ``output`` : ``Optional[str]``
            New path to save the resulting file.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the ``output`` path if a file already exists.

    **Returns**

        ``Fits``
            A new ``Fits`` object representing the result of the subtraction.

    **Raises**

        ``FileExistsError``
            If the file already exists and ``override`` is ``False``.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    other = Fits.sample()

    new_fits_1 = fits.sub(120)
    new_fits_2 = fits - 120

    new_fits_3 = fits.sub(other)
    new_fits_4 = fits - other
