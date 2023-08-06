"""
Survival Function of Generalized Gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import numpy as np
from scipy.special import gammainc
from pglg import pglg 

def surv_gg(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    if np.min(x > 0) == False:
       print('x must be a list of positive numbers.')
       return None   
    out = 1 - pglg(x, location, scale, shape)
    return out


#print(surv_gg(x = [15, 3, 2, 1, 0.0000001], shape = -1))
#print(surv_gg(x = [0.000000001, 1, 2], scale = 0.5, shape = 1 ))
#print(surv_gg(x = -1))