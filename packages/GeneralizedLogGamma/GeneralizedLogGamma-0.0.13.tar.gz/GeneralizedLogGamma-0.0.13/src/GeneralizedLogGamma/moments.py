"""
Mean, Median, Mode,  Variance, Coeficient of Variation, Skewness, Kurtosis of Generalized Log-gamma distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import numpy as np
import scipy.special as ssp
from qglg import qglg 

def lss(location = 0, scale = 1, shape = 1):

    shape_two = shape**2
    inv_shape_two = 1/shape_two
    mean = location + scale*((ssp.polygamma(0, inv_shape_two) - np.log(inv_shape_two))/shape)
    median = qglg(x = [0.5] , location = location, scale = scale, shape = shape)
    variance = (scale**2) * (inv_shape_two) * ssp.polygamma(1, inv_shape_two)
    if(abs(shape) < 0.09):
      cv = print("It is not defined because the mean of this distribution is too close to zero!")
    else:
      cv = np.square(variance)/mean
    skewness = np.sign(shape) * ssp.polygamma(2, inv_shape_two)/ssp.polygamma(1, inv_shape_two)**1.5
    kurtosis = (ssp.polygamma(3, inv_shape_two)/(ssp.polygamma(1, inv_shape_two)**2)) + 3
    return { 'mean' : mean, 
             'median' : median, 
             'mode' : location, 
             'variance' : variance, 
             'cv' : cv, 
             'skewness' : skewness, 
             'kurtosis' : kurtosis 
             }


print(lss())