import argparse
import PyPDF2
import os
from nltk.tokenize import sent_tokenize

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
    complete_text = ""
    with open(file, "rb") as file:
        pdf = PyPDF2.PdfFileReader(file)
        max_page = pdf.numPages
        for page in range(max_page):
            page_meta = pdf.getPage(page)
            complete_text = complete_text + page_meta.extractText()
    return complete_text


main_dict = {}

print("Extracting text from PDFs... this may take a while.")

for file in os.listdir(settings["dir"]):
    if file.endswith(".pdf"):
        working_text = extract_text(settings["dir"] + "/" + file)
        sent_tokenized = sent_tokenize(working_text)
        main_dict[file] = sent_tokenized

print("Text extracted. Analyzing fingerprints...")

out_list = []

for _key, _value in main_dict.items():
    for key, value in main_dict.items():
        if _value == value:
            out_list.append(_value)
