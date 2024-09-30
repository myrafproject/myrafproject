.. _fits_pow:

pow
===

Performs a power operation on the ``Fits`` object.

------------

.. method:: Fits.pow(other, output=None, override=False) -> Self

    Performs a power operation on the ``Fits`` object.

    **Notes**

    This method can raise numeric values or another ``Fits`` object to a power.

    - If ``other`` is numeric, each element of the matrix will be raised to that number.
    - If ``other`` is another ``Fits`` object, element-wise power will be performed.

    **Parameters**

        ``other`` : ``Union[Self, float, int]``
            Either a ``Fits`` object, a float, or an integer.

        ``output`` : ``Optional[str]``
            New path to save the resulting file.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the ``output`` path if a file already exists.

    **Returns**

        ``Fits``
            A new ``Fits`` object representing the result of the power operation.

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

    new_fits_1 = fits.pow(2)

    new_fits_2 = fits.pow(other)
