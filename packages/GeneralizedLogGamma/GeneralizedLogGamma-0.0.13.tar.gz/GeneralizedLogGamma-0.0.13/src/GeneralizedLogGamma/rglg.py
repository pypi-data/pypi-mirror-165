"""
Random generating function of Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import random
import numpy as np
from scipy.stats import chi2

def rglg(n, location = 0, scale = 1, shape = 1):
    pQ = np.zeros(n)
    s_two = shape^2
    for i in range(0,n) :
        quantile = random.uniform(0, 1)
        pQ[i] = (1/np.abs(shape)) * math.log((0.5 * s_two) * chi2.ppf(quantile, df = 2/s_two))
        pQ[i] = location + scale * pQ[i]
    
    return pQ

muestra = rglg(n = 10000)
print(np.mean(muestra))
print(np.median(muestra))
print(np.var(muestra))