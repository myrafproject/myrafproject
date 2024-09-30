.. _fitsarray_photometry_sep:

photometry_sep
==============

Performs photometry using ``sep``.

------------

.. method:: FitsArray.photometry_sep(xs: NUMERICS, ys: NUMERICS, rs: NUMERICS, headers: Optional[Union[str, list[str]]] = None, exposure: Optional[Union[str, float, int]] = None) -> pd.DataFrame

    Performs photometry using ``sep``.

    **Parameters**

        ``xs`` : ``Union[float, int, List[Union[float, int]]]``
            x coordinate(s) for the photometry.

        ``ys`` : ``Union[float, int, List[Union[float, int]]]``
            y coordinate(s) for the photometry.

        ``rs`` : ``Union[float, int, List[Union[float, int]]]``
            Aperture size(s) for the photometry.

        ``headers`` : ``Union[str, list[str]]``, optional
            Header keys to be extracted after performing photometry.

        ``exposure`` : ``Union[str, float, int]``, optional
            Header key that contains the exposure time or a numeric value of exposure time.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing the photometric data.

    **Raises**

        ``NumberOfElementError``
            When ``xs`` and ``ys`` coordinates do not have the same length.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    phot = fits.photometry_sep([10, 10], [20 , 20], [10, 15, 16])