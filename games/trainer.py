import random
import numpy as np
import matplotlib.pyplot as plt

from RPSGame import *

def rargmax(vector):
    ''' returns random argmax of vector '''
    m = np.amax(vector)
    indices = np.nonzero(vector == m)[0]
    return random.choice(indices)

