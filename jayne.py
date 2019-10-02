import argparse
import config
from analyze import get_distance
from parse_tei import process_tei
from printout import display

aParser = argparse.ArgumentParser(
    description='Analyze the similarity of text in TEI XML files.')

aParser.add_argument(
    "-i",
    "--in-dir",
    required=True,
    help="Directory with XML files")

settings = vars(aParser.parse_args())
in_dir = settings["in_dir"]

min_length = config.analysis['min_length']
cutoff_score = config.analysis['cutoff_score']


def compare(file, text, data):
    for key, v in data.items():
        for item in v:
            if (len(text) > min_length and len(item) > min_length and
                    key is not file):
                distance = get_distance(text, item)
                if distance <= cutoff_score:
                    display(key, file, text, item, distance, analysis_type)


results = process_tei(in_dir, min_length)

for k, v in results.items():
    for item in v:
        compare(k, item, results)
