"""
Quantile function of a Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import numpy as np
from scipy.stats import chi2

def qglg(x = 0.5, location = 0, scale = 1, shape = -1):
    x = np.array(x)
    s_two = shape**2
    n = x.size
    new_x = np.zeros(n)
    if (shape < 0):
        x = 1 - x     
    for i in range(0,n):
        new_x[i] = (1/shape)*np.log((0.5*s_two)*chi2.ppf(x[i], df = 2/s_two))
    
    new_x = location + scale * new_x
    return new_x

# print(qglg(x= [0.25,0.5,0.75]))