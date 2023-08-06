"""
Hansen-Hurvitz Estimator (HH)
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import random
import numpy as np

def hh_est (s = [1, 2, 3], probs = [0.3, 0.1, 0.4]):
    """Calculate the Hansen-Hurvitz Estimator of a population total parameter.

    Parameters
    ----------
    s : list or array-like, default = [1,2,3]
      Ordered Sample values of the interest variable.
    probs : list or array-like , default = [0.1, 0.2, 0.7]
      Vector with the selection probabilities of the elements in s.  
    Returns
    -------
    output : ndarray of shape (1, )
        The Hansen-Hurvitz Estimator evaluated in the sample.
    """  
    s = np.array(s)
    pi_vector = np.array(probs)
    output = (1/s.size)*sum(s/probs)
    return output      

# print(hh_est())