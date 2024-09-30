.. _cli_rotate:

rotate
======

Rotates the FITS files.

------------

.. method:: im rotate

    **usage**

        im rotate [-h] [--degrees] file angle output

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``angle``    Angle

        ``output``    Output directory



    **options**

        ``-h``, ``--help``  show this help message and exit

        ``--degrees``   Angle is in Degrees


------------

Example:
________

.. code-block:: bash

    im crop /PATH/TO/FILES*.fits 45 /PATH/TO/DIRECTORY --degrees
