.. _fitsarray_daofind:

daofind
=======

Runs ``daofind`` to detect sources on the image.

------------

.. method:: FitsArray.daofind(index: int = 0, sigma: float = 3.0, fwhm: float = 3.0, threshold: float = 5.0) -> pd.DataFrame

    Runs ``daofind`` to detect sources on the image.

    **References**

    [1] https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipped_stats.html
    [2] https://photutils.readthedocs.io/en/stable/api/photutils.detection.DAOStarFinder.html

    **Parameters**

        ``index`` : ``int``, default=0
            The index of the ``Fits`` object in the ``FitsArray`` to run ``daofind`` on.

        ``sigma`` : ``float``, default=3.0
            The number of standard deviations to use for both the lower and upper clipping limit.
            These limits are overridden by ``sigma_lower`` and ``sigma_upper``, if input.
            The default is 3. [1]

        ``fwhm`` : ``float``, default=3.0
            The full-width half-maximum (FWHM) of the major axis of the Gaussian kernel in units of pixels. [2]

        ``threshold`` : ``float``, default=5.0
            The absolute image value above which to select sources. [2]

    **Returns**

        ``pd.DataFrame``
            DataFrame containing the list of sources found on the image.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    sources = fa.daofind()