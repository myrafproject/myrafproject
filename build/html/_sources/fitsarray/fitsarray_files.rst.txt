.. _fitsarray_files:

files
=====

Returns all files as a list of strings.

------------

.. method:: FitsArray.files(self) -> List[str]

    Returns all files as a list of strings.

    **Returns**

        ``List[str]``
            A list of file paths.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    files = fa.files()
