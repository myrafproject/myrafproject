.. _fits:

Fits
=====

The `Fits` object encapsulates the data and functionalities needed for performing a wide range of astronomical photometry tasks. Designed for simplicity and ease of use, `Fits` eliminates the need for external functions to modify or analyze a FITS file.

The object supports method chaining, meaning most methods return a `Fits` object, either the current one or a new instance. This allows users to chain multiple method calls for a streamlined workflow.

If a method returns a new `Fits` object, it can optionally accept two parameters: `output` and `override`. The `output` parameter is the path to the output file as a string, while `override` specifies whether to overwrite an existing file at the given path. If `output` is not provided or set to `None`, a temporary file will be created and automatically deleted when the object is destroyed (``__del__``).


.. toctree::
   :maxdepth: 1
   :caption: File Operations:

   fits_from_image
   fits_from_path
   fits_from_data_header
   fits_sample
   fits_save_as
   fits_header
   fits_pure_header
   fits_hedit

.. toctree::
   :maxdepth: 1
   :caption: Arithmetic Operations:

   fits_add
   fits_sub
   fits_mul
   fits_div
   fits_pow
   fits_imarith

.. toctree::
   :maxdepth: 1
   :caption: Data Operations:

   fits_data
   fits_value


.. toctree::
   :maxdepth: 1
   :caption: Image Processing:

   fits_ccd
   fits_imstat
   fits_cosmic_clean
   fits_align
   fits_show
   fits_shift
   fits_rotate
   fits_crop
   fits_bin
   fits_zero_correction
   fits_dark_correction
   fits_flat_correction
   fits_ccdproc
   fits_background

.. toctree::
   :maxdepth: 1
   :caption: Coordinate Systems:

   fits_coordinate_picker
   fits_pixels_to_skys
   fits_skys_to_pixels
   fits_map_to_sky

.. toctree::
   :maxdepth: 1
   :caption: Photometry:

   fits_daofind
   fits_extract
   fits_photometry_sep
   fits_photometry_phu
   fits_photometry

.. toctree::
   :maxdepth: 1
   :caption: Advanced Operations:

   fits_solve_field
