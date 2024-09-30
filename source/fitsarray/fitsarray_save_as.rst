.. _fitsarray_save_as:

save_as
=======
Saves the ``FitsArray`` to the specified output.

------------

.. method:: FitsArray.save_as(self, output: str) -> Self

    Saves the ``FitsArray`` to the specified output.

    **Parameters**

        ``output`` : ``str``
            The new path to save the file.

    **Returns**

        ``FitsArray``
            A new ``FitsArray`` object representing the saved data.

    **Raises**

        ``NumberOfElementError``
            Raised when the number of FITS files is 0.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    saved_fa = fa.save_as("PATH/TO/DIRECTORY/")