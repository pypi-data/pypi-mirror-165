"""
Simple Random Sampling without Replacement of a population of size N.
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import random
import numpy as np

def srswor (n = 2, N = 5):
    """Select a sample of n sampling units from a sampling frame of size N.

    Parameters
    ----------
    n : int, default = 2
      Sample Size.
    N : int, default = 2
      Population Size.  
    Returns
    -------
    s : ndarray of shape (1, )
        Indexes of the sampling units to be considered in the sample.
    """ 
    s = np.zeros(N)
    i = 0
    value = random.randint(0, N-1)
    index = [value]
    while i <= (n-1):
        s[value] = 1
        i += 1
        value = random.randint(0, N-1)
        while value in index:
           value = random.randint(0, N-1)
        index.append(value) 
    return s      
