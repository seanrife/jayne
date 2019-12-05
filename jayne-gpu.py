import tensorflow as tf
import argparse
import config
from parse_tei import process_tei
from printout import display
import csv
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


def create_sparse_vec(word_list):
    num_words = len(word_list)
    indices = [[xi, 0, yi] for xi, x in enumerate(word_list) for yi, y in enumerate(x)]
    chars = list(''.join(word_list))
    return(tf.SparseTensorValue(indices, chars, [num_words, 1, 1]))


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


def create_sparse_inputs(text, item):
    hypothesis = [text]
    truth = [item]
    hyp_string_sparse = create_sparse_vec(hypothesis)
    truth_string_sparse = create_sparse_vec(truth*len(hypothesis))
    return hyp_string_sparse, truth_string_sparse


def compare(file, text, data):
    count = 0
    for key, v in data.items():
        count = count + 1
        for item in v:
            if (len(text) > min_length and len(item) > min_length and
                    key is not file):
                hypothesis, truth = create_sparse_inputs(text, item)
                hyp_input = tf.sparse_placeholder(dtype=tf.string)
                truth_input = tf.sparse_placeholder(dtype=tf.string)
                edit_distances = tf.edit_distance(hyp_input,
                                                  truth_input,
                                                  normalize=True)
                feed_dict = {hyp_input: hypothesis,
                             truth_input: truth}
                distance = sess.run(edit_distances, feed_dict=feed_dict)
                #print(similarity[0][0])
                if distance[0][0] <= cutoff_score:
                    handle_output(key,
                                  file,
                                  text,
                                  item,
                                  distance[0][0],
                                  analysis_type)
        if count > 0:
            return None


def analyze(data):
    for k, v in data.items():
        for item in v:
            compare(k, item, data)


sess = tf.Session()

sess = tf.Session(config=tf.ConfigProto(
                  device_count={"CPU": 4},
                  inter_op_parallelism_threads=4,
                  intra_op_parallelism_threads=8,
                  ))

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
