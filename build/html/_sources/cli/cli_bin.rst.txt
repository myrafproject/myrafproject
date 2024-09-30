.. _cli_bin:

bin
===

Bins the given FITS files.

------------

.. method:: im bin

    **usage**

        im bin [-h] file x y output

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``x``    X amount

        ``y``    Y amount

        ``output``    Output directory


    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im bin /PATH/TO/FILES*.fits 10 10 /PATH/TO/DIRECTORY
