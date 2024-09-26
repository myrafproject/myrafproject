.. _cli:

CLI
===

``MYRaf`` also includes a command-line interface (CLI), which, while capable of performing basic operations, does not fully encompass the extensive functionalities of the ``MYRaf`` library. Additionally, the CLI lacks the computational power and flexibility inherent to Python programming.

The ``MYRaf`` CLI is invoked using the command ``im``. This command is further subdivided into various subcommands, each of which has its own set of positional and optional arguments tailored to specific tasks.

The CLI proves particularly useful for executing simple operations directly from the terminal, providing a convenient alternative for certain tasks. Examples of such operations include:

CLI Example
-----------

The following example demonstrates how to retrieve the headers from all FITS files within a specified directory and output them in JSON format . This method enables efficient extraction and organization of metadata from multiple files, facilitating further analysis or integration with other systems.

.. code-block:: shell
   :caption: Get all headers using ``im``
   :name: lst_im_header

   im header *.fits

The following example illustrates a command-line operation that allows for the batch update of headers in all FITS files located in the current directory . Specifically, this process inserts or updates the header card ``"MYRAF"`` with the value ``"test"`` across all available FITS files.

.. code-block:: shell
   :caption: Update a header using ``im``
   :name: lst_im_hedit

   im hedit *.fits MYRAF --value test

Help documentation is available for the ``im`` command and its subcommands. Users can easily access detailed information for any command by appending the ``-h`` option, as in ``im -h``, to receive a description of available arguments and functionalities.
