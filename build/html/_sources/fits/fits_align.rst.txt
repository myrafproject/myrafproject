.. _fits_align:

align
=====

Aligns the fits file with the given reference image.

------------

.. method:: Fits.align(reference: Self, output=None, max_control_points=50, min_area=5, override=False) -> Self

    Aligns the fits file with the given reference image.

    **Notes**

    This method aligns the current ``Fits`` object with the specified reference image using control points.

    **Parameters**

        ``reference`` : ``Self``
            The reference image to which the current ``Fits`` object will be aligned.

        ``output`` : ``Optional[str]``, optional
            Path to save the new aligned fits file.

        ``max_control_points`` : ``int``, optional, default=50
            The maximum number of control point sources to find the transformation.

        ``min_area`` : ``int``, optional, default=5
            Minimum number of connected pixels to be considered a source.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the ``output`` path if a file already exists.

    **Returns**

        ``Fits``
            A ``Fits`` object of the aligned image.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    reference = Fits.sample().shift(10, 10)

    aligned = fits.align(reference)
