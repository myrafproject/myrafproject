FitsArray
=========

The ``FitsArray`` object, similar to the ``Fits`` object, provides all the necessary data and functionalities for handling multiple FITS files in photometry. It supports everything available in ``Fits`` and includes additional methods, such as ``combine`` and ``hselect``.

As with ``Fits``, if a method returns a new ``FitsArray`` object, it can optionally accept an ``output`` parameter. This parameter specifies the path to the output directory as a string, where files will be saved. There is no ``override`` option. If the ``output`` parameter is not provided or set to ``None``, a temporary directory will be created. The contents of this temporary directory will be automatically deleted when the object is destroyed (``__del__``).

.. toctree::
   :maxdepth: 1
   :caption: File Operations:

   fitsarray_from_video
   fitsarray_from_paths
   fitsarray_from_pattern
   fitsarray_sample
   fitsarray_files
   fitsarray_save_as
   fitsarray_header
   fitsarray_pure_header
   fitsarray_hedit
   fitsarray_merge
   fitsarray_append

.. toctree::
   :maxdepth: 1
   :caption: Arithmetic Operations:

   fitsarray_add
   fitsarray_sub
   fitsarray_mul
   fitsarray_div
   fitsarray_pow
   fitsarray_imarith

.. toctree::
   :maxdepth: 1
   :caption: Data Operations:

   fitsarray_data
   fitsarray_value


.. toctree::
   :maxdepth: 1
   :caption: Image Processing:


   fitsarray_ccd
   fitsarray_imstat
   fitsarray_hselect
   fitsarray_shift
   fitsarray_rotate
   fitsarray_crop
   fitsarray_bin
   fitsarray_align
   fitsarray_zero_correction
   fitsarray_dark_correction
   fitsarray_flat_correction
   fitsarray_ccdproc
   fitsarray_background
   fitsarray_photometry_sep
   fitsarray_photometry_phu
   fitsarray_photometry
   fitsarray_cosmic_clean
   fitsarray_show
   fitsarray_combine
   fitsarray_zero_combine
   fitsarray_dark_combine
   fitsarray_flat_combine


.. toctree::
   :maxdepth: 1
   :caption: Coordinate Systems:

   fitsarray_pixels_to_skys
   fitsarray_skys_to_pixels
   fitsarray_map_to_sky


.. toctree::
   :maxdepth: 1
   :caption: Photometry:

   fitsarray_daofind
   fitsarray_extract


.. toctree::
   :maxdepth: 1
   :caption: Advanced Operations:

   fitsarray_solve_field
   fitsarray_group_by
