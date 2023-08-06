import numpy as np

def fill_array(a, l):

    """
    Fill each row in the two-dimensional (2d) array so that the rows of the array
    have the same length l.

    Args:
        a (2d-array): Input 2d array.
        l (int): Row Length to be filled.

    Returns:
        a (2d-array): The filled 2d array of equal length rows.
    """

    for i in range(len(a)):
        if not (isinstance(a[i], (list, np.ndarray))):
            a[i] =l * [a[i]]

    return a