.. _fitsarray_dark_combine:

dark_combine
============

Combines ``FitsArray`` to a ``Fits`` optimized for dark combining.

------------

.. method:: FitsArray.dark_combine(method: str = "median", clipping: Optional[str] = None, weights: Optional[Union[List[str], List[Union[float, int]]]] = None, output: Optional[str] = None, override: bool = False) -> Fits

    Combines ``FitsArray`` to a ``Fits`` optimized for dark combining.

    **Parameters**

        ``method`` : ``str``
            Method of combination. Either "average", "mean", or "median".

        ``clipping`` : ``str``, optional
            Clipping method (same as rejection in IRAF). Either "sigmaclip" or "minmax".

        ``weights`` : ``Union[List[str], List[Union[float, int]]]``, optional
            Weights to be applied before combining. If None, [1, ...] will be used.

        ``output`` : ``str``, optional
            New path to save the files.

        ``override`` : ``bool``, default=False
            If True, delete the already existing file.

    **Returns**

        ``Fits``
            The combined ``Fits``.

    **Raises**

        ``ValueError``
            When the number of weights is not equal to the number of FITS files.

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
    combined = fa.combine()
