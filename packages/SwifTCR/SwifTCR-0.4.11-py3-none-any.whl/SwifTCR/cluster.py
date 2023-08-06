from itertools import combinations, count, repeat, chain
from more_itertools import split_when, unique_justseen, prepend



__all__ = ['get_clusters']





def hash_sort(sequences, substring_only=True):

    def skip_comb(string):
        hash_sub = map(hash, combinations(string, len(string)-1))
        return zip(hash_sub, count(), repeat(string))

    def skip_comb_del(string):
        hash_sub = map(hash, prepend(tuple(string), combinations(string, len(string)-1)))
        return zip(hash_sub, count(), repeat(string))

    sub_keys = map(skip_comb, sequences) if substring_only else map(skip_comb_del, sequences)
    sorted_keys = sorted(chain(*sub_keys), key=lambda k:k[0]+k[1])
    return unique_justseen(sorted_keys)

def replacement(sequence_list):
    sorted_keys = hash_sort(sequence_list)
    clusters = split_when(sorted_keys, lambda s1,s2: s1[:2] != s2[:2])
    return [{s[-1] for s in c} for c in clusters if len(c)>1]


def replacement_and_deletion(sequence_list):

    sorted_keys = hash_sort(sequence_list, substring_only=False)  
    
    clusters = []
    for hash_groups in split_when(sorted_keys, lambda s1,s2: s1[0]!=s2[0]):
        
        if len(hash_groups)==1:
            continue
        
        if not hash_groups[0][1]:
            clusters += [{s[-1] for s in prepend(hash_groups[0], cluster)} 
                for cluster in split_when(hash_groups[1:], lambda s1,s2: s1[1] != s2[1])]
        else:
            clusters += [{s[-1] for s in cluster} 
                for cluster in split_when(hash_groups, lambda s1,s2:s1[1]!=s2[1]) if len(cluster)>1]

    return clusters



def get_clusters(sequence_list, replacement_only=True):
    '''
    group together strings with single edit distance 

    Create a list containing all strings sub-groups sharing a single
    charachter replacement or deletion at the same possition.

    Parameters
    ----------
    sequence_list : list
        list of strings
    replacement_only : bool, optional
        if True returns sub-groups of the given stings sharing a single 
        character replacement. For False also character deletion is 
        included, by default True

    Returns
    -------
    list
        list of string sets
    '''
    return replacement(sequence_list) if replacement_only else replacement_and_deletion(sequence_list)