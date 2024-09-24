# clean
`clean` does cosmic clean on FITS files.

usage: im clean [-h] [--sigclip SIGCLIP] [--sigfrac SIGFRAC] [--objlim OBJLIM] [--gain GAIN] [--readnoise READNOISE] [--satlevel SATLEVEL] [--niter NITER] [--sepmed]
                [--cleantype CLEANTYPE] [--fsmode FSMODE] [--psfmodel PSFMODEL] [--psffwhm PSFFWHM] [--psfsize PSFSIZE] [--psfbeta PSFBETA] [--gain_apply]
                output

## Positional Arguments:
  - **output**                Output directory  

## Options:
  - -h, --help                Show this help message and exit  
  - --sigclip SIGCLIP         Laplacian-to-noise limit for cosmic ray detection. Lower values will flag more pixels as cosmic rays.  
  - --sigfrac SIGFRAC         Fractional detection limit for neighboring pixels. For cosmic ray neighbor pixels, a Laplacian-to-noise detection limit of `sigfrac * sigclip` will be used.  
  - --objlim OBJLIM           Minimum contrast between Laplacian image and the fine structure image. Increase this value if cores of bright stars are flagged as cosmic rays.  
  - --gain GAIN               Gain of the image (electrons / ADU). We always need to work in electrons for cosmic ray detection.  
  - --readnoise READNOISE     Read noise of the image (electrons). Used to generate the noise model of the image.  
  - --satlevel SATLEVEL       Saturation level of the image (electrons). This value is used to detect saturated stars and pixels at or above this level are added to the mask.  
  - --niter NITER             Number of iterations of the LA Cosmic algorithm to perform.  
  - --sepmed                  Use the separable median filter instead of the full median filter. The separable median is not identical to the full median filter, but they are approximately the same; the separable median filter is significantly faster and still detects cosmic rays well. Note, this is a performance feature, and not part of the original L.A. Cosmic.  
  - --cleantype CLEANTYPE     Set which clean algorithm is used. Options:  
                              - "median": An unmasked 5x5 median filter.  
                              - "medmask": A masked 5x5 median filter.  
                              - "meanmask": A masked 5x5 mean filter.  
                              - "idw": A masked 5x5 inverse distance weighted interpolation.  
  - --fsmode FSMODE           Method to build the fine structure image. Options:  
                              - "median": Use the median filter in the standard LA Cosmic algorithm.  
                              - "convolve": Convolve the image with the PSF kernel to calculate the fine structure image.  
  - --psfmodel PSFMODEL       Model to use to generate the PSF kernel if `fsmode == ‘convolve’` and `psfk` is None. The current choices are Gaussian and Moffat profiles. "gauss" and "moffat" produce circular PSF kernels. The "gaussx" and "gaussy" produce Gaussian kernels in the x and y directions respectively.  
  - --psffwhm PSFFWHM         Full Width Half Maximum of the PSF to use to generate the kernel.  
  - --psfsize PSFSIZE         Size of the kernel to calculate. Returned kernel will have size `psfsize x psfsize`. `psfsize` should be odd.  
  - --psfbeta PSFBETA         Moffat beta parameter. Only used if `fsmode=="convolve"` and `psfmodel=="moffat"`.  
  - --gain_apply              If True, return gain-corrected data with correct units; otherwise, do not gain-correct the data.  
