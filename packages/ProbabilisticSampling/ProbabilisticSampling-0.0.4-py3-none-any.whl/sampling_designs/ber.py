"""
Bernoulli Sampling with inclusion probability p of a population of size N. 
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import random
import numpy as np

def ber (p = 0.25, N = 5):
    """Select a sample under a Bernoulli sampling scheme of population of size of N.

    Parameters
    ----------
    p : float, default = 0.25
      Inclusion Probability.  
    N : int, default = 5
      Population Size.  
    Returns
    -------
    s : ndarray of shape (1, )
        Indexes of the sampling units to be considered in the sample.
    """ 
    s = np.zeros(N)
    for i in range(0,N):
        print(i)
        value = random.random()
        if value < p:
           s[i] = 1
        i += 1
    return s      

#muestra = ber(p = 0.1, N = 1000)
#print(muestra)
#print(np.sum(muestra))
