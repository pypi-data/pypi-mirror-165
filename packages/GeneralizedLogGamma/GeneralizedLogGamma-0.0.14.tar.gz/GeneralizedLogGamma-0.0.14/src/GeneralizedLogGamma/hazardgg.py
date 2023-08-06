"""
Hazard Function of a Generalized Gamma Distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import numpy as np
from scipy.special import gammainc
from dglg import dglg
from survgg import surv_gg 

def hazard_gg(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    if np.min(x > 0) == False:
       print('x must be a list of positive numbers.')
       return None   
    out = dglg(x, location, scale, shape)/(x*surv_gg(x, location, scale, shape))
    return out


#print(hazard_gg(x = [15, 3, 2, 1, 0.0000001], shape = -1))
#print(hazard_gg(x = [0.001, 1, 1.81], scale = 0.5, shape = 1))
#print(hazard_gg(x = -1))