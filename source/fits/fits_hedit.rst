.. _fits_hedit:

hedit
=====

Edits the header of the given FITS file.

------------

.. method:: Fits.hedit(keys, values=None, comments=None, delete=False, value_is_key=False) -> Self

    Edits the header of the given FITS file.

    **Parameters**

        ``keys`` : ``str`` or ``List[str]``
            Keys to be altered.

        ``values`` : ``Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]]``, optional
            Values to be added. This will be ignored if `delete` is ``True``.

        ``comments`` : ``Optional[Union[str, List[str]]]``, optional
            Comments to be added. This will be ignored if `delete` is ``True``.

        ``delete`` : ``bool``, optional
            If ``True``, deletes the key from the header.

        ``value_is_key`` : ``bool``, optional
            If ``True``, adds the value of the key given in `values`. This will be ignored if `delete` is ``True``.

    **Returns**

        ``Fits``
            The same `Fits` object.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    fits.hedit("MYRAF", "value")
