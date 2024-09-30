.. _fitsarray_hedit:

hedit
=====

Edits the header of the given files.

------------

.. method:: FitsArray.hedit(self, keys: Union[str, List[str]], values: Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]] = None, comments: Optional[Union[str, List[str]]] = None, delete: bool = False, value_is_key: bool = False) -> Self

    Edits the header of the given files.

    **Parameters**

        ``keys`` : ``Union[str, List[str]]``
            Keys to be altered.

        ``values`` : ``Optional[Union[str, int, float, bool, List[Union[str, int, float, bool]]]``, optional
            Values to be added or set. This will be ignored if ``delete`` is ``True``.

        ``comments`` : ``Optional[Union[str, List[str]]]``, optional
            Comments to be added. This will be ignored if ``delete`` is ``True``.

        ``delete`` : ``bool``, optional
            If set to ``True``, deletes the key from the header.

        ``value_is_key`` : ``bool``, optional
            If set to ``True``, adds the value of the key given in ``values``. This will be ignored if ``delete`` is ``True``.

    **Returns**

        ``FitsArray``
            The same ``FitsArray`` object after editing the headers.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    fa.hedit("MYRAF", "value")