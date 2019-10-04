import argparse
import config
from analyze import get_distance
from parse_tei import process_tei
from printout import display
import csv
import asyncio
from aiomultiprocess import Pool

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


async def compare(package):
    file, text, data = package
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


async def run():
    for k, v in results.items():
        for item in v:
            package = (k, item, results)
            async with Pool() as pool:
                await pool.map(compare, (package,))


results = process_tei(in_dir, min_length)

asyncio.run(run())
