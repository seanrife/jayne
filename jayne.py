import argparse
import config
from analyze import get_distance
from parse_tei import process_tei
from printout import display
import csv
import multiprocessing as mp
from itertools import combinations

aParser = argparse.ArgumentParser(
    description='Analyze the similarity of text in TEI XML files.')

aParser.add_argument(
    "-i",
    "--in-dir",
    required=True,
    help="Directory with XML files")

aParser.add_argument(
    "-o",
    "--out-file",
    required=False,
    help="File to store results")

settings = vars(aParser.parse_args())
in_dir = settings["in_dir"]
out_file = settings["out_file"]

min_length = config.analysis['min_length']
cutoff_score = config.analysis['cutoff_score']
analysis_type = config.analysis["analysis_type"]
process_count = config.system["process_count"]

if out_file:
    with open(out_file, mode='a') as csv_file:
        oa_writer = csv.writer(csv_file,
                               delimiter='\t',
                               quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        oa_writer.writerow(["analysis_type",
                            "score", "file1",
                            "text1",
                            "file2",
                            "text2"])


def write_line(out_file, file1, file2, text1, text2, score, score_type):
    with open(out_file, mode='a') as csv_file:
        oa_writer = csv.writer(csv_file,
                               delimiter='\t',
                               quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        oa_writer.writerow([score_type, score, file1, text1, file2, text2])


def handle_output(key, file, text, item, distance, analysis_type):
    display(key, file, text, item, distance, analysis_type)
    if out_file:
        write_line(out_file, key, file, text, item, distance, analysis_type)


def compare(file, text, data):
    for key, v in data.items():
        for item in v:
            if (len(text) > min_length and len(item) > min_length and
                    key is not file):
                distance = get_distance(text, item)
                if distance <= cutoff_score:
                    handle_output(key,
                                  file,
                                  text,
                                  item,
                                  distance,
                                  analysis_type)


# TODO: change "chunk" to "chonk" because James likes cats
def create_chunk(keys, results):
    chunk = {}
    for key in keys:
        chunk[key] = results[key]
    return chunk


def create_chunks(results):
    chunk_list = []
    key_combinations = combinations(results, 2)
    for keys in key_combinations:
        chunk = create_chunk(keys, results)
        chunk_list.append(chunk)
    return chunk_list


def analyze_chunk(chunk):
    for k, v in chunk.items():
        for item in v:
            compare(k, item, chunk)


def run(chunk):
    for item in chunk:
        print(item.keys())
        analyze_chunk(item)


results = process_tei(in_dir, min_length)

jobs = []

chunks_as_list = create_chunks(results)

chunk_size = int(len(chunks_as_list)/process_count)
print(chunk_size)

chunks = [chunks_as_list[x:x+chunk_size]
          for x in range(0, len(chunks_as_list), chunk_size)]
for chunk in chunks:
    p = mp.Process(target=run, args=(chunk,))
    jobs.append(p)
    p.start()
