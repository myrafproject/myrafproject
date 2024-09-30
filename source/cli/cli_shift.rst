.. _cli_shift:

shift
=====

Shifts the FITS files.

------------

.. method:: im shift

    **usage**

        im shift [-h] file x y output

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``x``    X component of coordinate

        ``y``    Y component of coordinate

        ``output``    Output directory



    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im shift /PATH/TO/FILES*.fits 100 100 /PATH/TO/DIRECTORY
