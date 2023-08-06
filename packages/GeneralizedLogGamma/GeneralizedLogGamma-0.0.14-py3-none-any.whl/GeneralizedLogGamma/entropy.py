"""
Entropy function of a Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import scipy.special as sp
import numpy as np

def entropy_glg(location = 0, scale = 1, shape = 1):       
    inv_shape_2 = 1/shape**2
    output = np.log(sp.gamma(inv_shape_2)/np.abs(shape))
    output = output + inv_shape_2 * (1 - sp.digamma(inv_shape_2))
    output = (1/scale) * (np.log(scale) + output)
    return output

# print(entropy_glg())
# print(entropy_glg(shape=0.077))