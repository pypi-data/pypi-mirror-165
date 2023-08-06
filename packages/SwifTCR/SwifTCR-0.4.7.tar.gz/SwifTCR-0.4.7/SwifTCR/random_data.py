import numpy as np
import random
import scipy.stats as ss

AA =   ['A', 'C', 'D', 'E', 'F', 
        'G', 'H', 'I', 'K', 'L', 
        'M', 'N', 'P', 'Q', 'R', 
        'S', 'T', 'V', 'W', 'Y']

def random_repertoire(seq_n, min_len=8, max_len=18, alphabet=None, sigma=2):
    
    if isinstance(alphabet, int):
        alphabet = AA[:alphabet]
    else:
        alphabet = AA

    sequence_lengths = normal_dist_int(min_len, max_len, seq_n, sigma)
    return ["".join(random.choices(alphabet, k=seq_size)) for seq_size in sequence_lengths]


def normal_dist_int(l, h, n, sigma):
    lengths = np.arange(l,h+1)
    d = lengths.size / 2
    x = np.arange(-d,d, 1) 
    xU, xL = x + 1, x
    prob = ss.norm.cdf(xU, scale = sigma) - ss.norm.cdf(xL, scale = sigma)
    prob = prob / prob.sum()
    nums = np.random.choice(lengths, size = n, p = prob)
    return nums