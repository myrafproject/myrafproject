.. _fitsarray_from_video:

from_video
==========

This method extracts frames from a video file and creates a ``FitsArray`` object.

------------

.. method:: FitsArray.from_video(cls, path: str, start_time: Optional[Union[Time, float]] = None, logger: Optional[Logger] = None, verbose: bool = False) -> Self

    Creates a ``FitsArray`` from frames of a video.

    **Notes**

    This method extracts frames from a video file and creates a ``FitsArray`` object.

    **Parameters**

        ``path`` : ``str``
            The path of the video file as a string.

        ``start_time`` : ``Optional[Union[Time, float]]``
            The start time of the video. It can be a ``Time`` object or a float representing the start time in seconds.
            If ``None``, the first frame's ``MY_RELJD`` is considered zero (0).

        ``logger`` : ``Optional[Logger]``
            An optional logger for logging messages during the operation.

        ``verbose`` : ``bool``, optional, default=False
            If set to ``True``, additional information will be displayed during processing.

    **Returns**

        ``FitsArray``
            A ``FitsArray`` object containing the frames extracted from the video.

    **Raises**

        ``FileNotFoundError``
            Raised when the specified video file does not exist.


------------

Example:
________

.. code-block:: python

    from myraflib import FitsArray

    fa = FitsArray.from_video("PATH/TO/VIDEO")
