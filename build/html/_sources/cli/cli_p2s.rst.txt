.. _cli_p2s:

p2s
===

Converts x-y to sky on the FITS files.

------------

.. method:: im p2s

    **usage**

        im p2s [-h] file x y

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

    im p2s /PATH/TO/FILES*.fits 100 100
