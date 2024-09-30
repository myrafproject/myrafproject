.. _fitsarray_extract:

extract
=======

Runs ``astroalign._find_sources`` to detect sources on the image.

------------

.. method:: FitsArray.extract(index: int = 0, detection_sigma: float = 5.0, min_area: float = 5.0) -> pd.DataFrame

    Runs ``astroalign._find_sources`` to detect sources on the image.

    **Parameters**

        ``index`` : ``int``, default=0
            The index of the ``Fits`` object in the ``FitsArray`` to run ``extract`` on.

        ``detection_sigma`` : ``float``, default=5.0
            Threshold value for source detection, calculated as
            ``thresh = detection_sigma * bkg.globalrms``.

        ``min_area`` : ``float``, default=5.0
            Minimum area of detected sources.

    **Returns**

        ``pd.DataFrame``
            DataFrame containing the list of sources found on the image.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    sources = fa.extract()