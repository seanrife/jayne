from similarity.ngram import NGram
from parse_tei import *
from printout import display

in_dir = '/home/sean/jayne/docs/naser/'
min_length = 100

gram = NGram(4)

results = process_tei(in_dir, min_length)

papers_analyzed = len(results)

count_l1 = 0

for result in results:
    result_len = len(result)
    count_l2 = 0
    for graf in result:
        while count_l2 < result_len:
            gd = gram.distance(graf, results[count_l1][count_l2])
            print(gd)
            if gd >= .9:
                display(graf, results[count_l1][count_l2], gd, "Ngram")
            count_l2 = count_l2 + 1
    count_l1 = count_l1 + 1
