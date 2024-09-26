from myraflib import FitsArray

# Create FitsArray
fa = FitsArray.from_pattern("ALL/FILES/*.fits")

# Group files by IMAGETYP in header
groups = fa.group_by("IMAGETYP")

# Separate files by types
light = groups["light"]
zeros = groups["zero"]
darks = groups["dark"]
flats = groups["flat"]

# Create master calibration files
master_zero = zeros.zero_combine()
master_dark = darks.dark_combine()
master_flat = flats.flat_combine()

# Calibrate the data images
# Zero, Dark, and Flat correction
calibrated = light.ccdproc(
    master_zero=master_zero,
    master_dark=master_dark,
    master_flat=master_flat
)

# Align the calibrated images
aligned = calibrated.align()

# Find sources on first fits file
sources = aligned.daofind(index=0, sigma=1.2)

# Do a photometry on found sources
# x coordinates are xcentriod
# y coordinates are ycentriod
# Aperture radii are [10, 20, 30]
photometry = aligned.photometry(
    sources["xcentriod"].to_list(),
    sources["ycentriod"].to_list(), 
    [10, 20, 30]
)
