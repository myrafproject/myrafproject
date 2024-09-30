.. _cli_map2sky:

map2sky
=======

Converts x-y to sky on the FITS files.

------------

.. method:: im map2sky

    **usage**

         im map2sky [-h] file

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")


    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im map2sky /PATH/TO/FILES*.fits
