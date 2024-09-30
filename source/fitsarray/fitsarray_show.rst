.. _fitsarray_show:

show
====

Shows the images using matplotlib.

------------

.. method:: FitsArray.show(scale: bool = True, interval: float = 1.0) -> None

    Shows the images using matplotlib.

    **Parameters**

        ``scale`` : ``bool``, optional
            Scales the image if True.

        ``interval`` : ``float``, default=1.0
            The interval of the animation in seconds.

------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.sample()
    fa.show()
