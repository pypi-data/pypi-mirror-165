import matplotlib.pyplot as plt
from .sol_ode import sol_ode
from .get_index import get_index


def sensitivity(var, xlabel="time", model=None, var0=None, t =None, param=None, param_var0=None, col_index = -1):
    
    """
    The sensitivity function computes the sensitivity of the results of the model
    to changing parameters. Run the model with all parameters at their specified
    values and get the results R1(t). Adjust parameter Par slightly by adding an
    amount ∆ equal to 0.0001 * Par. Run the model again, calling the results R2(t).
    Compute the sensitivity S(t) by the following formula: S(t) = (R2(t) - R1(t)) / ∆

    Args:
        par (float): Value of parameter.
        xlabel (str): Identify the xlabel of results. There are two options: time or
                        length. The time means the results changing with time. The length
                        means the results changing with the reactor series.
        model (callable(y,t,...)): The function computes the derivative of y at t.
        var0 (array): Initial condition on y.
        t (array): A sequence of time points for which to solve for y. The initial
                    value point should be the first element of this sequence.
        param (array, optional): Parameters used in the ode model function.
        param_var0 (array, optional): Parameters used in the initial condition function.
        col_index (integer, optional): if two variables (e.g. X,S) returns Sensitivity of the last, if not defined differently. 

    Returns:
        array:  Sensitivity of solved results to parameter - par.
    """
    if param_var0 != None:

        # solve the ode function using the initial input parameter
        C = sol_ode(model, var0(param_var0), t, param)

        # times the parameter with 1.0001
        param_var0_new = param_var0
        param_new = param
        if var in param_var0:
            index = get_index(var, param_var0)
            param_var0_new[index[0]] = 1.0001 * var
        if var in param:
            index = get_index(var, param)
            param_new[index[0]] = 1.0001 * var

        # solve the ode function using the changed parameter
        C_sens = sol_ode(model, var0(param_var0_new), t, param_new)
    else:
        # solve the ode function using the initial input parameter
        C = sol_ode(model, var0, t, param)

        # times the parameter with 1.0001
        param_new = param

        if var in param:
            index = get_index(var, param)
            param_new[index[0]] = 1.0001 * var

        # solve the ode function using the changed parameter
        C_sens = sol_ode(model, var0, t, param_new)
    # calculate the sensitivity of the parameter along the time or length
    if xlabel == "time":
        try:
            result = var*(C_sens - C) / (0.0001 * var)
        except:
            result = var*(C_sens[col_index]- C[col_index])/(0.0001 * var)
        
        # plot the results
        plt.figure(10)
        plt.grid()
        plt.xlabel("Time [min]")
        plt.ylabel("Absolute-relative Sensitivity")
        try:
            plt.plot(t,result[:,-1])
        except:
            plt.plot(t,result)
        plt.show()
        
        return result
    elif xlabel == "length":
        
        result = var*(C_sens[-1,:] - C[-1,:]) / (0.0001 * var)
        
        # plot the results
        plt.figure(10)
        plt.grid()
        plt.xlabel("Length [i]")
        plt.ylabel("Absolute-relative Sensitivity")
        plt.plot(range(len(result)),result)
        plt.show()
        return result