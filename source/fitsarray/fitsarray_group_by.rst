.. _fitsarray_group_by:

group_by
========

Groups the ``FitsArray`` by the given header.

------------

.. method:: FitsArray.group_by(groups: Union[str, List[str]]) -> Dict[Any, Self]

    Groups the ``FitsArray`` by the given header.

    **Parameters**

        ``groups`` : ``Union[str, List[str]]``
            Header keys to group by.

    **Returns**

        ``Dict[Any, FitsArray]``
            A dictionary mapping header keys to ``FitsArray`` pairs.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray
    import math

    fa = FitsArray.sample()
    groped_fa = fa.group_by("IMAGETYP")
