import numpy as np
import scipy as sp

def fft(data):

    """
    Compute the 1-D discrete Fourier Transform. 
    
    Args:
        data (dataframe): The dataframe with two columns, time and value
    Returns:
        frq (array): x-axis of the descrete frequency spectrum 
        amp (array): y-axis of the descrete frequency spectrum 
    """

    # acess data frame
    x = data.iloc[:, 0]
    y = data.iloc[:, 1]
    
    # sampling interval
    si = np.median(np.diff(x))
    
    # sampling frequency
    sf = 1/si
    
    # frequencies (x-axis)
    N = len(y)
    k = np.arange(int(N/2))
    p  = N/sf
    frq = k/p
    
    # amplitude (y-axis)
    amp = sp.fft.fft(y)
    
    # normalize amplitude
    amp = abs(amp/len(y)*2)
    amp[0] = amp[0]/2
    
    # exclude sampling frequency from amplitude
    amp = amp[range(int(len(y)/2))]
    
    # output
    return frq, amp