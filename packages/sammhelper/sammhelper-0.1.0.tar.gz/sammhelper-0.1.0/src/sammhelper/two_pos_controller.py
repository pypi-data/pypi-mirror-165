import numpy as np
import tqdm as tq

from .sol_ode import sol_ode
from .delay import delay
from .two_position import two_position

def two_pos_controller(model, var0, t, param, Tt, xlimit, ylimit, x_index = -1, y_index = 0):
    
    """
    Create a two position controller to adjust the parameter of input ode function,
    calculate the dataframe using the adjusted parameter.

    Args:
        model (callable(y,t,...)): The function computes the derivative of y at t.
        time (array): A sequence of time points for which to solve for y . The initial
                      value point should be the first element of this sequence.
        xlimit (list): Setpoints for measured element.
        ylimit (list): Setpoints for control element.
        Tt (float): Specified dead time.
        x_index (int, optional): The column index of control element in the
                                     solved dataframe. Default to -1.
        y_index (int, optional): Number of control element. Default to 0.

    Returns:
        results: The solved differential equation using adjusted control element.
        y_final: The log of the adjusted control element.
    """
    
    # create the y value list with initial value.
    y = ylimit[0]
    y_final = np.zeros(len(t))
    x = np.zeros(len(t))

    # empty dataframe for saving results
    results = list(range(len(t)))

    #  store the value calculated from last time.
    for i in tq.tqdm(range(len(t)),position=0,leave=True):
        
        y_final[i] = y
        param[y_index] = y

        #   get the solved results and get the new kla
        df = sol_ode(model, var0, t[i:i+2], param)

        # save the solved results, drop the duplicated value with the same time index,
        # only keeping the last one.
        
        results[i] = np.transpose(df)[-1]
        var0 = np.transpose(df)[-1]
        x[i] = df[x_index][-1]
        
        if Tt != 0:
            x_delay = delay(t, x, Tt, value = 0)

        else:
            x_delay = results

        # control the y value by teo position controller.
        y = two_position(x_delay[i], y, xlimit, ylimit)
        
    return np.transpose(results), y_final