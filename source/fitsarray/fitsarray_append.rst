.. _fitsarray_append:

append
======

Appends a ``Fits`` object to a ``FitsArray``.

------------

.. method:: FitsArray.append(self, other: Fits) -> None

    Appends a ``Fits`` object to a ``FitsArray``.

    **Parameters**

        ``other`` : ``Fits``
            The ``Fits`` object to append to the ``FitsArray``.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits

    fa = FitsArray.sample()
    fits = Fits.sample()

    appended_fa = fa.append(fits)
