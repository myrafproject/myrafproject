.. _fitsarray_solve_field:

solve_field
===========

Solves the field for the given FITS files.

------------

.. method:: FitsArray.solve_field(self, api_key: str, reference: Union[Fits, int] = 0, solve_timeout: int = 120, force_image_upload: bool = False, max_control_points: int = 50, min_area: int = 5, output: Optional[str] = None) -> Self

    Solves the field for the given FITS files.

    **Parameters**

        ``api_key`` : ``str``
            The API key for astrometry.net (https://nova.astrometry.net/api_help).

        ``reference`` : ``Union[Fits, int]``, default=0
            The reference image or the index of the ``Fits`` object in the
            ``FitsArray`` to be solved.

        ``solve_timeout`` : ``int``, default=120
            Timeout for solving the field, in seconds.

        ``force_image_upload`` : ``bool``, default=False
            If True, uploads the image to astrometry.net even if it is possible to
            detect sources in the image locally. This option generally takes longer
            than finding sources locally. The image will still be uploaded unless
            ``photutils`` is installed.
            See `Astroquery documentation <https://astroquery.readthedocs.io/en/latest/api/astroquery.astrometry_net.AstrometryNetClass.html#astroquery.astrometry_net.AstrometryNetClass.solve_from_image>`_.

        ``max_control_points`` : ``int``, default=50
            The maximum number of control point sources to find the transformation.
            See `Astroalign documentation <https://astroalign.quatrope.org/en/latest/api.html#astroalign.register>`_ for details.

        ``min_area`` : ``int``, default=5
            Minimum number of connected pixels to be considered a source.
            See `Astroalign documentation <https://astroalign.quatrope.org/en/latest/api.html#astroalign.register>`_.

        ``output`` : ``Optional[str]``
            New path to save the file.

    **Returns**

        ``FitsArray``
            A ``Fits`` object of the plate-solved image.

    **Raises**

        ``Unsolvable``
            Raised when the reference data cannot be solved or the operation times out.




------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray
    import math

    fa = FitsArray.sample()
    solved_fa = fa.solve_field("API-KEY")
