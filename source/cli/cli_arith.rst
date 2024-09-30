.. _cli_arith:

arith
=====

Does arithmetic operations of FITS files.

------------

.. method:: im arith

    **usage**

        im arith [-h] file operator other output

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``operator``    Operator \+, \-, \/, \*, \*\*, \^

        ``other``    Fits or Number to Operate

        ``output``    Output directory


    **options**

        ``-h``, ``--help``  show this help message and exit

------------

Example:
________

.. code-block:: bash

    im arith /PATH/TO/FILES*.fits + 200 /PATH/TO/DIRECTORY
