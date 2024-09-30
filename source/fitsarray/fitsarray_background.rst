.. _fitsarray_background:

background
==========

Returns a list of ``Background`` objects for the FITS files.

------------

.. method:: FitsArray.background(self) -> List[Background]

    Returns a list of ``Background`` objects for the FITS files.

    **Returns**

        ``List[Background]``
            List of ``Background`` objects corresponding to each FITS file.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    backgrounds = fa.background()