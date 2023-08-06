
def return_type(clusters_found, output):
    
    if output == "network":
        return network_graph(clusters_found)
    elif output == "df":
        return cluster_df(clusters_found)
    elif output == "edgelist":
        return edge_list_df(clusters_found)
    else:
        return clusters_found
    

def network_graph(clustered_nodes):
    '''
    Generate a networkx graph from the clusters found.

    Given a list of tuples of the form (sequence, cluster_id, edit_pos) for each cluster, return a networkx graph.
    Each node in the graph is a sequence, and each edge is a pair of sequences in the same cluster.
    '''
    import networkx as nx
    from itertools import combinations
    from more_itertools import flatten
    
    cluster_edges = map(lambda cluster: combinations(cluster, 2), clustered_nodes)
    return nx.from_edgelist(flatten(cluster_edges))

def cluster_df(clusters_found):
    '''
    Generate a dataframe from the clusters found.

    Given a list of tuples of the form (sequence, cluster_id, edit_pos) for each cluster, return a dataframe.
    Each row in the dataframe is a sequence, and each column is a cluster.
    '''
    import pandas as pd

    clusters_found = list(map(lambda cluster_seq: ",".join(cluster_seq), clusters_found))
    return pd.DataFrame(clusters_found, columns=["sequences"])

def edge_list_df(clusters_found):
    '''
    Generate a dataframe from the edges found.

    Given a list of tuples of the form (sequence1, sequence2, cluster_id, edit_pos) for each pair of sequences in the same cluster, return a dataframe.
    Each row in the dataframe is a pair of sequences, and each column is a cluster.
    '''
    import networkx as nx

    net = network_graph(clusters_found)
    edges_list_df = nx.to_pandas_edgelist(net, nodelist=['seq1', 'seq2'])
    return edges_list_df
