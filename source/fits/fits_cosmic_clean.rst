.. _fits_cosmic_clean:

cosmic_clean
============

Clears cosmic rays from the fits file

------------

.. method:: Fits.cosmic_clean(output=None, override=False, sigclip=4.5, sigfrac=0.3, objlim=5, gain=1.0, readnoise=6.5, satlevel=65535.0, niter=4, sepmed=True, cleantype='meanmask', fsmode='median', psfmodel='gauss', psffwhm=2.5, psfsize=7, psfk=None, psfbeta=4.765, gain_apply=True) -> Self

    Clears cosmic rays from the fits file.

    [1]: https://ccdproc.readthedocs.io/en/latest/api/ccdproc.cosmicray_lacosmic.html

    **Parameters**

        ``output`` : ``str``, optional
            Path of the new FITS file.

        ``override`` : ``bool``, default=False
            If ``True``, will overwrite the ``output`` path if a file already exists.

        ``sigclip`` : ``float``, default=4.5
            Laplacian-to-noise limit for cosmic ray detection.
            Lower values will flag more pixels as cosmic rays.

        ``sigfrac`` : ``float``, default=0.3
            Fractional detection limit for neighboring pixels.
            For cosmic ray neighbor pixels, a Laplacian-to-noise
            detection limit of ``sigfrac * sigclip`` will be used.

        ``objlim`` : ``int``, default=5
            Minimum contrast between Laplacian image and the fine structure image.
            Increase this value if cores of bright stars are flagged as cosmic rays.

        ``gain`` : ``float``, default=1.0
            Gain of the image (electrons / ADU). We always need to work in electrons for cosmic ray detection.

        ``readnoise`` : ``float``, default=6.5
            Read noise of the image (electrons). Used to generate the noise model of the image.

        ``satlevel`` : ``float``, default=65535.0
            Saturation level of the image (electrons). Pixels at or above this level are added to the mask.

        ``niter`` : ``int``, default=4
            Number of iterations of the LA Cosmic algorithm to perform.

        ``sepmed`` : ``bool``, default=True
            Use the separable median filter instead of the full median filter.
            The separable median is significantly faster and still detects cosmic rays well.

        ``cleantype`` : ``str``, default='meanmask'
            Set which clean algorithm is used:
            - "median": An unmasked 5x5 median filter.
            - "medmask": A masked 5x5 median filter.
            - "meanmask": A masked 5x5 mean filter.
            - "idw": A masked 5x5 inverse distance weighted interpolation.

        ``fsmode`` : ``str``, default='median'
            Method to build the fine structure image:
            - "median": Use the median filter in the standard LA Cosmic algorithm.
            - "convolve": Convolve the image with the PSF kernel to calculate the fine structure image.

        ``psfmodel`` : ``str``, default='gauss'
            Model to use to generate the PSF kernel if `fsmode` == 'convolve' and `psfk` is None.

        ``psffwhm`` : ``float``, default=2.5
            Full Width Half Maximum of the PSF to use to generate the kernel.

        ``psfsize`` : ``int``, default=7
            Size of the kernel to calculate. Returned kernel will have size `psfsize` x `psfsize`.

        ``psfk`` : ``Any``, optional
            PSF kernel array to use for the fine structure image if `fsmode` == 'convolve'.

        ``psfbeta`` : ``float``, default=4.765
            Moffat beta parameter. Only used if `fsmode`=='convolve' and `psfmodel=='moffat'`.

        ``gain_apply`` : ``bool``, default=True
            If ``True``, return gain-corrected data with correct units; otherwise, do not gain-correct the data.

    **Returns**

        ``Fits``
            Cleaned FITS file.


------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    cleaned_fits = fits.cosmic_clean()
