import numpy as np

def limit(a, a_min):

    """
    Limit the values in an array or one value.

    Args:
        a (array_like or float): Array containing elements to clip or elements to
                                 clip.
        a_min (array_like or None): Minimum value in the clipped list or the clipped
                                    value.

    Returns:
        array_like: An array with the elements of a, but where values < a_min are
                    replaced with a_min.
    """

    # limit the value with int or float type
    if isinstance(a, float) or isinstance(a, int):
        return a if a > a_min else a_min

    else:
        # check if the given minimum value larger than the maximum value in the array.
        if max(a) > a_min:
            a_max = max(a)
        else:
            a_max = a_min
        return np.clip(a, a_min, a_max)