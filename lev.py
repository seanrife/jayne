from similarity.normalized_levenshtein import NormalizedLevenshtein
from parse_tei import *
from printout import display

in_dir = '/home/sean/jayne/docs/naser/'
min_length = 100

normalized_levenshtein = NormalizedLevenshtein()

results = process_tei(in_dir, min_length)

papers_analyzed = len(results)

count_l1 = 0

for result in results:
    result_len = len(result)
    count_l2 = 0
    for graf in result:
        while count_l2 < result_len:
            graf2 = results[count_l1][count_l2]
            if len(graf) > 10 and len(graf2) > 10:
                ld = normalized_levenshtein.distance(graf, graf2)
                if ld >= .9:
                    display(graf, graf2, ld, "LD")
                count_l2 = count_l2 + 1
    count_l1 = count_l1 + 1
