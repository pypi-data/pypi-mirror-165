"""
Horvitz-Thompson Estimator (HT)
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import random
import numpy as np

def ht_est (s = [1,2,5], pi_vector = [0.1, 0.2, 0.5]):
    """Calculate the Horvitz-Thompson Estimator of population total parameter.

    Parameters
    ----------
    s : list or array-like, default = [1,2,5]
      Sample values of the interest variable.
    pi_vector : list or array-like , default = [0.1, 0.2, 0.5]
      Vector with the inclusion probabilities of first-order of the elements in s.  
    Returns
    -------
    output : ndarray of shape (1, )
        The Horvitz-Thompson Estimator evaluated in the sample.
    """  
    s = np.array(s)
    pi_vector = np.array(pi_vector)
    output = sum(s/pi_vector)
    return output      

#print(ht())