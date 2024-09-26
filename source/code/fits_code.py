from myraflib import Fits

fits = Fits.from_path("sample.fits")
fits.hedit(
    ["Ke1y", "Key2"], ["Value1", "Value2"], ["Comment1", "Comment2"]
)

sources = fits.daofind(sigma=1.2)

