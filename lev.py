from similarity.normalized_levenshtein import NormalizedLevenshtein
from parse_tei import process_tei
from printout import display

in_dir = '/home/sean/jayne/docs/naser/'
min_length = 100

normalized_levenshtein = NormalizedLevenshtein()


def compare(file, text, data):
    for key, v in data.items():
        for item in v:
            if len(text) > 100 and len(item) > 100 and key is not file:
                ld = normalized_levenshtein.distance(text, item)
                if ld <= .5:
                    #print(len(text))
                    #print(len(item))
                    print(key)
                    print(file)
                    display(text, item, ld, "LD")


results = process_tei(in_dir, min_length)

for k, v in results.items():
    for item in v:
        compare(k, item, results)
