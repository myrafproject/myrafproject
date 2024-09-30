.. _fitsarray_cosmic_clean:

cosmic_clean
============

Clears cosmic rays from the fits files.

------------

.. method:: FitsArray.cosmic_clean(output: Optional[str] = None, override: bool = False, sigclip: float = 4.5, sigfrac: float = 0.3, objlim: int = 5, gain: float = 1.0, readnoise: float = 6.5, satlevel: float = 65535.0, niter: int = 4, sepmed: bool = True, cleantype: str = 'meanmask', fsmode: str = 'median', psfmodel: str = 'gauss', psffwhm: float = 2.5, psfsize: int = 7, psfk: Any = None, psfbeta: float = 4.765, gain_apply: bool = True) -> Self

    Clears cosmic rays from the fits files.

    **References**
    [1]: https://ccdproc.readthedocs.io/en/latest/api/ccdproc.cosmicray_lacosmic.html

    **Parameters**

        ``output`` : ``str``, optional
            Path of the new fits file.

        ``override`` : ``bool``, default=False
            If True, will overwrite the new_path if a file already exists.

        ``sigclip`` : ``float``, default=4.5
            Laplacian-to-noise limit for cosmic ray detection.
            Lower values will flag more pixels as cosmic rays.
            Default: 4.5. see [1]

        ``sigfrac`` : ``float``, default=0.3
            Fractional detection limit for neighboring pixels.
            For cosmic ray neighbor pixels, a Laplacian-to-noise
            detection limit of sigfrac * sigclip will be used.
            Default: 0.3. see [1]

        ``objlim`` : ``int``, default=5
            Minimum contrast between Laplacian image and the fine structure image.
            Increase this value if cores of bright stars are flagged as cosmic rays.
            Default: 5.0. see [1]

        ``gain`` : ``float``, default=1.0
            Gain of the image (electrons / ADU).
            We always need to work in electrons for cosmic ray detection.
            Default: 1.0 see [1]

        ``readnoise`` : ``float``, default=6.5
            Read noise of the image (electrons).
            Used to generate the noise model of the image.
            Default: 6.5. see [1]

        ``satlevel`` : ``float``, default=65535.0
            Saturation level of the image (electrons).
            This value is used to detect saturated stars and pixels at or
            above this level are added to the mask.
            Default: 65535.0. see [1]

        ``niter`` : ``int``, default=4
            Number of iterations of the LA Cosmic algorithm to perform.
            Default: 4. see [1]

        ``sepmed`` : ``bool``, default=True
            Use the separable median filter instead of the full median filter.
            The separable median is not identical to the full median filter,
            but they are approximately the same.
            The separable median filter is significantly faster,
            and still detects cosmic rays well.
            Note, this is a performance feature,
            and not part of the original L.A. Cosmic.
            Default: True. see [1]

        ``cleantype`` : ``str``, default='meanmask'
            Set which clean algorithm is used:
            1) "median": An unmasked 5x5 median filter.
            2) "medmask": A masked 5x5 median filter.
            3) "meanmask": A masked 5x5 mean filter.
            4) "idw": A masked 5x5 inverse distance weighted interpolation.
            Default: "meanmask". see [1]

        ``fsmode`` : ``str``, default='median'
            Method to build the fine structure image:
            1) "median": Use the median filter in the standard LA Cosmic algorithm.
            2) "convolve": Convolve the image with the PSF kernel to calculate the fine structure image.
            Default: "median". see [1]

        ``psfmodel`` : ``str``, default='gauss'
            Model to use to generate the PSF kernel if fsmode == ‘convolve’ and psfk is None.
            The current choices are Gaussian and Moffat profiles:
            - "gauss" and "moffat" produce circular PSF kernels.
            - The "gaussx" and "gaussy" produce Gaussian kernels in the x and y directions respectively.
            Default: "gauss". see [1]

        ``psffwhm`` : ``float``, default=2.5
            Full Width Half Maximum of the PSF to use to generate the kernel.
            Default: 2.5. see [1]

        ``psfsize`` : ``int``, default=7
            Size of the kernel to calculate.
            Returned kernel will have size psfsize x psfsize.
            psfsize should be odd.
            Default: 7. see [1]

        ``psfk`` : ``Any``, optional
            PSF kernel array to use for the fine structure image
            if fsmode == 'convolve'. If None and fsmode == 'convolve',
            we calculate the PSF kernel using psfmodel.
            Default: None. see [1]

        ``psfbeta`` : ``float``, default=4.765
            Moffat beta parameter. Only used if fsmode=='convolve' and
            psfmodel=='moffat'.
            Default: 4.765.

        ``gain_apply`` : ``bool``, default=True
            If True, return gain-corrected data, with correct units,
            otherwise do not gain-correct the data.
            Default is True to preserve backwards compatibility. see [1]

    **Returns**

        ``FitsArray``
            Cleaned ``FitsArray``

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    clean_fa = fits.cosmic_clean()