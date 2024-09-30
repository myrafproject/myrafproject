.. _cli_value:

value
=====

Returns value of the given coordinate of FITS files.

------------

.. method:: im value

    **usage**

        im value [-h] file x y

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``x``    X component of coordinate

        ``y``    Y component of coordinate



    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im value /PATH/TO/FILES*.fits 10 10
