import argparse
from pdfrw import PdfReader
import os
from nltk.tokenize import sent_tokenize
from fuzzywuzzy import fuzz

aParser = argparse.ArgumentParser(
    description='Extract text from PDFs and analyze their similarity.')
aParser.add_argument(
    "-d",
    "--dir",
    required=True,
    help="Directory with the PDFs")
aParser.add_argument(
    "-n",
    "--num",
    required=False,
    help="Number of words")

settings = vars(aParser.parse_args())


def extract_text(file):
    print(file)
    complete_text = ""
    with open(file, "rb") as file:
        pdf = PyPDF2.PdfFileReader(file)
        max_page = pdf.numPages
        for page in range(max_page):
            page_meta = pdf.getPage(page)
            complete_text = complete_text + page_meta.extractText()
    complete_text = complete_text.replace("\n", " ")
    print(complete_text)
    return complete_text


main_dict = {}

print("Extracting text from PDFs... this may take a while.")

for file in os.listdir(settings["dir"]):
    if file.endswith(".pdf"):
        working_text = extract_text(settings["dir"] + "/" + file)
        sent_tokenized = sent_tokenize(working_text)
        main_dict[file] = sent_tokenized

#print(main_dict)

print("Text extracted. Analyzing fingerprints...")

out_list = []

for _key, _value in main_dict.items():
    #print(_key)
    for key, value in main_dict.items():
        if _key != key:
            for _v in _value:
                for v in value:
                    similarity = fuzz.ratio(v, _v)
                    if similarity > 80:
                        print("File 1: {0}: ".format(_key))
                        print("File 2: {0}: ".format(key))
                        print(_v)
                        print(v)
