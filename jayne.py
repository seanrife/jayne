import argparse
import config
from analyze import get_distance
from parse_tei import process_tei
from printout import display
import csv
from multiprocessing import Pool
from itertools import combinations
import os
import time

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

version = '0.64'

settings = vars(aParser.parse_args())
in_dir = settings["in_dir"]
out_file = settings["out_file"]

min_length = config.analysis['min_length']
cutoff_score = config.analysis['cutoff_score']
analysis_type = config.analysis["analysis_type"]
process_count = config.system["process_count"]

logfile_name = time.strftime("%Y-%m-%d_%H;%M;%S") + '.log'

completed_list = []

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


def mkdirp(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


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


# This function makes me feel sad
def compare(file1, file2, list1, list2):
    start_time = time.process_time()

    pool = Pool()

    for item1 in list1:
        for item2 in list2:
            pool.apply_async(run_comparison, args=(item1, item2, file1, file2))
    pool.close()
    pool.join()
    end_time = time.process_time()
    logger('END TIME: {0}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    logger('Time to process: '.format(end_time-start_time))


def generate_pairlist(results):
    keylist = []
    combo_list = []
    for k, v in results.items():
        keylist.append(k)
    combos = combinations(keylist, 2)
    for combo in combos:
        combo_list.append(combo)
    return combo_list


def create_pairs(results):
    pairlist = generate_pairlist(results)
    pairs = []
    for pair in pairlist:
        dict = {
                'file1': pair[0],
                'file2': pair[1],
                'list1': results[pair[0]],
                'list2': results[pair[1]]
                }
        pairs.append(dict)
    return pairs


def logger(text):
    with open(logfile_name, mode='a') as logfile:
        logfile.write(text + '\n')


def run_comparison(item1, item2, file1, file2):
    distance = get_distance(item1, item2)
    if distance <= cutoff_score:
        handle_output(file1,
                      file2,
                      item1,
                      item2,
                      distance,
                      analysis_type)


results = process_tei(in_dir, min_length)

print("Creating pairs...")

paired_papers = create_pairs(results)

print("Done! Running comparisons.")

mkdirp('logs')

logger('jayne v{0} initialized'.format(version))
logger('START TIME: {0}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
logger('Total number of comparisons requested: '.format(len(paired_papers)))
logger('Number of independent processes: '.format(process_count))
logger('')

processes = []

for pair in paired_papers:
    comparison = compare(pair['file1'], pair['file2'], pair['list1'], pair['list2'])
