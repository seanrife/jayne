grobid = {
    'host': 'localhost',
    'path': 'grobid',
    'port': '8070'
    }

analysis = {
    'min_length': 100,
    'analysis_type': 'lev',
    'cutoff_score': .2,
    'qgram_val': 4,
    'ngram_val': 4,
    'level': 'paragraph'
}

system = {
    'process_count': 200
}
