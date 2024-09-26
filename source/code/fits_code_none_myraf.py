from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder

with fits.open("sample.fits", "update") as hdu:
    for key, value, comment in zip(
            ["Ke1y", "Key2"], ["Value1", "Value2"],
            ["Comment1", "Comment2"]
    ):
        hdu[0].header[key] = value
        hdu[0].header.comments[key] = comment

    hdu.flush()

data = fits.getdata("sample.fits")
mean, median, std = sigma_clipped_stats(data, sigma=1.2)
daofind = DAOStarFinder(fwhm=3.0, threshold=3.0 * std)
sources = daofind(data - median)

