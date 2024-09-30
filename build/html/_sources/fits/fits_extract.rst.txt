.. _fits_extract:

extract
=======

Runs ``astroalign._find_sources`` to detect sources on the image.

------------

.. method:: Fits.extract(detection_sigma: float = 5.0, min_area: float = 5.0) -> pd.DataFrame

    Runs ``astroalign._find_sources`` to detect sources on the image.

    **Parameters**

        - **detection_sigma** (``float``, default=5.0):
            Threshold for source detection, defined as ``thresh = detection_sigma * bkg.globalrms``.

        - **min_area** (``float``, default=5.0):
            Minimum area of connected pixels to be considered as a source.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing a list of sources found on the image.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    sources = fits.extract()
