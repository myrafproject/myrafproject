.. _fitsarray_bin:

bin
===

Bins the data of the ``FitsArray`` object.

------------

.. method:: FitsArray.bin(self, binning_factor: Union[int, List[int]], func: Callable[[Any], float] = np.mean, output: Optional[str] = None) -> Self

    Bins the data of the ``FitsArray`` object.

    **Parameters**

        ``binning_factor`` : ``Union[int, List[Union[int, List[int]]]]``
            Binning factor.

        ``func`` : ``Callable[[Any], float]``, default ``np.mean``
            The function to be used for merging values during binning.

        ``output`` : ``Optional[str]``
            New path to save the files.

    **Returns**

        ``FitsArray``
            A binned ``FitsArray`` object.

    **Raises**

        ``ValueError``
            When the ``binning_factor`` is invalid.

        ``ValueError``
            When the ``binning_factor`` is too large.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray
    import math

    fa = FitsArray.sample()

    cropped_fa_1 = fa.bin(10)
    cropped_fa_2 = fa.bin([10, 20])
