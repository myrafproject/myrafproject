.. _cli_align:

align
=====

Aligns the FITS fies.

------------

.. method:: im align

    **usage**

        im align [-h] [--max-control-points MAX_CONTROL_POINTS] [--min-area MIN_AREA] file other output

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

        ``other``                 Fits or index of the reference

        ``output``    Output directory

    **options**

        ``-h``, ``--help``  show this help message and exit

        ``--max-control-points`` MAX_CONTROL_POINTS Maximum number of control points

        ``--min-area`` MIN_AREA   Minimum area

------------

Example:
________

.. code-block:: bash

    im align /PATH/TO/FILES*.fits 0
