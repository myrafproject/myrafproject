.. _fits_daofind:

daofind
=======

Runs DAOFind to detect sources on the image.

------------

.. method:: Fits.daofind(sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> pd.DataFrame

    Runs DAOFind to detect sources on the image.

    .. seealso::
        - `sigma-clipped statistics documentation <https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipped_stats.html>`_ [1]
        - `DAOStarFinder documentation <https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html>`_ [2]

    **Parameters**

        - **sigma** (``float``, default=3.0):
            The number of standard deviations to use for both the lower and upper clipping limit.
            These limits are overridden by ``sigma_lower`` and ``sigma_upper``, if specified.
            Default is 3. [1]

        - **fwhm** (``float``, default=3.0):
            The full-width half-maximum (FWHM) of the major axis of the Gaussian kernel in units of pixels. [2]

        - **threshold** (``float``, default=5.0):
            The absolute image value above which to select sources. [2]

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing a list of sources found on the image.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    sources = fits.daofind()
