.. _understanding:

Understanding
=====================================

Once a ``Fits`` object is created, it allows for various operations on both the data and header. Each operation performed on the data returns a new ``Fits`` object, ensuring file integrity and enabling method chaining. These operations accept two keyword arguments: ``output`` and ``override``. If the ``output`` argument is specified with a file path, a new FITS file will be created at that location. The ``override`` argument is a flag that allows overwriting the file if it already exists. If the ``output`` argument is not provided, a temporary file is created, which is automatically deleted when the ``Fits`` object is garbage collected.

``FitsArray`` is designed as a wrapper for managing multiple ``Fits`` objects. It retains all the functionalities of the ``Fits`` class, while introducing additional features that apply to multiple FITS files, such as combining data and other operations suited for batch processing. This allows users to efficiently handle and manipulate collections of FITS files with the same ease and flexibility offered by the ``Fits`` class for individual files.
