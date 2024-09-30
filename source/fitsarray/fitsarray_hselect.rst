.. _fitsarray_hselect:

hselect
=======

Returns a DataFrame containing the specified keys.

------------

.. method:: FitsArray.hselect(self, fields: Union[str, List[str]]) -> pd.DataFrame

    Returns a DataFrame containing the specified keys.

    **Parameters**

        ``fields`` : ``Union[str, List[str]]``
            The fields (keys) to be selected.

    **Returns**

        ``pd.DataFrame``
            A DataFrame containing the header values of the specified keys.



------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    selected_header = fa.hselect(["KEY1", "KEY2"])