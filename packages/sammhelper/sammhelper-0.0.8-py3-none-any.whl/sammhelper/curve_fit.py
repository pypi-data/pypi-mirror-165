import numpy as np
import scipy as sp

def curve_fit(model,data,time,param):

    """
    Compute the 1-D discrete Fourier Transform. 
    
    Args:
        model (callable): Models the data. It must take the independent variable as the first argument and the parameters (as an array) as the second argument.
        data (array): The dependent (measured) data.
        time (array): The independent variable where the data is measured.
        param (array): Parameters of the model
    Returns:
        res.x (array): Optimal values for the parameters so that the sum of the squared residuals between measured and modelled data is minimized.
    """
    
    # Define optimization function
    def fit(param):
        sol = model(time,param)
        return np.linalg.norm(sol[~np.isnan(data)]-data[~np.isnan(data)])

    # Returns initial and parameter values that fit the data perfectly.
    res = sp.optimize.minimize(fit,param)

    return res.x