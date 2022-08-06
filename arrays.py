import numpy as np


def trim_zeros(array, margin=0):
    """
    Trim the leading and trailing zeros from an N-dimensional array.

    :param array: numpy array
    :param margin: how many zeros to leave as a margin
    :returns: trimmed array
    """
    index = []
    for dim in range(array.ndim):
        start = 0
        end = -1
        slice_ = [slice(None)] * array.ndim

        go = True
        while go:
            slice_[dim] = start
            go = not np.any(array[tuple(slice_)])
            start += 1
        start = max(start-1-margin, 0)

        go = True
        while go:
            slice_[dim] = end
            go = not np.any(array[tuple(slice_)])
            end -= 1
        end = array.shape[dim] + min(-1, end + 1 + margin) + 1

        index.append(slice(start, end))
    return array[tuple(index)]
