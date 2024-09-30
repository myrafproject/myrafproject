.. _cli_crop:

crop
====

Crops the FITS files.

------------

.. method:: im crop

    **usage**

        im crop [-h] file x y w h output

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``x``    X component of coordinate

        ``y``    Y component of coordinate

        ``w``    Width of bounding box

        ``h``    Height of bounding box

        ``output``    Output directory



    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im crop /PATH/TO/FILES*.fits 100 100 200 200 /PATH/TO/DIRECTORY
