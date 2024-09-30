.. _cl:


CLI
===

``MYRaf`` also includes a command-line interface (CLI), which, while capable of performing basic operations, does not fully encompass the extensive functionalities of the ``MYRaf`` library. Additionally, the CLI lacks the computational power and flexibility inherent to Python programming.

The ``MYRaf`` CLI is invoked using the command ``im``. This command is further subdivided into various subcommands, each of which has its own set of positional and optional arguments tailored to specific tasks.

The CLI proves particularly useful for executing simple operations directly from the terminal, providing a convenient alternative for certain tasks.


.. method:: im Subcommand

    **usage**

        im [-h] {header, hedit, arith, value, stat, bin, crop, rotate, shift, clean, show, align, p2s, s2p, map2sky} ...

    **positional arguments**

        ``file``        A file path or pattern (e.g., "\*.fits")

    **subcommands**

        ``header``, ``hedit``, ``arith``, ``value``, ``stat``, ``bin``, ``crop``, ``rotate``, ``shift``, ``clean``, ``show``, ``align``, ``p2s``, ``s2p``, ``map2sky``

    **options**

        ``-h``, ``--help``  show this help message and exit


.. toctree::
   :maxdepth: 1
   :caption: Available Subcommands:

   cli_header
   cli_hedit
   cli_arith
   cli_value
   cli_stat
   cli_bin
   cli_crop
   cli_rotate
   cli_shift
   cli_clean
   cli_show
   cli_align
   cli_p2s
   cli_s2p
   cli_map2sky
