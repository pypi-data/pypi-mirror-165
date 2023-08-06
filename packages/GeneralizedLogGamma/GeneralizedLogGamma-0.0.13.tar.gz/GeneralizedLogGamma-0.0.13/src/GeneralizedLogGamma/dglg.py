"""
Density function of Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import numpy as np

def dglg(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    if abs(shape) < 0.1:
        if shape > 0: 
            shape = 0.1
        else:
            shape = -0.1
    inv_shape = 1/shape        
    inv_shape_2 = inv_shape**2
    cl_shape = (np.abs(shape)/math.gamma(inv_shape_2))*(inv_shape_2)

    y = (x - location)/scale
    output = (inv_shape)*y - (inv_shape_2)*np.exp(shape*y)
    output = np.exp(output)
    output = cl_shape*output/scale
    return output

# print(dglg(x = [0,1,2]))