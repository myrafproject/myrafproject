.. _fitsarray_rotate:

rotate
======

Rotates the data of the ``FitsArray`` object.

------------

.. method:: FitsArray.rotate(self, angle: Union[List[Union[float, int]], float, int], output: Optional[str] = None) -> Self

    Rotates the data of the ``FitsArray`` object.

    **Parameters**

        ``angle`` : ``Union[List[Union[float, int]], float, int]``
            Rotation angle(s) in radians.

        ``output`` : ``Optional[str]``
            New path to save the files.

    **Returns**

        ``FitsArray``
            A rotated ``FitsArray`` object.





------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray
    import math

    fa = FitsArray.sample()

    rotated_fa_1 = fa.rotate(math.radians(45))
    rotated_fa_2 = fa.rotate([math.radians(angle) for angle in range(45, 145, 10)])
