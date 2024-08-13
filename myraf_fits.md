# Fits

[FitsArray](myraf_fits_array.md)

## Create
How to create a `Fits` object.

```python
from myraflib import Fits
from pathlib import Path

file_name = "SOME_FILE_PATH"

fits = Fits(Path(file_name))
```

or

```python
from myraflib import Fits

file_name = "SOME_FILE_PATH"

fits = Fits.from_path(file_name)
```

You can create a sample file without having a fits file.

```python
from myraflib import Fits

fits = Fits.sample()
```

## ccd
Returns the CCDData of the fits:

```python
from myraflib import Fits

fits = Fits.sample()

ccd_data = fits.ccd
```

## data
Returns the data as np.ndarray of the fits:

```python
from myraflib import Fits

fits = Fits.sample()

ccd_data = fits.data
```

## value
Returns the value of a given pixel

```python
from myraflib import Fits

fits = Fits.sample()

ccd_data = fits.value(120, 120)
```

## header
Returns the header of the given fits

```python
from myraflib import Fits

fits = Fits.sample()

ccd_data = fits.header
```

## stats
Returns the statistics of the given fits

```python
from myraflib import Fits

fits = Fits.sample()

stats = fits.stats
```

## background
Returns the background (sep.Background) of the given fits

```python
from myraflib import Fits

fits = Fits.sample()

background = fits.background()
```

## cosmic_cleaner
Returns the fits from cosmic rays. (`cosmicray_lacosmic`)

```python
from myraflib import Fits

fits = Fits.sample()

clean_fits = fits.cosmic_cleaner()
```

## hedit
Edits the header (add, update, deleter)

```python
from myraflib import Fits

fits = Fits.sample()

fits.hedit(keys="key", values="value", delete=False, value_is_key=False)
```

## save
Saves the fits file (save as)

```python
from myraflib import Fits

fits = Fits.sample()

new_fits = fits.save("NEW_PATH")
```

## abs
Returns absolute value of the fits

```python
from myraflib import Fits

fits = Fits.sample()

abs_fits = fits.abs() # also `abs(fits)`
```

## add
Adds numeric value or another fits.

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

added_fits = fits.add(3) # also `fits + 3`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

added_fits = fits.add(other_fits) # also `fits + other_fits`
```


## sub
Subtracts a numeric value or another fits.

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

subtracted_fits = fits.sub(3) # also `fits - 3`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

subtracted_fits = fits.sub(other_fits) # also `fits - other_fits`
```


## mul
Multiplies a numeric value or another fits.

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

multiplied_fits = fits.mul(3) # also `fits * 3`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

multiplied_fits = fits.mul(other_fits) # also `fits * other_fits`
```


## div
Divides a numeric value or another fits.

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

divided_fits = fits.div(3) # also `fits / 3`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

divided_fits = fits.div(other_fits) # also `fits / other_fits`
```


## pow
Raises the fits to a numeric value or another fits.

Be aware of integer overflow

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

raised_fits = fits.pow(3) # also `fits**3`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

raised_fits = fits.pow(other_fits) # also `fits ** other_fits`
```


## mod
Modular arithmetic by numeric value or another fits.

Be aware of integer overflow

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

mod_fits = fits.mod(3) # also `fits % 3`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

mod_fits = fits.mod(other_fits) # also `fits % other_fits`
```
### imarith
Does all available arithmetic operations

### Numeric
```python
from myraflib import Fits

fits = Fits.sample()

added_fits = fits.imarith(3, "+") # Same as `fits.add(3)`
subtracted_fits = fits.imarith(3, "-") # Same as `fits.sub(3)`
multiplied_fits = fits.imarith(3, "*") # Same as `fits.mul(3)`
divided_fits = fits.imarith(3, "/") # Same as `fits.div(3)`
raised_fits = fits.imarith(3, "**") # either "**" or "^". Same as `fits.pow(3)`
mod_fits = fits.imarith(3, "%") # Same as `fits.mod(3)`
```

### fits
```python
from myraflib import Fits

fits = Fits.sample()
other_fits = Fits.sample()

added_fits = fits.imarith(other_fits, "+") # Same as `fits.add(other_fits)`
subtracted_fits = fits.imarith(other_fits, "-") # Same as `fits.sub(other_fits)`
multiplied_fits = fits.imarith(other_fits, "*") # Same as `fits.mul(other_fits)`
divided_fits = fits.imarith(other_fits, "/") # Same as `fits.div(other_fits)`
raised_fits = fits.imarith(other_fits, "**") # either "**" or "^". Same as `fits.pow(other_fits)`
mod_fits = fits.imarith(other_fits, "%") # Same as `fits.mod(other_fits)`
```

### extract
Extracts sources on the fits file using `sep_extract`.
```python
from myraflib import Fits

fits = Fits.sample()

sources = fits.extract()
```

### daofind
Extracts sources on the fits file using `daofind`.
```python
from myraflib import Fits

fits = Fits.sample()

sources = fits.daofind()
```

### align
Aligns the fits with the given reference

```python
from myraflib import Fits

fits = Fits.sample()
reference = Fits.sample()

aligned = fits.align(reference)
```

### show
Shows the fits file image using `matplotlib`

```python
from myraflib import Fits

fits = Fits.sample()

fits.show()
```

### coordinate_picker
Shows the fits file image using `matplotlib` and lets use to pick coordinates on the image

```python
from myraflib import Fits

fits = Fits.sample()

sources = fits.coordinate_picker()
```

### shift
Shifts the image by the given amount

```python
from myraflib import Fits

fits = Fits.sample()

shifted_fits = fits.shift(100, 100)
```

### rotate
Rotates the image by the given amount. (In radians)

```python
from myraflib import Fits

fits = Fits.sample()

rotated_fits = fits.rotate(3.1415/3)
```

### crop
Crops the image by given window (position of the top left lower corner and width and height)

```python
from myraflib import Fits

fits = Fits.sample()

cropped_fits = fits.crop(10, 10, 10, 10)
```

### bin
Bins the image by given value

```python
from myraflib import Fits

fits = Fits.sample()

binned_fits = fits.bin(10)
```

### zero_correction
Zero Corrects the image by given master zero

```python
from myraflib import Fits

fits = Fits.sample()
master_zero = Fits.sample()

zero_corrected_fits = fits.zero_correction(master_zero)
```

### dark_correction
Dark Corrects the image by given master zero

```python
from myraflib import Fits

fits = Fits.sample()
master_dark = Fits.sample()

dark_corrected_fits = fits.dark_correction(master_dark)
```

### flat_correction
Flat Corrects the image by given master zero

```python
from myraflib import Fits

fits = Fits.sample()
master_flat = Fits.sample()

flat_corrected_fits = fits.flat_correction(master_flat)
```

### pixels_to_skys
Converts the numeric pixel values to SkyCoords if WCS is available

```python
from myraflib import Fits

fits = Fits.sample()

skys = fits.pixels_to_skys(10, 10)
```

### skys_to_pixels
Converts the SkyCoords to numeric pixel values if WCS is available

```python
from myraflib import Fits
from astropy.coordinates import SkyCoord

fits = Fits.sample()

skys = SkyCoord()

pixels = fits.skys_to_pixels(skys)
```

### photometry_sep
Does photometry using `sep.sum_circle`

```python
from myraflib import Fits

fits = Fits.sample()

phot_sep = fits.photometry_sep(10, 10, 10)
```

### photometry_phu
Does photometry using `photutils.aperture_photometry`

```python
from myraflib import Fits

fits = Fits.sample()

phot_phu = fits.photometry_phu(10, 10, 10)
```

### photometry
Does photometry using both `sep.sum_circle` and `photutils.aperture_photometry`

```python
from myraflib import Fits

fits = Fits.sample()

phot = fits.photometry(10, 10, 10)
```


