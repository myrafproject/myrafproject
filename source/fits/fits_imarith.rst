.. _fits_imarith:

imarith
=======

returns the data of fits file

------------

.. method:: Fits.imarith(other, operand: str, output=None, override=False) -> Self

    Performs an arithmetic operation on the ``Fits`` object.

    **Notes**

    This method can perform operations with numeric values or another ``Fits`` object.

    - If ``other`` is numeric, each element of the matrix will be processed using that number.
    - If ``other`` is another ``Fits`` object, element-wise operations will be performed.

    **Parameters**

        ``other`` : ``Union[Self, float, int]``
            Either a ``Fits`` object, a float, or an integer.

        ``operand`` : ``str``
            The operation as a string. One of ``["+", "-", "*", "/"]``.

        ``output`` : ``Optional[str]``
            New path to save the resulting file.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the ``output`` path if a file already exists.

    **Returns**

        ``Fits``
            A new ``Fits`` object representing the result of the arithmetic operation.

    **Raises**

        ``ValueError``
            If the given ``other`` value is not a ``Fits``, ``float``, or ``int``.

        ``ValueError``
            If ``operand`` is not one of ``["+", "-", "*", "/", "**", "^"]``.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    other = fits.data()

    new_fits_1 = fits.imarith(2, "+")
    new_fits_2 = fits.imarith(other, "+")

    new_fits_3 = fits.imarith(2, "-")
    new_fits_4 = fits.imarith(other, "-")

    new_fits_5 = fits.imarith(2, "*")
    new_fits_6 = fits.imarith(other, "*")

    new_fits_7 = fits.imarith(2, "/")
    new_fits_8 = fits.imarith(other, "/")

    new_fits_9 = fits.imarith(2, "**") # or ^
    new_fits_10 = fits.imarith(other, "**") # or ^
