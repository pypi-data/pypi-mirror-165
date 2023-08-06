def two_position(x, y, xlimit, ylimit):

    """
    This function compares the value of the measured element with limits and
    generates an adjusted output of the control element. The output value of
    the control element is in the range of setpoints.

    Args:
        x (float, optional): Measured element.
        y (float, optional): Control element.
        xmin (int, optional): Lower setpoint for measured element.
        xmax (int, optional): Upper setpoint for measured element.
        ymin (int, optional): Lower setpoint for control element.
        ymax (int, optional): Upper setpoint for control element.

    Returns:
        y (float, optional): Control elements after adjusted.
    """

    if x > xlimit[-1]:
        y = ylimit[-1]
    elif x < xlimit[0]:
        y = ylimit[0]

    return y