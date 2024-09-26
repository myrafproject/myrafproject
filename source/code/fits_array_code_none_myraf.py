import astroalign
from astropy.io import fits
from glob import glob

files = glob("PATTERN/OF/FILES/*.fits")
reference_data = fits.getdata(files[0])

for file in files[1:]:
    with fits.open(file, "update") as hdu:
        for key, value, comment in zip(
                ["Ke1y", "Key2"], ["Value1", "Value2"],
                ["Comment1", "Comment2"]
        ):
            hdu[0].header[key] = value
            hdu[0].header.comments[key] = comment
            hdu.flush()


    data = fits.getdata(file)
    header = fits.getheader(file)
    registered_image, footprint = astroalign.register(
        data, reference_data, max_control_points=50, min_area=5
    )
    # A new fits file creation and WCS correction will not be
    # considered here



