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
    return sorted(substings, key=lambda k:hash(k[0])+k[1])

def hash_clsuter(string_list, substring_only):
    substring_keys = skip_substrings(string_list, substring_only)
    sorted_hash_keys = hash_sort(substring_keys)
    sorted_hash_keys = unique_justseen(sorted_hash_keys)
    grouped = groupby(sorted_hash_keys, key=lambda x: hash(x[0]))
    return grouped

def deletion(hash_clusters):
    is_gap = next(hash_clusters)
    if is_gap[0] == -1:
        hash_clusters = starmap(lambda p, c: (p, is_gap[1] + c), hash_clusters)
    else:
        hash_clusters = chain([is_gap], hash_clusters)
    return hash_clusters
    
def valid_clusters(grouped_hash, include_sting):
    grouped_hash = groupby(grouped_hash, key=operator.itemgetter(1))
    grouped_hash = starmap(lambda p, c: (p, list(map(operator.itemgetter(-1), c))), grouped_hash)
    return deletion(grouped_hash) if include_sting else grouped_hash

def cluster(string_list, deletion=False):
    clusters_found = hash_clsuter(string_list, deletion)
    return [(p, c) for h, g in clusters_found 
        for p, c in valid_clusters(g, deletion) 
            if len(c) > 1]