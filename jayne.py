import argparse
from fuzzywuzzy import fuzz
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

print("Text extracted. Analyzing... (this will probably take forever)")

# report = {}
working_list = []

# This is ugly, slow, inefficient, and probably causes global warming.
# It also analyzes everything twice, which is dumb.
# Other than that, it's fine.
for _key, _value in main_dict.items():
    for _i in _value:
        for key, value in main_dict.items():
            if key == _key:
                continue
            for i in value:
                working_list.append(fuzz.ratio(i, _i))

print("Analyzed similarity of {0} sentences extracted from {1} files."
      .format(len(working_list), len(os.listdir(settings["dir"]))))
print("Total similarity: {0}".format((sum(working_list))/len(working_list)))
