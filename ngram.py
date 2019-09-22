from similarity.ngram import NGram
from parse_tei import *
from printout import display

in_dir = '/home/sean/jayne/docs/naser/'
min_length = 100

ngram = NGram(4)

def compare(file, text, data):
    for key, v in data.items():
        for item in v:
            if len(text) > 200 and len(item) > 200 and key is not file:
                ng = ngram.distance(text, item)
                if ng <= .7:
                    #print(len(text))
                    #print(len(item))
                    print(key)
                    print(file)
                    display(text, item, ng, "Ngram")


results = process_tei(in_dir, min_length)

for k, v in results.items():
    for item in v:
        compare(k, item, results)
