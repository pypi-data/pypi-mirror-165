import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from .sol_ode import sol_ode
from .get_index import get_index

def curve_fit_ode(model,
    var0,
    t,
    xdata,
    ydata,
    param=None,
    param_var0=None,
    guess0=None,
    bounds=None,
    col_index=-1,
):

    """
    Use non-linear least squares to fit results of ordinary differential
    equations (model), to data.

    Args:
        model (callable(y,t,...)): The function computes the derivative of y at t.
        var0 (array): Initial condition on var.
        t (array): A sequence of time points for which to solve for y. The initial
                    value point should be the first element of this sequence.
        xdata (array): The independent variable where the data is measured.
                                Should usually be an M-length sequence or an
                                (k, M)-shaped array for functions with k predictors,
                                but can actually be any object.
        ydata (array): The dependent data, a length M array - nominally
                                f(xdata, ...).
        param (array, optional): Parameters used in the ode model function.
        param_var0 (array, optional): Parameters used in the initial condition function.

        guess0 (array, optional): Initial guess for the parameters (length N). If None,
                                then the initial values will all be 1 (if the number of
                                parameters for the function can be determined using
                                introspection, otherwise a ValueError is raised).
        bounds (2-tuple of array_like, optional): Lower and upper bounds on parameters.
                                                   Defaults to [0.1*guess0, 1.5*guess0].
        col_index (int, optional): The index of fitted results in the solved dataframe
                                    of the model. The default will be the last column of
                                    the dataframe.

    Returns:
        avg: Optimal values for the parameters so that the sum of the squared residuals
                of f(xdata, *popt) - ydata is minimized.
        std: The estimated covariance of avg. The diagonals provide the variance of the
                parameter estimate.
    """
    
    
    if isinstance(ydata, int) | isinstance(ydata, float):
        ydata = np.array([ydata] * len(xdata))
    
    if xdata[0] != 0:
        xdata.loc[-1] = 0
        xdata.index = xdata.index + 1
        xdata = xdata.sort_index()
        ydata.loc[-1] = np.math.nan
        ydata.index = ydata.index + 1
        ydata = ydata.sort_index()
                         
    try:
        df = sol_ode(model, var0(param_var0), t, param)
    except:
        df = sol_ode(model, var0, t, param)
        
    if isinstance(df,list):
        C = df[col_index]
    else:
        C = df[:,col_index]

    plt.figure(100)
    plt.grid()
    plt.plot(xdata, ydata, 'o', markersize = 2)
    plt.plot(t,C)
    
    # set the default bounds
    if (bounds == None) & (guess0 != None):
        # bounds = (
        #     [-np.inf] * (len(set(guess0))),
        #     [np.inf] * (len(set(guess0))),
        # )

        bounds = np.empty([2, len(guess0)])
        for i in range(len(guess0)):
            if guess0[i] > 0:
                bounds[0][i] = -3 * guess0[i]
                bounds[1][i] = 3 * guess0[i]
            elif guess0[i] == 0:
                bounds[0][i] = -np.inf
                bounds[1][i] = np.inf
            else:
                bounds[0][i] = 3 * guess0[i]
                bounds[1][i] = -3 * guess0[i]

    # identify the index of initial condition's parameters in input guess0
    try:
        p0 = get_index(param_var0, guess0)
        p0_converse = get_index(guess0, param_var0)
    except:
        pass

    # identify the index of ode function's parameters in input guess0
    try:
        p1 = get_index(param, guess0)
        p1_converse = get_index(guess0, param)
    except:
        pass

    # create the fitted function, changing the parameter to making the ode
    # function solved results fitting the input data
    def func(xdata, *args):

        # change the parameter in the ode function
        param_new = param
        for i in range(len(p1)):
            param_new[p1_converse[i]] = args[p1[i]]

        try:
            # change the parameter in the initial condition
            param_var0_new = param_var0
            for i in range(len(p0)):
                param_var0_new[p0_converse[i]] = args[p0[i]]
            # solve the ode function
            results = sol_ode(model, var0(param_var0_new), xdata, param_new)
        except:
            results = sol_ode(model, var0, xdata, param_new)

        # return the solved result
        try:
                return results[:, col_index][~np.isnan(ydata)]
        except:
                return results[col_index][~np.isnan(ydata)]
        
    avg, std = sp.optimize.curve_fit(func, xdata, ydata[~np.isnan(ydata)], p0=guess0, bounds=bounds)
    try:
         df = sol_ode(model, var0(param_var0), t, param)
    except:
         df = sol_ode(model, var0, t, param)
        
    if isinstance(df,list):
        Cnew = df[col_index]
    else:
        Cnew = df[:,col_index]
        
    plt.figure(100)
    plt.plot(t,Cnew)
    plt.legend(["measured data","model","fitted model"])
    plt.show()
    
    print("average:", avg)
    
    return avg, std