from itertools import chain, combinations, count, groupby, starmap, repeat
from more_itertools import unique_justseen
import operator


def skip_comb(string):
    return combinations(string, len(string)-1)
    # return map(lambda ss: "".join(ss), combinations(string, len(string)-1))

def comb_substrings(sequence):
    '''returns all subsequences of the given sequence with a missing character at a specific index.'''
    return zip(skip_comb(sequence), count(len(sequence)-1, -1), repeat(sequence))

def skip_substrings(string_list, also_sting):
    ''' hashes all subsequences of the given sequences which are all substrings with a missing character at any possible index in a string. '''
    tokens = map(comb_substrings, string_list)
    if also_sting:
        tokens = chain([map(lambda s: (tuple(s), -1, s),string_list)], tokens)
    return chain(*tokens)
def hash_sort(substings):
    return sorted(substings, key=lambda k:(hash(k[0])+k[1], k[-1]))

def hash_clsuter(string_list, substring_only):
    substring_keys = skip_substrings(string_list, substring_only)
    sorted_hash_keys = hash_sort(substring_keys)
    sorted_hash_keys = unique_justseen(sorted_hash_keys)
    grouped = groupby(sorted_hash_keys, key=lambda x: hash(x[0]))
    return grouped

def replacement(hash_clusters):
    hash_clusters = starmap(lambda h, g: groupby(g, key=operator.itemgetter(1)), hash_clusters)
    hash_clusters = starmap(lambda p, c: map(operator.itemgetter(-1), c), chain.from_iterable(hash_clusters))
    return hash_clusters

def cluster(cdr3_list):
    cdr3_list = filter(lambda s: isinstance(s, str) and len(s) >= 2, cdr3_list)
    clusters_found = hash_clsuter(cdr3_list, False)
    clusters_found = replacement(clusters_found)
    clusters_found = filter(lambda c: len(c) > 1, map(list, clusters_found))
    clusters_found = list(clusters_found)
    return clusters_found