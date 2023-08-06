"""
Random generating function of K-th Order Statistics from a Generalized Log-gamma Distribution
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import numpy as np
import scipy.stats as stats
from qglg import qglg
from dglg import dglg

def order_glg (size, mu = 0, sigma = 1, shape = 1, k = 1, n = 1, alpha = 0.05):
  '''
  Parameters
  ----------
  size int, represents the size of the sample.
  mu float, represents the location parameter. Default value is 0.
  sigma float, represents the scale parameter. Default value is 1.
  lambda float, represents the shape parameter. Default value is 1.
  k int, represents the K-th smallest value from a sample.
  n int, represents the size of the sample to compute the order statistic from.
  alpha float, (1 - alpha) represents the confidence of an interval for the population median of the distribution of the k-th order statistic. Default value is 0.05.
  
  Returns
  -------
  A list with an one numpy array random sample of order statistics from a generalized log-gamma distribution and the join probability density function evaluated in the random sample.
  '''

  initial = stats.beta.rvs(size = size, a= k, b = n + 1 - k)
  sample  = qglg(initial, mu, sigma, shape)
  pdf     = math.factorial(size) * np.cumprod( dglg(x = sample, location= mu, scale = sigma, shape = shape))[size - 1]
  if (size > 5):
    return [sample, pdf]
  print("---------------------------------------------------------------------------------------------\n")
  print("We cannot report the confidence interval. The size of the sample is less or equal than five.\n")
  return [sample, pdf]

#print(order_glg(size = 6, shape = -1))
