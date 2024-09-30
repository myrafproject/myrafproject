.. _fitsarray_zero_combine:

zero_combine
============

Combines ``FitsArray`` to a ``Fits`` optimized for zero combining.

------------

.. method:: FitsArray.zero_combine(method: str = "median", clipping: Optional[str] = None, output: Optional[str] = None, override: bool = False) -> Fits

    Combines ``FitsArray`` to a ``Fits`` optimized for zero combining.

    **Parameters**

        ``method`` : ``str``
            Method of combination. Either "average", "mean", or "median".

        ``clipping`` : ``str``, optional
            Clipping method (same as rejection in IRAF). Either "sigmaclip" or "minmax".

        ``output`` : ``str``, optional
            New path to save the files.

        ``override`` : ``bool``, default=False
            If True, delete the already existing file.

    **Returns**

        ``Fits``
            The combined ``Fits``.

    **Raises**

        ``ValueError``
            When the method is not either "average", "mean", "median", or "sum".

        ``ValueError``
            When the clipping is not either "sigmaclip" or "minmax".


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    combined = fa.zero_combine()
