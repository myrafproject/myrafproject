.. _fits_bin:

fits_bin
========

Bins the data of the ``Fits`` object.

------------

.. method:: Fits.bin(binning_factor: Union[int, List[int]], func: Callable[[Any], float] = np.mean, output: Optional[str] = None, override: bool = False) -> Self

    Bins the data of the ``Fits`` object.

    **Parameters**

        - **binning_factor** (``Union[int, List[int]]``):
            The binning factor to reduce the data.

        - **func** (``Callable[[Any], float]``, default: ``np.mean``):
            The function to be applied to the binned data (e.g., ``np.mean``, ``np.sum``, etc.).

        - **output** (``str, optional``):
            Path of the new fits file where the binned data will be saved.

        - **override** (``bool, default=False``):
            If ``True``, will overwrite the output if a file with the same name already exists.

    **Returns**

        ``Fits``
            A binned ``Fits`` object.

    **Raises**

        - **ValueError**
            When the ``binning_factor`` is invalid.

        - **ValueError**
            When the ``binning_factor`` is too large for the data dimensions.




------------

Example:
________

.. code-block:: python

    from myraflib import Fits

    fits = Fits.sample()
    binned_fits = Fits.bin(10)
