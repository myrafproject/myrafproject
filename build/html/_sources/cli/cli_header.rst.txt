.. _cli_header:

header
======

Gets headers of the given FITS files.

------------

.. method:: im header

    **usage**

        im header [-h] file

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

    **options**

        ``-h``, ``--help``  show this help message and exit



------------

Example:
________

.. code-block:: bash

    im header /PATH/TO/FILES*.fits
