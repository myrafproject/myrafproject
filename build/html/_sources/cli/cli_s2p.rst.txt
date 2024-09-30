.. _cli_s2p:

s2p
===

Converts sky to x-y on the FITS files.

------------

.. method:: im s2p

    **usage**

        im s2p [-h] file ra dec

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``ra``          Right ascension in degrees
        ``dec``         Declination in degrees




    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im s2p /PATH/TO/FILES*.fits 305.112983392782 4.833096450290802
