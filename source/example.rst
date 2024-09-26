.. _example:

Examples
========

Here, we present some examples illustrating the functionalities of both the ``Fits`` and ``FitsArray`` classes.

Fits
----

In this example, we demonstrate the process of updating the header of a FITS file and retrieving a list of coordinates of sources from the data.

.. literalinclude:: code/fits_code.py
   :language: python
   :caption: ``Fits`` updates header and finds sources on data of a FITS file.
   :name: lst_fits_code

The same goal can be achieved using ``Astropy`` and ``photutils`` as shown in the following example:

.. literalinclude:: code/fits_code_none_myraf.py
   :language: python
   :caption: Updating header and finding sources on data of a FITS file.
   :name: lst_fits_code_none_myraf


FitsArray
---------

As mentioned before, ``FitsArray`` can perform operations on multiple FITS files. Below is an example where we update the header and align multiple FITS files.

.. literalinclude:: code/fits_array_code.py
   :language: python
   :caption: ``FitsArray`` updates header and aligns multiple FITS files.
   :name: lst_fits_array_code

The same goal can be achieved using ``Astropy`` and ``AstroAlign``:

.. literalinclude:: code/fits_array_code_none_myraf.py
   :language: python
   :caption: Updating header and aligning multiple FITS files.
   :name: lst_fits_array_code_none_myraf

The code demonstrating how to perform operations without ``MYRaf`` essentially reflects the processes that ``MYRaf`` executes internally. ``MYRaf`` simplifies these operations by making them more human-readable and writable, while maintaining the same underlying functionality.

Video
-----

The ``FitsArray`` class extends its functionality to support the importation of video files. By utilizing the ``FitsArray.from_video`` class method, users can decompose a video into individual frames, with each frame being assigned corresponding time and exposure metadata in the FITS header. This feature has demonstrated significant utility, particularly in the context of occultation observations.

Photometry
----------

In theory, the following example is capable of performing both calibration and photometry on a given list of FITS files, even when the calibration data and image data are not stored separately.

.. literalinclude:: code/fits_array_photometry.py
   :language: python
   :caption: Photometry With ``MYRaf``.
   :name: lst_fits_array_photometry
