import numpy as np

def len_check(a):

    """
    Get the maximum row length in a two-dimensional array.

    Args:
        a (2d-array): Input 2d array.

    Returns:
        max_len (int): Maximum row length in 2d-array, a.
    """

    max_len = 0
    for item in a:
        if isinstance(item, (list, np.ndarray)):
            if len(item) > max_len:
                max_len = len(item)

    return max_len