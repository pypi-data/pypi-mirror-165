import pandas as pd
import os


def prepare(sequence_list, min_len, max_len):
    '''
    Filter sequences by length.

    Given a list of sequences, return a list of sequences with length between min_len and max_len.
    '''
    if not isinstance(min_len, int) or min_len < 2:
        min_len = 2

    if not isinstance(max_len, int):
        return filter(lambda s: isinstance(s, str) and len(s) >= min_len, sequence_list)
    elif max_len <= min_len:
        return filter(lambda s: isinstance(s, str) and len(s) == min_len, sequence_list)
    else:
        return filter(lambda s: isinstance(s, str) and len(s) >= min_len and len(s) <= max_len, sequence_list)



# AIRR-seq community format out headers
out_headers = ['sequence_id', 'sequence', 'v_call', 'd_call', 'j_call', 'junction_aa', 'duplicate_count',
            'rev_comp', 'productive', 'sequence_alignment', 'germline_alignment',
            'junction', 'v_cigar', 'd_cigar', 'j_cigar']


def read_mixcr_cdr3(input_path, get_column='aaSeqCDR3', delim='\t'):
    '''
    Read mixcr output.

    Read and return list of the specified column data Path to the mixcr output from the given file / list of file / directory path.

    '''
    if isinstance(input_path, str):
        if os.path.isdir(input_path):
            input_path = [os.path.join(input_path, file) for file in os.listdir(input_path)]
        else:
            input_path = [input_path]

    def read_sequences(mixcr_file):
        if os.path.exists(mixcr_file) and os.path.isfile(mixcr_file):
            df = pd.read_csv(mixcr_file, header=0, sep=delim)
            if get_column in df.columns:
                return df[get_column].tolist()
        return []
    
    return [read_sequences(file_path) for file_path in input_path] if isinstance(input_path, list) else []


