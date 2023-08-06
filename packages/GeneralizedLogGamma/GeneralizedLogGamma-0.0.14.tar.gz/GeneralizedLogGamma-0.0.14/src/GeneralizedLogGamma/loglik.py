"""
Log-likelihood of Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import time
import numpy as np
import scipy.special as ssp

def c_l(shape = 1):
    if (np.abs(shape) < 0.15):
        if (shape > 0):
            shape = 0.15
        else:
            shape = -0.15

    i_shape_two = 1/shape**2
    c = np.abs(shape)/math.gamma(i_shape_two)
    output = c * (i_shape_two**i_shape_two)
    return output

def logLikglg(x, location = 0, scale = 1, shape = 1):
        init = time.time()
        x = np.array(x)
        epsilon = (x - location)/scale
        i_shape = 1/shape
        output = np.log(c_l(shape)/scale) + (i_shape) * epsilon - (i_shape**2) * np.exp(shape * epsilon)
        end = time.time()
        return { 'logLik': output, 'exec_time': end - init } 


#print(logLikglg(x=np.linspace(-4, 4, num = 100)))