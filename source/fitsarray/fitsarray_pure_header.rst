.. _fitsarray_pure_header:

pure_header
===========

Returns the ``Header`` of the files.

------------

.. method:: FitsArray.pure_header(self) -> List[Header]

    Returns the ``Header`` of the files.

    **Returns**

        ``List[Header]``
            A list of ``Header`` objects from the files.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    headers = fa.pure_header()