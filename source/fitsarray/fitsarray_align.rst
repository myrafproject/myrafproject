.. _fitsarray_align:

align
=====

Aligns the FITS files with the given reference.

------------

.. method:: FitsArray.align(self, reference: Union[Fits, int] = 0, output: Optional[str] = None, max_control_points: int = 50, min_area: int = 5) -> Self

    Aligns the FITS files with the given reference.

    **Parameters**

        ``reference`` : ``Union[Fits, int]``, default=0
            The reference image or the index of the ``Fits`` object in the
            ``FitsArray`` to be aligned as a ``Fits`` object.

        ``output`` : ``Optional[str]``
            New path to save the files.

        ``max_control_points`` : ``int``, default=50
            The maximum number of control point sources to find the transformation.
            See `Astroalign documentation <https://astroalign.quatrope.org/en/latest/api.html#astroalign.register>`_ for details.

        ``min_area`` : ``int``, default=5
            Minimum number of connected pixels to be considered a source.
            See `Astroalign documentation <https://astroalign.quatrope.org/en/latest/api.html#astroalign.register>`_ for details.

    **Returns**

        ``FitsArray``
            A ``FitsArray`` object of aligned images.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray, Fits
    import math

    fa = FitsArray.sample()
    fits = Fits.sample()

    aligned_fa_1 = fa.align(fits)
    aligned_fa_2 = fa.align(0)
