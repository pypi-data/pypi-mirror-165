from itertools import combinations, count, groupby, repeat, starmap, chain
import operator

def tokenize(string, ss):
    tokens = combinations(string, len(string)-1)
    return tokens if ss else chain([tuple(string)], tokens)

def hash_sort(sequences, substings_only):
    
    def skip_comb(string, full_string):
        comb = combinations(string, len(string)-1)
        comb = chain([tuple(string)], comb) if full_string else comb
        hash_comb = zip(map(hash, comb), count(-1), repeat(string))
        return hash_comb
    
    hash_key = map(lambda s: skip_comb(s, substings_only), sequences)
    return sorted(chain(*hash_key), key=lambda k:k[0]+k[1])

def hash_clsuter(sorted_keys, key_i):
    grouped = groupby(sorted_keys, key=operator.itemgetter(*key_i))
    return grouped

def deletion(hash_grouped):
    clusters, gap = [], None
    for p, c in groupby(hash_grouped, key=lambda k: k[1]):
        
        if p == -1:
            gap = set(c)
            continue
        elif gap:
            c = set(c).union(gap)
        else:
            c = set(c)
            
        if len(c)>1:
            clusters.append(c)

    return clusters

def preprocess(sequences, min_len, max_len):
    '''
    Filter sequences by length.

    Given a list of sequences, return a list of sequences with length between min_len and max_len.
    '''
    if min_len < 2:
        min_len = 2
    if max_len is None:
        return filter(lambda s: isinstance(s, str) and len(s) >= min_len, sequences)
    return filter(lambda s: isinstance(s, str) and len(s) >= min_len and len(s) <= max_len, sequences)

def cluster(string_list, with_deletion=False):
    
    string_list = preprocess(string_list)
    
    sub_keys = hash_sort(string_list, with_deletion)
    
    if with_deletion:
        clusters = hash_clsuter(sub_keys, [0])
        clusters = starmap(lambda h, g: deletion(g), clusters)
        clusters = chain(*clusters)
    else:
        clusters = hash_clsuter(sub_keys, [0, 1])
        clusters = starmap(lambda k, g: set(g), clusters)
        clusters = filter(lambda c: len(c)>1, clusters)
    
    return [{s[-1] for s in c} for c in clusters]


def cluster_file(file_path, cluster_column="aaSeqCDR3", has_h=0, delim='\t'):
    import pandas as pd
    col_seq_list = pd.read_csv(file_path, usecols=[cluster_column], header=has_h, sep=delim).iloc[:,0].to_list()
    return cluster(col_seq_list)