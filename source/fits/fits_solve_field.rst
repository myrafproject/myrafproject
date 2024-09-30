.. _fits_solve_field:

solve_field
===========

Solves the field for the given FITS file using Astrometry.net.

------------

.. method:: Fits.solve_field(api_key: str, solve_timeout=120, force_image_upload=False, output=None, override=False) -> Self

    Solves the field for the given FITS file using Astrometry.net.

    **Parameters**

        ``api_key`` : ``str``
            The API key for Astrometry.net (https://nova.astrometry.net/api_help).

        ``solve_timeout`` : ``int``, optional, default=120
            The timeout for the solve operation, in seconds.

        ``force_image_upload`` : ``bool``, optional, default=False
            If ``True``, the image will be uploaded to Astrometry.net even if it is possible to detect sources locally.
            Note that this may take longer than detecting sources locally, and the image will be uploaded unless photutils is installed.

        ``output`` : ``str``, optional
            New path to save the solved FITS file.

        ``override`` : ``bool``, optional, default=False
            If ``True``, will overwrite the output path if a file already exists.

    **Returns**

        ``Fits``
            A ``Fits`` object of the solved field image.

    **Raises**

        ``Unsolvable``
            If the data is unsolvable or if a timeout occurs.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    solved_fits = fits.solve_field("MY-API-KEY")
