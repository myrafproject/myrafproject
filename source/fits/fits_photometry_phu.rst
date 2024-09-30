.. _fits_photometry_phu:

photometry_phu
==============

Performs photometry using ``photutils``.

------------

.. method:: Fits.photometry_phu(xs: NUMERICS, ys: NUMERICS, rs: NUMERICS, headers: Optional[Union[str, list[str]]] = None, exposure: Optional[Union[str, float, int]] = None) -> pd.DataFrame

    Performs photometry using ``photutils``.

    **Parameters**

        - **xs** (``Union[float, int, List[Union[float, int]]]``):
            x coordinate(s) of the sources.

        - **ys** (``Union[float, int, List[Union[float, int]]]``):
            y coordinate(s) of the sources.

        - **rs** (``Union[float, int, List[Union[float, int]]]``):
            aperture radius(es) for the photometry.

        - **headers** (``Union[str, list[str]], optional``):
            Header keys to be extracted after photometry.

        - **exposure** (``Union[str, float, int], optional``):
            Header key that contains or a numeric value of exposure time.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing the photometric data.

    **Raises**

        - **NumberOfElementError**
            Raised when the ``x`` and ``y`` coordinates do not have the same length.



------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()

    phot = fits.photometry_phu([10, 10], [20 , 20], [10, 15, 16])
