.. _fitsarray_ccd:

ccd
===

Returns the ``CCDData`` of the given files.

------------

.. method:: FitsArray.ccd(self) -> List[CCDData]

    Returns the ``CCDData`` of the given files.

    **Returns**

        ``List[CCDData]``
            A list of ``CCDData`` objects from the files.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    ccd = fa.ccd()