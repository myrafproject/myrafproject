# FitsArray

[Fits](myraf_fits.md)

## Create
How to create a `FitsArray` object.

```python
from myraflib import Fits, FitsArray
from pathlib import Path

file_names = ["SOME_FILE_PATH1", "SOME_FILE_PATH2"]

fits_array = FitsArray([Fits(Path(file_name)) for file_name in file_names])
```

or

```python
from myraflib import FitsArray

file_names = ["SOME_FILE_PATH1", "SOME_FILE_PATH2"]

fits_array = FitsArray.from_paths(file_names)
```

or

```python
from myraflib import FitsArray

fits_array = FitsArray.from_pattern("./*.fits")
```

## Sample
Creates a sample fits array

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()
```

## merge
Merges two FitsArrays

```python
from myraflib import FitsArray

fits_array1 = FitsArray.sample()
fits_array2 = FitsArray.sample()

merged_array = fits_array2.merge(fits_array2)
```

## append
Appends a Fits to FitsArrays

```python
from myraflib import Fits, FitsArray

fits_array = FitsArray.sample()
fits = Fits.sample()

merged_array = fits_array.append(fits)
```

## header
Returns headers of all fits as an astropy table

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

headers = fits_array.header
```

## ccd
Returns CCDData of all fits as a list of CCDData

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

ccds = fits_array.ccd
```

## value
Returns values of the given x and y of all fits as an astropy table

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

values = fits_array.value(10, 10)
```

## files
Returns a list of absolute paths as string

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

paths = fits_array.files
```

## stats
Returns statistics of all fits files as an astropy table

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

stats = fits_array.stats
```

## background
Returns background (sep.Background) of all fits as an iterator

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

background_iterator = fits_array.background()
```

## cosmic_cleaner
Cleans all fits from cosmic rays (`cosmicray_lacosmic`)

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

clean_fits_array = fits_array.cosmic_cleaner()
```

## hedit
Edits the headers (add, update, deleter)


```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

fits_array.hedit(keys="key", values="value", delete=False, value_is_key=False)
```

## hselect
Returns all selected header keys values as an astropy table


```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

selected_headers_table = fits_array.hselect("key")
```

## save
Saves all fits the given folder with the same name


```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

new_fits_array = fits_array.sample("NEW_PATH")
```


## show
Animates all fits files using (matplotlib)

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

fits_array.show()
```

## group_by
Groups all fits files with given header values

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

grouped_fits_array = fits_array.group_by(["FILTER", "IMAGETYP"])
```

## combine
Combines all fits files into one fits

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

fits = fits_array.combine("average")
```

## zero_combine
A combine method specialized on Zero Combine

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

fits = fits_array.zero_combine("average")
```

## dark_combine
A combine method specialized on Dark Combine

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

fits = fits_array.dark_combine("average")
```
## flat_combine
A combine method specialized on Flat Combine

```python
from myraflib import FitsArray

fits_array = FitsArray.sample()

fits = fits_array.flat_combine("average")
```

## zero_correction
Does zero correction on all fits files

```python
from myraflib import Fits, FitsArray

fits_array = FitsArray.sample()
master_zero = Fits.sample()

zero_corrected = fits_array.zero_correction(master_zero)
```

## dark_correction
Does dark correction on all fits files

```python
from myraflib import Fits, FitsArray

fits_array = FitsArray.sample()
master_dark = Fits.sample()

zero_corrected = fits_array.dark_correction(master_dark)
```

## flat_correction
Does flat correction on all fits files

```python
from myraflib import Fits, FitsArray

fits_array = FitsArray.sample()
master_flat = Fits.sample()

flat_corrected = fits_array.flat_correction(master_flat)
```

## abs
[see Fits.abs](myraf_fits.md#abs)

## add
[see Fits.add](myraf_fits.md#add)

## sub
[see Fits.sub](myraf_fits.md#sub)

## mul
[see Fits.mul](myraf_fits.md#mul)

## div
[see Fits.div](myraf_fits.md#div)

## pow
[see Fits.pow](myraf_fits.md#pow)

## mod
[see Fits.mod](myraf_fits.md#mod)

## imarith
[see Fits.imarith](myraf_fits.md#imarith)

## extract
[see Fits.extract](myraf_fits.md#extract)

## daofind
[see Fits.daofind](myraf_fits.md#daofind)

## align
[see Fits.align](myraf_fits.md#align)

## shift
[see Fits.shift](myraf_fits.md#shift)

## rotate
[see Fits.rotate](myraf_fits.md#rotate)

## crop
[see Fits.crop](myraf_fits.md#crop)

## bin
[see Fits.bin](myraf_fits.md#bin)

## photometry_sep
[see Fits.photometry_sep](myraf_fits.md#photometry_sep)

## photometry_phu
[see Fits.photometry_phu](myraf_fits.md#photometry_phu)

## photometry
[see Fits.photometry](myraf_fits.md#photometry)

## pixels_to_skys
[see Fits.pixels_to_skys](myraf_fits.md#pixels_to_skys)

## skys_to_pixels
[see Fits.skys_to_pixels](myraf_fits.md#skys_to_pixels)

