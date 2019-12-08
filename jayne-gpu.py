import tensorflow.compat.v1 as tf
import argparse
import config
from parse_tei import process_tei
from printout import display
import csv
import os
import time

tf.disable_v2_behavior()

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

version = '0.58'

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


def logger(text):
    with open(logfile_name, mode='a') as logfile:
        logfile.write(text + '\n')


def compare(file, text, data):
    count = 0
    for key, v in data.items():
        count = count + 1
        if key is not file:
            print([text])
            hypothesis_list = v
            truth_list = [text]
            num_h_words = len(hypothesis_list)
            h_indices = [[xi, 0, yi] for xi, x in enumerate(hypothesis_list) for yi, y in enumerate(x)]
            h_chars = list(''.join(hypothesis_list))
            h = tf.SparseTensor(h_indices, h_chars, [num_h_words, 1, 1])
            truth_word_vec = truth_list*num_h_words
            t_indices = [[xi, 0, yi] for xi, x in enumerate(truth_word_vec) for yi, y in enumerate(x)]
            t_chars = list(''.join(truth_word_vec))
            t = tf.SparseTensor(t_indices, t_chars, [num_h_words, 1, 1])
            print(sess.run(tf.edit_distance(h, t, normalize=True)))


def analyze(data):
    for k, v in data.items():
        for item in v:
            compare(k, item, data)


sess = tf.Session(config=tf.ConfigProto(intra_op_parallelism_threads=10))

start_time = time.clock()

mkdirp('logs')

logger('jayne v{0} initialized'.format(version))
logger('START TIME: {0}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
logger('')


results = process_tei(in_dir, min_length)

analyze(results)

end_time = time.clock()

logger('END TIME: {0}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
logger('Time to process: '.format(end_time-start_time))
