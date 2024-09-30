.. _fitsarray_merge:

merge
=====

Merges two ``FitsArray`` objects to create another ``FitsArray``.

------------

.. method:: FitsArray.merge(self, other: Self) -> None

    Merges two ``FitsArray`` objects to create another ``FitsArray``.

    **Parameters**

        ``other`` : ``FitsArray``
            The other ``FitsArray`` to append to this one.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa_1 = FitsArray.sample()
    fa_2 = FitsArray.sample()

    merged_fa = fa_1.merge(fa_2)
