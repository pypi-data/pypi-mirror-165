import numpy as np

def delay(time, var, delay, value = 0):

    """
    This function returns a time array shifted by the delay value

    Args:
        time (array): A sequence of time points.
        var (array): A sequence of values which are shifted in time.
        delay (float): Specified delay time.
        value (float, optional): specified value for var for the delay time
        

    Returns:
        t_delayed (array): Returns a time vector delayed by the delay time with the same length as the time vector.
    """
    DT = time[1]-time[0]
    i_delay = int(round(delay/DT))
        
    var_delayed = np.zeros(len(var))
    var_delayed[0:i_delay] = value
    var_delayed[i_delay:] = var[0:-i_delay]
    
    return var_delayed