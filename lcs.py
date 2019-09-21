from similarity.longest_common_subsequence import LongestCommonSubsequence
from parse_tei import *

in_dir = '/home/sean/jayne/docs/naser/'
min_length = 100

lcs = LongestCommonSubsequence()

results = process_tei(in_dir, min_length)

papers_analyzed = len(results)

count_l1 = 0

for result in results:
    result_len = len(result)
    count_l2 = 0
    for graf in result:
        while count_l2 < result_len:
            lcs_r = lcs.distance(graf, results[count_l1][count_l2])
            if lcs_r >= 2000:
                display(graf, results[count_l1][count_l2], lcs_r, "LCS")
            count_l2 = count_l2 + 1
    count_l1 = count_l1 + 1
