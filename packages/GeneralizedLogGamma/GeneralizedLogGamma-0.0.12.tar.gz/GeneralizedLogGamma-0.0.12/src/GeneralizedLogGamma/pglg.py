"""
Cumulative distribution function of Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import numpy as np
from scipy.special import gammainc

def pglg(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    y = (x - location)/scale
    sh_2 = shape**2
    out = gammainc( 1/sh_2, (1/sh_2)*np.exp(shape*y))
    if shape < 0:
        out = 1 - out
    return out

# print(pglg(x = [-1.24589932, -0.36651292, 0.32663426], shape = 1))
# print(pglg(x = [-0.3266343, 0.3665129, 1.2458993], shape = 1))