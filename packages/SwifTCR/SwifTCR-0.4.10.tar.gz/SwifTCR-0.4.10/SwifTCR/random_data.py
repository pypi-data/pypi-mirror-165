import numpy as np
import random
import scipy.stats as ss


__all__ = ['random_repertoire']



AA =   ['A', 'C', 'D', 'E', 'F', 
        'G', 'H', 'I', 'K', 'L', 
        'M', 'N', 'P', 'Q', 'R', 
        'S', 'T', 'V', 'W', 'Y']

def random_repertoire(seq_n, min_len=8, max_len=18, alphabet=None):
    '''
    Generate list of CDR3 amino acid sequences

    Generate strings with distribiutions of the repertoire's size, sequences' 
    size and amino acid types py position that are more or less similar to 
    real data samples of TCR repertoire.


    Parameters
    ----------
    seq_n : int
        Number of unique sequences
    min_len : int, optional
        Minimum sequence size to be generated, by default 8
    max_len : int, optional
        Maximum sequence size to be generated, by default 18

    Returns
    -------
    list
        Strings of amino acid sequences
    '''
    if isinstance(alphabet, int):
        alphabet = AA[:alphabet]

    sequence_lengths = normal_dist_int(min_len, max_len, seq_n, 2)
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